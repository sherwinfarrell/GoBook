import time

from datetime import datetime, timezone

from utils.ddb_setup_utils import run_local_db_containers, create_tables_in_all_regions
from models.route import Route
from models.user import User
from models.trip import Trip

from storage.models.trips_table import TripsTable
from storage.storage_client import book_trip, get_user_trips, get_routes, cancel_trip


if __name__ == '__main__':

    user = User('8', 'john')
    route = Route('1', 'ire', 'dub', '8', 'lolz')

    trip = Trip('020bd5f3-63c9-40a5-9a24-0b444035fd83', "book_date_time", "start_date_time", "end_date_time", "route_id", "country", "city", "area", "street", "user_id", "username")

    # print(book_trip(user, route,  datetime.now(timezone.utc).isoformat(timespec='seconds'),  datetime.now(timezone.utc).isoformat(timespec='seconds')))
    # print(book_trip(user, route,  datetime.now(timezone.utc).isoformat(timespec='seconds'),  datetime.now(timezone.utc).isoformat(timespec='seconds')))

    print(cancel_trip(trip))