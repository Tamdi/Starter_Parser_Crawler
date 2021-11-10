import logging

logging.basicConfig(level=logging.INFO, format='')


def get_logger(name):
    return logging.getLogger(name)



