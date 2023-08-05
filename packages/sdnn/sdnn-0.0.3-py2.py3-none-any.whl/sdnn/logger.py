import logging


def get_level(level: str):
    level = level.upper()
    return getattr(logging, level)


def create_logger(name: str = None, con_level='INFO', file_level='DEBUG', filename=None):
    con_level = get_level(con_level)
    file_level = get_level(file_level)

    fmt = '%(asctime)s|%(name)s|%(funcName)s:%(lineno)d|%(levelname)s|%(message)s'

    formatter = logging.Formatter(fmt)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(con_level)
    logger.addHandler(ch)

    if filename is not None:
        fh = logging.FileHandler(filename)
        fh.setFormatter(formatter)
        fh.setLevel(file_level)
        logger.addHandler(fh)

    logger.debug('New logger created')
    return logger


if __name__ == '__main__':
    logger = create_logger(con_level='DEBUG', filename='somefile.log')
    logger.debug('hello world')
