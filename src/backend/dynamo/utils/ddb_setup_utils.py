import docker
import time

from const import ddb_regions
from config import ddb_config

from storage.models.trips_table import TripsTable


def run_local_db_containers():
    client = docker.from_env()
    containers = []

    all_running = False

    for region_name, region in ddb_regions.items():
        try:
            container = client.containers.get(region_name)
        except docker.errors.NotFound:
            container = client.containers.run('amazon/dynamodb-local', ports={'8000/tcp': region.port}, name=region_name, detach=True)

        containers.append(container)

    time.sleep(5)

def create_tables_in_all_regions():
    for region in ddb_regions.values():
        try:
            TripsTable.change_region(region)

            if not TripsTable.exists():
                TripsTable.create_table()
        except:
            print(region.name + ' failed')
    
    TripsTable.change_region(ddb_config.regions[0])


# def handle_db_disconnect():

