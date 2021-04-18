from flask import Flask, render_template, redirect, url_for, request, Response
from time import sleep
import json
from json import dumps, loads
from kafka import KafkaProducer, KafkaConsumer
import logging


import asyncio
import threading

print(f"In flask global level: {threading.current_thread().name}")
app = Flask(__name__)


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

        print("The selected Route is " + selectedRoute)
        print("The selected City is " + selectedCity)

        print("Reached here")

        try:
            producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8'))

            data = {'route': selectedRoute, 'city': selectedCity}
            producer.send('Booking', value=data)
            
            
            
        except Exception as e:
            print("There was an error")
            # print("The following error occured: " + e)


        # data = {'city': selectedCity, 'route': selectedRoute}

        # producer.send('Booking', value=data)

        return "Successful"


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
        'Booking',
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
        print("There was an error {error1}".format(error1 = str(e)))
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


if __name__ == '__main__':
    app.run('0.0.0.0',debug=True, threaded = True)