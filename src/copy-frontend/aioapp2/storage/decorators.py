from storage.models.trips_table import TripsTable
from config import ddb_config
import logging 

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | [%(levelname)s] : %(name)s | %(lineno)d | %(module)s | %(filename)s | %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logFilePath = "my.log"
file_handler = logging.FileHandler(logFilePath)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def try_connect(region):
    logger.info('trying connection to ' + region.name + region.code)
    TripsTable.change_region(region)
    TripsTable.describe_table()


def check_connection(func):

    def inner(*args, **kwargs):
        for region in ddb_config.regions:
            try:
                try_connect(region)
                break
            except:
                logger.info(region.name + ' failed')
        logger.info('processing request with ' + str(TripsTable.get_host_and_region()[1]))
        results = func(*args, **kwargs)
        TripsTable.change_region(ddb_config.regions[0]) # retores to deafult region
        
        return results
    
    return inner
