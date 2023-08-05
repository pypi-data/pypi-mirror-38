import logging


def get_logger():
    logger = logging.getLogger("patch_issue")
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    return logger
