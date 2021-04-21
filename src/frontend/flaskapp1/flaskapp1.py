from flask import Flask, render_template, redirect, url_for, request, Response
from time import sleep
import json
from json import dumps, loads
from kafka import KafkaProducer, KafkaConsumer
import logging
import time


import asyncio
import threading

print(f"In flask global level: {threading.current_thread().name}")
app = Flask(__name__)
consumer = KafkaConsumer(
            'GetBooking',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group-id',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
                    )

@app.route('/ping')
def ping():
    return 'PONG FROM APP 1', 200

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    return render_template('book.html')



@app.route('/bookTrip', methods=['GET', 'POST'])
def bookTrip():
        selectedCity = request.json['city']
        selectedRoute = request.json['route']
        selectedCountry = request.json['country']
        userid = request.json['userid']

        return_result = {}
        return_result['route'] = selectedRoute

        print("The selected Route is " + selectedRoute)
        print("The selected City is " + selectedCity)
        nested_dict = {}
        nested_dict ={'id':userid,'data':{'route': selectedRoute, 'city': selectedCity, 'user':userid, 'start_date_time': None, 'end_date_time': None}}

        error = None
        try:
            print("debug point 1")
            producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8'))
            # print("debug point 2")
            # data1['data']['route'] = selectedRoute
            # data1['data']['city'] = selectedRoute
            # data1['data']['user'] = userid
            # data1['data']['start_date_time'] = None
            # data1['data']['end_date_time'] = None
            # data1['id'] = userid

            # data1 = { 'id':userid, data:{'route': selectedRoute, 'city': selectedCity, 'user': userid, 'start_date_time': None, 'end_date_time': None}}
            
            print("debug point 3")
            # print("The data is" + data1)

            producer.send('Booking', value=nested_dict)

            
            for event in consumer:
                event_data = event.value
                if event_data['id'] == userid:
                    print(event_data, flush=True)
                    trip_id = event_data['trip_id']
                    return_result['trip_id'] = trip_id
                    return_result['city'] = selectedCity
                    return_result['country'] = selectedCountry
                    break
                print(event_data, flush=True)
            time.sleep(5)
            
        except Exception as e:
            print("There was an error " + str(e))
            error = e

        result={}
        result['return_result'] = return_result
        result['Status'] = "Success"

        if error:
            return Response(json.dumps({"Status": "There was an error: " + str(error) + " Please try again."}), mimetype='application/json', status='400')
        else :
            return Response(json.dumps(result), mimetype='application/json', status='200')


@app.route('/getBookedTrips', methods=['GET', 'POST'])
def getBookedTrips():
    print(f"Inside flask function: {threading.current_thread().name}")

    userId = request.json['user_id']
    print(request)
    error = None
    try:
        producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: dumps(x).encode('utf-8'))

        data = {'userId': userId}
        producer.send('Booking', value=data)

        consumer = KafkaConsumer(
        'UserBooking',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group-id',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
                )
        for event in consumer:
            event_data = event.value
            if event_data['userId'] == userId:
                print(event_data, flush=True)

                break
            print(event_data, flush=True)

# Do whatever you want
            
    except Exception as e:
        print("There was an error" + str(e))
        error = e
    
    return_data = {}
    return_data['route1']= "Carlow Route 3 Date"
    return_data['route2'] = "Dublin Route 4 Date"
    if error:
        return Response(json.dumps({"message": "There was an error: " + str(error) + " Please try again."}), mimetype='application/json', status='400')
    else:
        return Response(json.dumps(return_data), mimetype='application/json', status='200')




@app.route('/cancelTrip', methods=['GET', 'POST'])
def cancelTrip():
    selectedCity = request.json['city']
    selectedRoute = request.json['route']

    print("The selected route is " + selectedRoute)
    print("The selected Country is " + selectedCity)

    return render_template('book.html')

@app.route('/getRoutes', methods=['GET', 'POST'])
def getRoutes():
    # selectedCity = request.json['city']
    # selectedRoute = request.json['route']

    # print("The selected route is " + selectedRoute)
    # print("The selected Country is " + selectedCity)

    error = None
    if error:
        return Response(json.dumps({"message": "There was an error: " + str(error) + " Please try again."}), mimetype='application/json', status='400')
    else:
        return Response(json.dumps({"message": "There was no error"}), mimetype='application/json', status='200')



if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,threaded = True)