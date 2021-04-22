from flask import Flask
from flask.wrappers import Response
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import datetime
from pykafka import KafkaClient
from pykafka.common import OffsetType
# from frontend.flaskapp1.flaskapp1 import bookTrip
from models.route import Route
from models.user import User
from models.trip import Trip
from storage.storage_client import book_trip, get_user_trips, get_routes, cancel_trip
import threading, time

app = Flask(__name__)

TOPIC = "first"
count = 0 
# producerG = None
prod = KafkaProducer(bootstrap_servers=['localhost:9092'],
                     value_serializer=lambda x: json.dumps(x).encode('utf-8'))

client = KafkaClient(hosts="localhost:9092", )


class Consumer(threading.Thread):
    def __init__(self, topic):
        self.topic = topic
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.count = 0

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(self.topic, bootstrap_servers='localhost:9092',
                                 auto_offset_reset='latest',
                                 enable_auto_commit=True,
                                 group_id="my-group-id",
                                 consumer_timeout_ms=1000)
        consumer.commit()
        print(self.topic)
        print("It has created a consumer")
        # consumer.poll()
        # consumer.seek_to_end()

        # consumer.subscribe([self.topic])

        while not self.stop_event.is_set():
            for message in consumer:
                data = {}
                print(message)
                x = json.loads(message.value.decode())
                

                if self.topic == "Routes":
                    # data["result"] = get_routes(x["data"]["country"],
                                                # x["data"]["city"], "test", "test")
                    print("The Data that is recieved is " + x)
                    # prod.send("GetRoutes", value=data)

                elif self.topic == "Booking":
                    self.count = self.count +1
                    print(self.count)
                    for i in x:
                        print(i,x[i])

                    # print("Sending Data: " + x["data"]["user"] + "  " + x["data"]["route"] + " " +x["data"]["city"])
                    user = User(x["data"]["user"], "test")
                    
                    route = Route( x["data"]["route"],x["data"]["country"], x["data"]["city"], "test", "test")
                    print()
                    print("The route object that was just created is *********** \n" )
                    print(route.to_string())
                    print()
                    print("The route object that was just created is \n")
                    print(user.user_id)
                    print(user.username)


                    trip = book_trip(
                        user,
                        route,
                        "test", "test"
                    )
                    
                    
                    data["id"] = x["id"]
                    if(trip):
                        print("The Trip that we got back from calling book_trip is " )
                        print(trip.to_string())
                        print("This is the trip id "+ trip.trip_id)
                        print("This is the trip book_date_time "+ str(trip.book_date_time))
                        print("This is the trip start_date_time "+ str(trip.start_date_time))
                        print("This is the trip end_date_time "+ str(trip.end_date_time))
                        print("This is the trip route_id "+ trip.route_id)
                        print("This is the trip country "+ trip.country)
                        print("This is the trip city "+ trip.city)
                        print("This is the trip area "+ trip.area)
                        print("This is the trip street "+ trip.street)
                        print("This is the trip user_id "+ trip.user_id)
                        print("This is the trip username "+ trip.username)
                        data["trip_id"] = trip.trip_id
                        
                    print("The data to be sent back is ------------> ", data)
                    prod.send("GetBooking", value=data)


                elif self.topic == "UserBookings":
                    print("Sending Data  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", x["data"]["user"])

                    trips = get_user_trips( User(x["data"]["user"], "test"))
                    data["id"] = x["id"]

                    # print("The Trips that I got back is ********************************")
                    # print(trips)
                    data["trips"]= {}
                    for i, trip in enumerate(trips):
                        print(trip.trip_id)
                        # print("id is ", i)
                        data["trips"][ trip.trip_id] =trip.country + "," + trip.city +"," + trip.route_id
                        print(trip)
                    print("Data that is being sent back is **************************************")
                    print(data)
                    
                    prod.send("GetUserBookings", value=data)


                elif self.topic == "cancel":
                    trip = Trip(x["data"]["tripid"], "test", "test", "test", "test", "test", "test", "test", "test", "test", "test")
                    is_cancelled = cancel_trip(trip )
                    data["id"] = x["id"]
                    print(is_cancelled)
                    if is_cancelled:
                        data['is_cancelled'] = is_cancelled
                    print("Data that is being sent back is ************************************************************")
                    print(data)
                    prod.send("GetCancellation", value=data)


                if self.stop_event.is_set():
                    break
        consumer.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    return "welcome to back end server"


@app.route('/stream/<cityName>')
def sendMessage(cityName):
    def events():
        for i in client.topics["Booking"].get_simple_consumer(
                auto_offset_reset=OffsetType.LATEST,
                auto_commit_enable=True,
                auto_commit_interval_ms=2000,
                queued_max_messages=1,
                reset_offset_on_start=True):
            #what ever calculations i have to do. then i forwad it some where.
            x = json.loads(i.value.decode())
            print(x)
            data = {}
            if x["querry"] == "getRoutes":
                data["result"] = get_routes(x["data"]["country"])
                data["id"] = x["id"]
                if x["id"] == cityName:
                    yield f"id: someid\nevent: response\ndata: {x}\n\n"
                #vuser, route, start_date_time, end_date_time
            # x["hello"] = datetime.datetime.now()
            # if x["so"] == cityName:
            # calculate things
            # prod.send(x["userId"], value=x)

    return Response(
        events(),
        mimetype="text/event-stream",
    )


@app.route('/prod/<ide>', methods=['GET', 'POST'])
def prodExample(ide):
    data = {"so": ide}
    prod.send('Booking', value=data)
    return {"status": 800200}


if __name__ == '__main__':
    # produce()
    # consume()
    # admin = KafkaAdminClient(bootstrap_servers='localhost:9092')

    # topic = NewTopic(name='my-topic',
    #                     num_partitions=1,
    #                     replication_factor=1)
    # admin.create_topics([topic])
    # client = KafkaClient(hosts="localhost:9092")
    #    KAFKA_CREATE_TOPICS: "Booking:1:3,GetBooking:1:3,Cancellation:1:3,GetCancellation:1:3,
    # UserBookings:1:3,GetUserBookings:1:3,Routes:1:3,GetRoutes:1:3"

    getRoute = Consumer(topic="Routes")
    bookTrip = Consumer(topic="Booking")
    getUserTrips = Consumer(topic="UserBookings")
    cancelTrip = Consumer(topic="Cancellation")
    getRoute.start()
    bookTrip.start()
    getUserTrips.start()
    cancelTrip.start()
    app.run(debug=True)
