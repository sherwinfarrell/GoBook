from config import ddb_config

from models.exceptions import RouteAlreadyBooked
from storage.models.trips_table import TripsTable
from storage.decorators import check_connection
import logging
 
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | [%(levelname)s] : %(name)s | %(lineno)d | %(module)s | %(filename)s | %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logFilePath = "app.log"
file_handler = logging.FileHandler(logFilePath)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

@check_connection
def book_trip(user, route, start_date_time, end_date_time):
    if not user or not route:
        logger.info("Storage Client ========> user is none")
        return None

    logger.info("Storage Client ========> user is not none")
    trip = TripsTable.from_user_and_route(user, route)
    trip.start_date_time = start_date_time
    trip.end_date_time = end_date_time

    logger.info(" Storage Client ========>  trip id is " + trip.trip_id)
    try:
        user_trips = get_user_trips(user)
        for t in user_trips:
            logger.info('user got trip ' + t.trip_id + ' ' + t.route_id)
            if t.route_id == route.route_id:
                raise RouteAlreadyBooked
    except RouteAlreadyBooked:
        logger.exception("Storage Client ========> Route already booked")
        return None

    try:
        trip.write()
    except Exception:
        logger.exception("Storage Client ========>   Trip.write worked")
        return None

    logger.info("Storage Client ========>   Returning Something")
    return trip.to_trip()


def get_current_route_capacity(route):
    if not route:
        logger.info("It thinks its not a route *****************************************************************************")
        return None
    try:
        trips = TripsTable.get_trips_by_route_id(route.route_id)
        # except Exception as e:
        logger.info("There was an error with route capacity " )
        logger.info(trips)

        return len(trips)
    except: 
        logger.exception("There was an error with checking the route capacity")
        return -1


@check_connection
def get_routes(country, city=None, area=None, street=None):
    try:
        routes = TripsTable.get_routes(country, city, area, street)
    except Exception:
        logger.exception("There was an error with booking the route")
        return None

    return routes


@check_connection
def get_user_trips(user):
    if not user:
        return None
    
    try:
        trips = TripsTable.get_trips_by_user_id(user.user_id)
    except Exception:
        logger.exception("There was an error getting the user trips")
        return None

    return trips


@check_connection
def cancel_trip(trip):
    if not trip:
        return None

    try:
        TripsTable.remove_trip_by_id(trip.trip_id)
    except Exception:
        logger.exception("There was an error cancelling the trip")
        return None
    
    return 'done'

@check_connection
def truncate_table():
    logger.info('cleaning table')
    TripsTable.truncate_table()
    logger.info('finished cleaning')
