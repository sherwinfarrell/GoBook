from aiohttp import web
import json
import logging
import time
import asyncio
from aiohttp_cache import (  # noqa
    setup_cache, cache, AvailableKeys,
)
from models.route import Route
from models.user import User
from models.trip import Trip
from storage.storage_client import book_trip, get_user_trips, get_routes, cancel_trip, get_current_route_capacity, truncate_table
import threading, time

loop = asyncio.get_event_loop()
custom_cache_key = (AvailableKeys.method, AvailableKeys.json)


async def getServerNum(request):
    return web.Response(text="This is server 2", status=200)


async def getRoutes(request):
    body = await request.json()
    print(body)
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

    print("The selected Route is " + selectedRoute)
    print("The selected City is " + selectedCity)
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
        print( "Route capacity that we got back is ==================================================> "+ str(route_capacity))
        if route_capacity > -1:
            if route_capacity < 5:
                print("the user is ", user.user_id)
                print("the rotue is ", route.route_id)
                trip = book_trip(user, route, "test", "test")
                if trip:
                    print("It got the trip yes ------------------------------------------------------------")
                    return_result["trip_id"] = trip.trip_id
                    return_result['city'] = selectedCity
                    return_result['country'] = selectedCountry
                    return_result['route'] = selectedRoute
                else:
                    print("Booking is full")
                    error = "Booking is full"
                    return_result = None

            else:
                print("booking seems to be full")
                error = "Booking is Full"
                return_result['trip_id'] = None
        else:
            print("There is an error with route capacity")
            error = "There is an error with route capacity, Try again "
            return_result['trip_id'] = None

    except Exception as e:
        print("There was an error " + str(e))
        error = e

    result['return_result'] = return_result
    result['Status'] = "Success"

    print("The data that is being send back is ")
    print(result['return_result'])

    if error:
        return web.Response(text=json.dumps({"Status": "There was and Error: " + str(error)}),status=201)
    if result['return_result']:
        return web.Response(text=json.dumps(result), status=200)
    else:
        return web.Response(text=json.dumps({"Status": "You have already made this booking"}),status=201)


@cache(
    expires=1 * 24 * 3600,  # in seconds
    unless=False,
)
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
            print("There are the trips")
            print(trips)
            for trip in trips:
                print("This is the trip")
                print(trip.trip_id)
                return_result[ trip.trip_id] = trip.country + "," + trip.city + "," + trip.route_id
        else:
            error = "The no trips for the user"
            return_result = None

    except Exception as e:
        print("There was an error " + str(e))
        error = e

    result = {}
    result['return_result'] = return_result
    result['Status'] = "Success"

    print("The data that is being send back is ")
    print(result['return_result'])
    print(return_result)

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

    # print("The selected Route is " + selectedRoute)
    # print("The selected City is " + selectedCity)
    nested_dict = {}
    nested_dict = {'id': userid, 'data': {'tripid': trip_id}}

    error = None
    try:
        print("debug point 1")
        trip = Trip(trip_id, "test", "test", "test", "test", "test", "test","test", "test", "test", "test")
        is_cancelled = cancel_trip(trip)
        if is_cancelled:
            return_result['is_cancelled'] = is_cancelled
            print("Cancelled trip successful")
        else:
            error = "There was an error cancelling this trip"
            print("There was an error cancelling")

    except Exception as e:
        print("There was an error in exception " + str(e))
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
setup_cache(app, key_pattern=custom_cache_key)

web.run_app(app, port=5000)