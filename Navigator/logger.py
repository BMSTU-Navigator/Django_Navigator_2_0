import logging
logging.basicConfig(filename='ex.log',level=logging.DEBUG)
logger = logging.getLogger('lg')
logger.debug('test')

def log(item):
    print(item)
    logger.debug(item)