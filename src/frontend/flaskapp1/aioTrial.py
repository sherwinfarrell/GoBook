from aiohttp import web 
import json 
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import logging
import time
import asyncio


loop = asyncio.get_event_loop()


async def getRoutes(request):
    body = await request.json()
    print(body)
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj), status = 200)


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
    nested_dict ={'id':userid,'data':{'route': selectedRoute,'country':selectedCountry, 'city': selectedCity, 'user':userid, 'start_date_time': None, 'end_date_time': None}}
    
    

    error = None
    try:
        print("debug point 1")
        producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers='localhost:9092')
        await producer.start()
        await producer.send_and_wait("Booking", json.dumps(nested_dict).encode('utf-8'))
        await producer.stop()


        print("debug point 3")
        # print("The data is" + data1)

        consumer = AIOKafkaConsumer(
        'GetBooking',
        loop=loop, bootstrap_servers='localhost:9092',
        group_id="my-group-id",
        auto_offset_reset="latest",
        enable_auto_commit=True,)
        
        await consumer.start()

        async for msg in consumer:
            event_data = msg.value
            print(event_data)
            event_data =json.loads(event_data)
            if event_data['id'] == userid:
                # print(event_data)
                if 'trip_id' in event_data:
                    trip_id = event_data['trip_id']
                    return_result['trip_id'] = trip_id
                    return_result['city'] = selectedCity
                    return_result['country'] = selectedCountry
                    return_result['route'] = selectedRoute

                    await consumer.commit()
                break
        
    except Exception as e:
        print("There was an error " + str(e))
        error = e
    
    finally: 
        await consumer.stop()

    result={}
    result['return_result'] = return_result
    result['Status'] = "Success"

    

    if error:
        return web.Response(text=json.dumps({"Status": "There was and Error: " + str(error)}), status = 201)
    if result['return_result'] :
        return web.Response(text=json.dumps(result), status = 200)
    else :
        return web.Response(text=json.dumps({"Status": "You have already made this booking"}), status = 201)



async def getBookedTrips(request):
    body = await request.json()


    userid = body['userid']
    

    return_result = {}

    
    nested_dict = {}
    nested_dict ={'id':userid,'data':{ 'user':userid}}
    
    

    error = None
    try:
        print("debug point 1")
        producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers='localhost:9092')
        await producer.start()
        await producer.send_and_wait("UserBookings", json.dumps(nested_dict).encode('utf-8'))
        await producer.stop()


        print("debug point 3")
        # print("The data is" + data1)

        consumer = AIOKafkaConsumer(
        'GetUserBookings',
        loop=loop, bootstrap_servers='localhost:9092',
        group_id="my-group-id",
        auto_offset_reset="latest",
        enable_auto_commit=True,)
        
        await consumer.start()

        async for msg in consumer:
            event_data = msg.value
            print(event_data)
            event_data =json.loads(event_data)
            if event_data['id'] == userid:
                # print(event_data)
                if 'trips' in event_data:
                    trips = event_data['trips']
                    for trip in trips:
                        return_result['trip'] = trips[trip]
                        

                    await consumer.commit()
                break
        
    except Exception as e:
        print("There was an error " + str(e))
        error = e
    
    finally: 
        await consumer.stop()

    result={}
    result['return_result'] = return_result
    result['Status'] = "Success"

    

    if error:
        return web.Response(text=json.dumps({"Status": "There was and Error: " + str(error)}), status = 201)
    if result['return_result'] :
        return web.Response(text=json.dumps(result), status = 200)
    else :
        return web.Response(text=json.dumps({"Status": "This user has no booked trips"}), status = 201)

async def cancelTrip(request):
    body = await request.json()


    userid = body['userid']
    trip_id = body['trip_id']
    

    return_result = {}

    # print("The selected Route is " + selectedRoute)
    # print("The selected City is " + selectedCity)
    nested_dict = {}
    nested_dict ={'id':userid, 'data': {'trip_id': trip_id}}
    
    

    error = None
    try:
        print("debug point 1")
        producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers='localhost:9092')
        await producer.start()
        await producer.send_and_wait("Cancellation", json.dumps(nested_dict).encode('utf-8'))
        await producer.stop()


        print("debug point 3")
        # print("The data is" + data1)

        consumer = AIOKafkaConsumer(
        'GetCancellation',
        loop=loop, bootstrap_servers='localhost:9092',
        group_id="my-group-id",
        auto_offset_reset="latest",
        enable_auto_commit=True,)
        
        await consumer.start()

        async for msg in consumer:
            event_data = msg.value
            print(event_data)
            event_data =json.loads(event_data)
            if event_data['id'] == userid:
                if 'is_cancelled' in event_data:
                    print(event_data['is_cancelled'])
                    return_result['is_called'] = event_data['is_cancelled']
                    await consumer.commit()
                break
        
    except Exception as e:
        print("There was an error " + str(e))
        error = e
    
    finally: 
        await consumer.stop()

    result={}
    result['return_result'] = return_result
    result['Status'] = "Success"

    

    if error:
        return web.Response(text=json.dumps({"Status": "There was and Error: " + str(error)}), status = 201)
    if result['return_result'] :
        return web.Response(text=json.dumps(result), status = 200)
    else :
        return web.Response(text=json.dumps({"Status": "There was a problem cancelling the trip"}), status = 201)



app = web.Application()
app.router.add_post('/getRoutes', getRoutes)
app.router.add_get('/', serveIndex)
app.router.add_post('/bookTrip', bookTrip)
app.router.add_post('/cancelTrip', cancelTrip)
app.router.add_post('/getBookedTrips', getBookedTrips)

web.run_app(app)