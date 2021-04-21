
const express = require('express')
const { Kafka } = require('kafkajs')

// const Json = require('json')

const  bodyParser = require('body-parser')


const port = 3000
const app = express()

let kafkaClient = new Kafka({
    clientId: 'my-group-id',

    brokers: ['localhost:9092']
  })



// const client = new kafka.KafkaClient({kafkaHost: 'localhost:9092'});


app.set('view engine', 'ejs')
app.use(bodyParser.json());

app.get('/', (req, res)=>{
    console.log("server 1")
    res.render('book')
})

app.get('/which', (req, res) =>{
    res.send("This is serever 1")
})



// const server = http.createServer((req, res) => {
//     res.writeHead(200, { 'content-type': 'text/html' })
//     fs.createReadStream('index.html').pipe(res)
// })


app.post('/bookTrip', async (req, res) => {
    console.log(req.body)

    let userid = req.body['userid']
    let route = req.body['route']
    let city = req.body['city']
    let country = req.body['country']


    const consumer = kafkaClient.consumer({groupId: 'my-group-id',     readUncommitted: true })
    await consumer.connect()
        
    await consumer.subscribe({ topic: 'GetBooking', fromBeginning: false }) 

    // let error  = null
    // 'start_date_time': null, 'end_date_time': null
    
    data = {'id':userid, 'data':{'user':userid,'route':route,'city': city, 'country': country, 'start_date_time': null, 'end_date_time': null }}

    let return_result = {}
    return_result['route'] = route
    let trip_id  = null
    res.setHeader('Content-Type', 'application/json');     // your JSON


    try{




        const producer = kafkaClient.producer()
        await producer.connect()
        await producer.send({
        topic: 'Booking',
        acks: -1,
        timeout: 30000,
        messages: [
            { value: JSON.stringify(data) },
        ],  
        })  
        await producer.disconnect()


        
        await consumer.run({
            eachMessage: async ({ topic, partition, message }) => {
                console.log({
                    key: message.key,
                    value: message.value.toString(),
                    headers: message.headers,
                })
                
                let value = message.value.toString()
                value = JSON.parse(value)
                console.log(value)
                if(userid.toString() == value['id']){
                    console.log("This happened")
                    trip_id = value['trip_id']
                    return_result['trip_id'] = trip_id
                    return_result['city'] = city
                    return_result['country'] = country

                    if(trip_id){
                        res.send(JSON.stringify({ return_result,"Status": "Success" }))
                    }
                    else {
                     res.send(JSON.stringify({ "Status": `Failure: Booking was unsuccessfull` }))
                    }
                    consumer.disconnect()
                }
                console.log("I am here ..............................................")

            },
        })


    }catch (error) {

        console.error("There is an error" + error);

        if(error){
    
            res.send(JSON.stringify({ "Status": `Failure: ${error}` }))
        }
        consumer.disconnect()


    }  
  });





app.post('/getBookedTrips', async (req, res)=> {
    // console.log(req.body)
    let userid = req.body['userid']

    data = {'id' : userid, 'data':{'user':userid}}
    let error = null
    res.setHeader('Content-Type', 'application/json');     // your JSON
    return_result = {}


    const userBookingConsumer = kafkaClient.consumer({groupId: 'my-group-id',   readUncommitted: true  })

    try{
        await userBookingConsumer.connect()
        await userBookingConsumer.subscribe({ topic: 'GetUserBookings', fromBeginning: false })  

        const producer = kafkaClient.producer()

        await producer.connect()
        await producer.send({
        topic: 'UserBookings',
        acks: -1,
        timeout: 30000,
        messages: [
            { value: JSON.stringify(data)},
        ],  
        })  

        await producer.disconnect()


        
        await userBookingConsumer.run({
            eachMessage: async ({ topic, partition, message }) => {
                console.log({
                    key: message.key,
                    value: message.value,
                    headers: message.headers,
                    message: message
                })

                let value = message.value.toString()
                value = JSON.parse(value)
                console.log(value)
                if(userid.toString() == value['id']){
                    console.log("This happened")
                    console.log(value)
                    trips = value['trips']
                    if(Object.keys(trips).length !== 0){
                    Object.keys(trips).forEach((tripKey)=>{
                        return_result[key] = trips[key]
                    })                        
      

                        res.send(JSON.stringify({ return_result,"Status": "Success" }))

                    }
                    else {
                     res.send(JSON.stringify({ "Status": 'Failure: There are no trips' }))
                    }
                    userBookingConsumer.disconnect()

                }
                console.log("I am here ..............................................")
            },
        })


    }catch (e) {
        console.error(e);
        error= e
    }

    if(error){
        res.send(JSON.stringify({ "Status": `Failure: ${error}` }))
        userBookingConsumer.disconnect()
    }
  
})



const cancellationConsumer = kafkaClient.consumer({groupId: 'my-group-id' })
cancellationConsumer.connect()

cancellationConsumer.subscribe({ topic: 'GetCancellation' }) 

app.post('/cancelTrip', async (req, res)=> {
    console.log(req.body)
    let trip_id = req.body['trip_id']
    let userid = req.body['userid']

    data = { 'id': userid, 'data': {'trip_id': trip_id}}
    let error = null
    try{
        const producer = kafkaClient.producer()

        await producer.connect()
        await producer.send({
        topic: 'Cancellation',
        acks: -1,
        timeout: 30000,
        messages: [
            { value: JSON.stringify(data)},
        ],  
        })  

        await producer.disconnect()


        
        await cancellationConsumer.run({
            eachMessage: async ({ topic, partition, message }) => {
                console.log({
                    key: message.key.toString(),
                    value: message.value.toString(),
                    headers: message.headers,
                })
            },
        })

        // await cancellationConsumer.disconnect()

    }catch (e) {

        console.error(e);

        error= e

    }

    res.setHeader('Content-Type', 'application/json');     // your JSON

    if(error){
        res.send(JSON.stringify({ "Status": `Failure: ${error}` }))
    }
    else res.send(JSON.stringify({ "Status": "Success" }))
})

const routesConsumer = kafkaClient.consumer({groupId: 'my-group-id' })
routesConsumer.connect()

routesConsumer.subscribe({ topic: 'GetRoutes' }) 
app.post('/getRoutes', async (req, res)=> {
    console.log(req.body)
    // let country = req.body['country']
    let city = req.body['city']
    let userid = req.body['userid']


    data = {'id': userid, 'data': {'country':'Ireland', 'city': city}}

    let error = null
    try{
        const producer = kafkaClient.producer()

        await producer.connect()
        await producer.send({
        topic: 'Routes',
        acks: -1,
        timeout: 30000,
        messages: [
            { value: JSON.stringify(data)},
        ],  
        })  

        await producer.disconnect()


        
        await routesConsumer.run({
            eachMessage: async ({ topic, partition, message }) => {
                console.log({
                    key: message.key.toString(),
                    value: message.value.toString(),
                    headers: message.headers,
                }, "This is the message I have received back -----------------------")
            },
        })

        routesConsumer.pause()

    }catch (e) {

        console.error(e);

        error= e

    }

    res.setHeader('Content-Type', 'application/json');     // your JSON

    if(error){
        res.send(JSON.stringify({ "Status": `Failure: ${error}` }))
    }
    else res.send(JSON.stringify({ "Status": "Success" }))
})



app.listen(port)
  