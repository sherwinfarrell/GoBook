from src.storage.trips_table import TripsTable


def book_trip(user, route, start_date_time, end_date_time):
    if not user or route:
        return

    trip = TripsTable.from_user_and_route(user, route)
    trip.start_date_time = start_date_time
    trip.end_date_time = end_date_time

    trip.write()


def get_current_route_capacity(route):
    if not route:
        return

    trips = TripsTable.get_trips_by_route_id(route.route_id)

    return len(trips)


def get_routes(country, city, area, street):
    # to be implemented
    return
    


def get_user_trips(user):
    if not user:
        return

    trips = TripsTable.get_trips_by_user_id(user.user_id)

    return trips


def cancel_trip(trip):
    if not trip:
        return

    TripsTable.remove_trip_by_id(trip.trip_id)