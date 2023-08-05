import logging


def get_logger():
    logger = logging.getLogger("panager")
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    return logger
