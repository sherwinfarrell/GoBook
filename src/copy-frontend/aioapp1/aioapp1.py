from aiohttp import web
import json
import logging
import time
import asyncio

from models.route import Route
from models.user import User
from models.trip import Trip
from storage.storage_client import book_trip, get_user_trips, get_routes, cancel_trip, get_current_route_capacity, truncate_table
import threading, time
import numpy as np



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

loop = asyncio.get_event_loop()


async def getServerNum(request):
    return web.Response(text="This is server 1", status=200)


async def getRoutes(request):
    body = await request.json()
    logger.info(body)
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj), status=200)


async def serveIndex(request):
    return web.FileResponse('templates/book.html')


async def bookTrip(request):
    body = await request.json()

    selectedCity = body['city']
    selectedRoute = body['route']
    selectedCountry = body['country']
    userid = body['userid']
    return_result = {}

    logger.info("The selected Route is " + selectedRoute)
    logger.info("The selected City is " + selectedCity)
    nested_dict = {}
    nested_dict = {
        'id': userid,
        'data': {
            'route': selectedRoute,
            'country': selectedCountry,
            'city': selectedCity,
            'user': userid,
            'start_date_time': None,
            'end_date_time': None
        }
    }

    result = {}

    error = None
    try:
        user = User(userid, "test")
        route = Route(selectedRoute, selectedCountry, selectedCity, "test","test")
        route_capacity = get_current_route_capacity(route)
        logger.info( "Route capacity that we got back is ==================================================> "+ str(route_capacity))
        if route_capacity > -1:
            if route_capacity < 5:
                logger.info("the user is " + user.user_id)
                logger.info("the rotue is " + route.route_id)
                trip = book_trip(user, route, "test", "test")
                if trip:
                    logger.info("It got the trip yes ------------------------------------------------------------")
                    return_result["trip_id"] = trip.trip_id
                    return_result['city'] = selectedCity
                    return_result['country'] = selectedCountry
                    return_result['route'] = selectedRoute
                else:
                    logger.info("Booking is full")
                    error = "Booking is full"
                    return_result = None

            else:
                logger.info("booking seems to be full")
                error = "Booking is Full"
                return_result['trip_id'] = None
        else:
            logger.info("There is an error with route capacity")
            error = "There is an error with route capacity, Try again "
            return_result['trip_id'] = None

    except Exception as e:
        logger.exception("There was an error " + str(e))
        error = e

    result['return_result'] = return_result
    result['Status'] = "Success"

    logger.info("The data that is being send back is ")
    logger.info(result['return_result'])

    if np.random.rand() <= 0.4:
        logger.info("There was a network failure")
        return web.Response(text=json.dumps({"Status": "There was an unkown error"}), status = 400)
        

    if error:
        return web.Response(text=json.dumps({"Status": "There was and Error: " + str(error)}),status=201)
    if result['return_result']:
        return web.Response(text=json.dumps(result), status=200)
    else:
        return web.Response(text=json.dumps({"Status": "You have already made this booking"}),status=201)


async def getBookedTrips(request):
    body = await request.json()
    userid = body['userid']

    return_result = {}

    nested_dict = {}
    nested_dict = {'id': userid, 'data': {'user': userid}}

    error = None
    try:
        trips = get_user_trips(User(userid, "test"))
        if trips:
            logger.info("There are the trips")
            logger.info(trips)
            for trip in trips:
                logger.info("This is the trip")
                logger.info(trip.trip_id)
                return_result[ trip.trip_id] = trip.country + "," + trip.city + "," + trip.route_id
        else:
            error = "The no trips for the user"
            return_result = None

    except Exception as e:
        logger.exception("There was an error " + str(e))
        error = e

    result = {}
    result['return_result'] = return_result
    result["handler"] = "app1"
    result['Status'] = "Success"

    logger.info("The data that is being send back is ")
    logger.info(result['return_result'])
    logger.info(return_result)

    if error:
        return web.Response(text=json.dumps({"Status": "There was and Error: " + str(error)}), status=201)
    if result['return_result']:
        return web.Response(text=json.dumps(result), status=200)
    else:
        return web.Response(text=json.dumps(
            {"Status": "This user has no booked trips"}), status=201)


async def cancelTrip(request):
    body = await request.json()

    userid = body['userid']
    trip_id = body['trip_id']
    return_result = {}

    # logger.info("The selected Route is " + selectedRoute)
    # logger.info("The selected City is " + selectedCity)
    nested_dict = {}
    nested_dict = {'id': userid, 'data': {'tripid': trip_id}}

    error = None
    try:
        logger.info("debug point 1")
        trip = Trip(trip_id, "test", "test", "test", "test", "test", "test","test", "test", "test", "test")
        is_cancelled = cancel_trip(trip)
        if is_cancelled:
            return_result['is_cancelled'] = is_cancelled
            logger.info("Cancelled trip successful")
        else:
            error = "There was an error cancelling this trip"
            logger.info("There was an error cancelling")

    except Exception as e:
        logger.exception("There was an error in exception " + str(e))
        error = e
        
    result = {}
    result['return_result'] = return_result
    result['Status'] = "Success"

    
    if error:
        return web.Response(text=json.dumps(  {"Status": "There was and Error: " + str(error)}),  status=201)
    if result['return_result']:
        return web.Response(text=json.dumps(result), status=200)
    else:
        return web.Response(text=json.dumps( {"Status": "There was a problem cancelling the trip"}),status=201)


app = web.Application()
app.router.add_post('/getRoutes', getRoutes)
app.router.add_get('/', serveIndex)
app.router.add_post('/bookTrip', bookTrip)
app.router.add_post('/cancelTrip', cancelTrip)
app.router.add_post('/getBookedTrips', getBookedTrips)
app.router.add_get('/getServerNum', getServerNum)
web.run_app(app, port=5000)