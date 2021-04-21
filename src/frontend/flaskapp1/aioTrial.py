from aiohttp import web 
import json 
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import logging
import time


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
    return_result['route'] = selectedRoute

    print("The selected Route is " + selectedRoute)
    print("The selected City is " + selectedCity)
    nested_dict = {}
    nested_dict ={'id':userid,'data':{'route': selectedRoute, 'city': selectedCity, 'user':userid, 'start_date_time': None, 'end_date_time': None}}
    
    

    error = None
    try:
        print("debug point 1")
        producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers='localhost:9092')
        await producer.start()
        await producer.send_and_wait("Booking", json.dumps(nested_dict).encode('utf-8'))

        print("debug point 3")
        # print("The data is" + data1)

        consumer = AIOKafkaConsumer(
        'GetBooking',
        loop=loop, bootstrap_servers='localhost:9092',
        group_id="my-group-id")

        async for msg in consumer:
            event_data = msg.value
            event_data =json.loads(event_data)
            if event_data['id'] == userid:
                print(event_data)
                trip_id = event_data['trip_id']
                return_result['trip_id'] = trip_id
                return_result['city'] = selectedCity
                return_result['country'] = selectedCountry
                break
        
    except Exception as e:
        print("There was an error " + str(e))
        error = e

    result={}
    result['return_result'] = return_result
    result['Status'] = "Success"

    if error:
        return web.Response(text=json.dumps({"Status": "There was and Error" + str(error)}), status = 201)
    else :
        return web.Response(text=json.dumps(result), status = 200)



app = web.Application()
app.router.add_post('/getRoutes', getRoutes)
app.router.add_get('/', serveIndex)
app.router.add_post('/bookTrip', bookTrip)


web.run_app(app)