from storage.models.trips_table import TripsTable
from config import ddb_config


def try_connect(region):
    print('trying connection to ' + region.name + region.code)
    TripsTable.change_region(region)
    TripsTable.describe_table()


def check_connection(func):

    def inner(*args, **kwargs):
        for region in ddb_config.regions:
            try:
                try_connect(region)
                break
            except:
                print(region.name + ' failed')
        print('processing request with ' + str(TripsTable.get_host_and_region()[1]))
        results = func(*args, **kwargs)
        TripsTable.change_region(ddb_config.regions[0]) # retores to deafult region
        
        return results
    
    return inner
