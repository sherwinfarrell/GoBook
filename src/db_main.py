from datetime import datetime, timezone

from utils.ddb_setup_utils import run_local_db_containers, create_tables_in_all_regions
from models.route import Route
from models.user import User

from storage.models.trips_table import TripsTable
from storage.storage_client import book_trip, get_user_trips, get_routes


if __name__ == '__main__':

    run_local_db_containers()
    create_tables_in_all_regions()

    print('db running')

    user = User('1', 'john')
    route = Route('1', 'ire', 'dub', '8', 'lolz')

    trip_id = book_trip(user, route,  datetime.now(timezone.utc).isoformat(timespec='seconds'),  datetime.now(timezone.utc).isoformat(timespec='seconds'))

    user_trips = get_user_trips(user)

    print([r.to_string() for r in get_routes('ire')])

