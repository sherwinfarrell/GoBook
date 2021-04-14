from flask import Flask, render_template, redirect, url_for, request
from time import sleep
from json import dumps
from kafka import KafkaProducer
import logging



app = Flask(__name__)


@app.route('/ping')
def ping():
    return 'PONG FROM APP 2', 200

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
            bootstrap_servers=['localhost:9093'],
            value_serializer=lambda x: dumps(x).encode('utf-8'))

            data = {'route': selectedRoute, 'city': selectedCity}
            producer.send('Booking', value=data)
        except Exception as e:
            print("There was an error")
            # print("The following error occured: " + e)


        # data = {'city': selectedCity, 'route': selectedRoute}

        # producer.send('Booking', value=data)

        return "Successful"






@app.route('/cancelTrip', methods=['GET', 'POST'])
def cancelTrip():
    selectedCity = request.json['city']
    selectedRoute = request.json['route']

    print("The selected route is " + selectedRoute)
    print("The selected Country is " + selectedCity)

    return render_template('book.html')


if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)