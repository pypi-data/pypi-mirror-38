# encoding=utf-8

import os, sys
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL, Formatter, StreamHandler, FileHandler, getLogger
from constant import LOG_DIR

console = StreamHandler()
console.setLevel(INFO)
console.setFormatter(
    Formatter(
        '[%(filename)s-%(funcName)s()][%(levelname)s] %(message)s'
    )
)

def myLogger(fqsn, wf_id, debug=False):
    logger = getLogger(fqsn+'.'+str(wf_id))
    logger.setLevel(DEBUG)

    if debug:
        if console not in logger.handlers:
            logger.addHandler(console)
    else:
        logger.removeHandler(console)

    log_filename = LOG_DIR + fqsn + "." + str(wf_id) + '.log'
    if log_filename not in [h.baseFilename for h in logger.handlers if hasattr(h,'baseFilename')]:
        file_handler = FileHandler(log_filename, 'a')
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(
            Formatter(
                '%(asctime)s [%(filename)s:%(threadName)s:line_%(lineno)s:%(funcName)s()][%(levelname)s] %(message)s'
            )
        )
        logger.addHandler(file_handler)
    return logger


from logging.handlers import TimedRotatingFileHandler

'''
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s [%(filename)s:%(threadName)s:line_%(lineno)s:%(funcName)s()][%(levelname)s] %(message)s',
                    # filename=os.path.join(BASEDIR,'log'+os.sep+'log.txt'),
                    filename=os.path.join(BASEDIR, '..', 'logs', 'apscli.log'),
                    filemode='a')
'''

file_handler = TimedRotatingFileHandler(os.path.join(LOG_DIR, 'apscli.log'), when='D', interval=1, backupCount=30)
file_handler.setLevel(DEBUG)
file_handler.setFormatter(
    Formatter(
        '%(asctime)s [%(filename)s:%(threadName)s:line_%(lineno)s:%(funcName)s()][%(levelname)s] %(message)s'
    )
)

daemon_file_handler = TimedRotatingFileHandler(os.path.join(LOG_DIR, 'daemon.log'), when='D', interval=1, backupCount=30)
daemon_file_handler.setLevel(DEBUG)
daemon_file_handler.setFormatter(
    Formatter(
        '%(asctime)s [%(filename)s:%(threadName)s:line_%(lineno)s:%(funcName)s()][%(levelname)s] %(message)s'
    )
)
