from config import ddb_config

from storage.models.trips_table import TripsTable
from storage.decorators import check_connection


def book_trip(user, route, start_date_time, end_date_time):
    if not user or not route:
        return

    trip = TripsTable.from_user_and_route(user, route)
    trip.start_date_time = start_date_time
    trip.end_date_time = end_date_time

    # writing to all regions for demonstration purposes,
    # writes would automatically replicate using dynamodb global
    # tables in practice.
    for region in ddb_config.regions:
        try:
            TripsTable.change_region(region)
            trip.write()
        except:
            pass
    TripsTable.change_region(
        ddb_config.regions[0])  # changing back to default region

    return trip.trip_id


@check_connection
def get_current_route_capacity(route):
    if not route:
        return

    trips = TripsTable.get_trips_by_route_id(route.route_id)

    return len(trips)


@check_connection
def get_routes(country, city=None, area=None, street=None):
    routes = TripsTable.get_routes(country, city, area, street)

    return routes


@check_connection
def get_user_trips(user):
    if not user:
        return

    trips = TripsTable.get_trips_by_user_id(user.user_id)

    return trips


@check_connection
def cancel_trip(trip):
    if not trip:
        return

    TripsTable.remove_trip_by_id(trip.trip_id)

    return trip.trip_id