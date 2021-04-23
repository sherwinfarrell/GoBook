from config import ddb_config

from models.exceptions import RouteAlreadyBooked
from storage.models.trips_table import TripsTable
from storage.decorators import check_connection


@check_connection
def book_trip(user, route, start_date_time, end_date_time):
    if not user or not route:
        return None

    trip = TripsTable.from_user_and_route(user, route)
    trip.start_date_time = start_date_time
    trip.end_date_time = end_date_time

    try:
        user_trips = get_user_trips(user)
        for t in user_trips:
            print('user got trip ' + t.trip_id + ' ' + t.route_id)
            if t.route_id == route.route_id:
                raise RouteAlreadyBooked
    except RouteAlreadyBooked:
        return None

    try:
        trip.write()
    except Exception:
        return None

    return trip.to_trip()


@check_connection
def get_current_route_capacity(route):
    if not route:
        return None
    try:
        trips = TripsTable.get_trips_by_route_id(route.route_id)
    except Exception:
        return None

    return len(trips)


@check_connection
def get_routes(country, city=None, area=None, street=None):
    try:
        routes = TripsTable.get_routes(country, city, area, street)
    except Exception:
        return None

    return routes


@check_connection
def get_user_trips(user):
    if not user:
        return None
    
    try:
        trips = TripsTable.get_trips_by_user_id(user.user_id)
    except Exception:
        return None

    return trips


@check_connection
def cancel_trip(trip):
    if not trip:
        return None

    try:
        TripsTable.remove_trip_by_id(trip.trip_id)
    except Exception:
        return None
    
    return 'done'

@check_connection
def truncate_table():
    print('cleaning table')
    TripsTable.truncate_table()
    print('finished cleaning')
