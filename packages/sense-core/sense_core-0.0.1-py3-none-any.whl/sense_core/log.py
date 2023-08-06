import logging
import logging.config

__log_path = '.'


def _get_config(root_path='.', is_console=True):
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[{levelname}][{asctime}]{message}',
                'style': '{',
            },
        },
        'handlers': {
            'info': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': root_path + '/info.log',
                'formatter': 'verbose'
            },
            'error': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': root_path + '/error.log',
                'formatter': 'verbose'
            },
        },
        'root': {
            'handlers': ['info', 'error'],
            'level': 'INFO',
        },
    }
    if is_console:
        config['handlers'] = {
            'console': {
                'class': 'logging.StreamHandler',
            }
        }
        config['root'] = {
            'handlers': ['console'],
            'level': 'INFO',
        }
    return config


__logger = None
__module = None


def log_init_config(module='unknown', root_path='.', is_console=False):
    global __logger, __module
    logging.config.dictConfig(_get_config(root_path, is_console))
    __logger = logging.getLogger('root')
    __module = module


def _check_log_init():
    global __logger
    if __logger is None:
        log_init_config()


def log_info(msg):
    global __logger
    if __logger is None:
        return
    __logger.info(msg)


def log_error(msg, module=''):
    global __logger
    if __logger is None:
        return
    if module != '':
        msg = '[' + module + ']' + msg
    __logger.error(msg)


def raise_exception(msg, module=''):
    log_exception(msg, module)
    raise Exception(msg)


def log_exception(msg, module=''):
    global __logger
    if __logger is None:
        return
    if module != '':
        msg = '[' + module + ']' + msg
    __logger.exception(msg)
