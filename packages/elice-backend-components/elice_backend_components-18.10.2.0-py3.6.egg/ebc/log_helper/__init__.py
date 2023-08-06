import json
import logging
import logging.handlers
import os
import queue
import random
import sys
import threading
import time
import traceback
import urllib.parse
import urllib.request

_DEFAULT_LOGGING_FORMAT = ('[%(levelname)1.1s %(asctime)s P%(process)d %(threadName)s %(module)s:%(lineno)d] '
                           '%(message)s')


class _SlackLoggerThread(threading.Thread):

    MAX_FLUSH_BACKOFF = 64  # 64 seconds

    def __init__(self, log_queue, slack_url):
        super().__init__()
        self.daemon = True
        self.slack_url = slack_url

        self._hostname = os.getenv('DOCKER_HOSTNAME') or os.getenv('HOSTNAME')
        self._log_queue = log_queue
        self._flush_cnt = 0

    def run(self):
        while True:
            if self.flush() == 0:
                self._flush_cnt = 0
            self._flush_cnt += 1

            # https://cloud.google.com/storage/docs/exponential-backoff
            backoff_time = (2 ** self._flush_cnt) + (random.randint(0, 1000) / 1000)
            time.sleep(min(backoff_time, self.MAX_FLUSH_BACKOFF))

    def flush(self):
        logs = []
        while not self._log_queue.empty():
            logs.append(self._log_queue.get())

        if not logs:
            return 0

        msg_text = '*Hostname : %s* \n%d log messages' % (self._hostname, len(logs))
        if 20 < len(logs):
            msg_text += ' (only first 20 logs are attached)'
            logs = logs[:20]

        msg = {
            'payload': json.dumps({
                'text': msg_text,
                'attachments': logs
            })
        }

        urllib.request.urlopen(self.slack_url,
                               data=urllib.parse.urlencode(msg).encode('utf-8'))

        return len(logs)


class _SlackLoggerHandler(logging.handlers.QueueHandler):
    def __init__(self, queue):
        super().__init__(queue)

    def prepare(self, record):
        if len(record.message) <= 80:
            msg_pretext = record.message
        else:
            msg_pretext = record.message[:77] + '...'

        msg_fields = [
            {
                'title': 'LoggerName',
                'value': record.name,
                'short': True
            },
            {
                'title': 'Level',
                'value': record.levelname,
                'short': True
            },
            {
                'title': 'When',
                'value': record.asctime,
                'short': True
            },
            {
                'title': 'Where',
                'value': '%s:%s (in %s)' % (record.module,
                                            record.lineno,
                                            record.funcName),
                'short': True
            },
            {
                'title': 'Process',
                'value': '%s (%d)' % (record.processName,
                                      record.process),
                'short': True
            },
            {
                'title': 'Thread',
                'value': '%s (%d)' % (record.threadName,
                                      record.thread),
                'short': True
            },
            {
                'title': 'Path',
                'value': record.pathname
            }
        ]

        msg_text = record.message
        if record.exc_info is not None:
            traceback_lines = ''.join(traceback.format_exception(*record.exc_info)).splitlines()
            if 100 < len(traceback_lines):
                traceback_lines = traceback_lines[:50] + ['...(truncated)...'] + traceback_lines[-50:]
            msg_text += '\n```%s```' % '\n'.join(traceback_lines)

        return {
            'color': '#ff7777',
            'pretext': 'Message: ' + msg_pretext,
            'text': msg_text,
            'fields': msg_fields
        }


def init_logger(logger_name,
                logging_format=_DEFAULT_LOGGING_FORMAT,
                logger_level=logging.INFO,
                slack_url=None,
                additional_loggers=[]):
    app_logger = logging.getLogger(logger_name)
    log_formatter = logging.Formatter(logging_format)

    log_handlers = []

    # STDOUT handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(log_formatter)
    log_handlers.append(stdout_handler)

    # Slack handler
    if slack_url is not None:
        slack_log_queue = queue.Queue()
        _SlackLoggerThread(slack_log_queue).start()

        slack_handler = _SlackLoggerHandler(slack_log_queue)
        slack_handler.setLevel(logging.ERROR)
        log_handlers.append(slack_handler)

    # TODO: Sentry handler
    pass

    interested_loggers = [
        app_logger,
        *additional_loggers
    ]

    for logger in interested_loggers:
        for log_hadnler in log_handlers:
            logger.addHandler(log_hadnler)

    app_logger.setLevel(logger_level)

    app_logger.info('Logger is started.')

    return app_logger, log_handlers
