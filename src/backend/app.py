from flask import Flask
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json 

app = Flask(__name__)

TOPIC = "first"

@app.route('/', methods=['GET', 'POST'])
def ding():
    return {"solution": 'pinggie'}


@app.route('/ping')
def ping():
    return 'PONG', 200


def produce():
    try:
        producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'))
 
        data = {'userId': "userId"}
        producer.send('Booking', value=data)
        producer.send(topic=TOPIC, value=data)
        producer.flush()
       

def consume():
    try:
        producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'))
 
        data = {'userId': "userId"}
        producer.send('Booking', value=data)
 
        consumer = KafkaConsumer(
        'Booking',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='my-group-id',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
                )
        for event in consumer:
            event_data = event.value
            if event_data['userId'] == "userId":
                print(event_data, flush=True)
 
                break
            print(event_data, flush=True)

if __name__ == '__main__':
    app.run(debug=True)
