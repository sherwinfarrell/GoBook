
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


    let error  = null
    // 'start_date_time': null, 'end_date_time': null
    
    data = {'id':userid, 'data':{'user':userid,'route':route,'start_date_time': null, 'end_date_time': null }}


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

        const consumer = kafkaClient.consumer({groupId: 'my-group-id' })
        await consumer.connect()

        await consumer.subscribe({ topic: 'GetBooking' }) 
        
        await consumer.run({
            eachMessage: async ({ topic, partition, message }) => {
                console.log({
                    key: message.key,
                    value: message.value,
                    headers: message.headers,
                })

            },
        })

        await consumer.disconnect()

    }catch (e) {

        console.error(e);

        error= e

    }

    let return_data = {}
    return_data['route1']= "Carlow Route 3 Date"

    res.setHeader('Content-Type', 'application/json');     // your JSON
    if(error){
        res.send(JSON.stringify({ "Status": `Failure: ${error}` }))
    }
    else res.send(JSON.stringify({ return_data }))
  });


app.post('/getBookedTrips', async (req, res)=> {
    console.log(req.body)
    let userid = req.body['user_id']

    data = {'id' : userid, 'data':{'user':userid}}
    let error = null
    try{
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

        const consumer = kafkaClient.consumer({groupId: 'my-group-id' })
        await consumer.connect()

        await consumer.subscribe({ topic: 'GetUserBookings' }) 
        
        await consumer.run({
            eachMessage: async ({ topic, partition, message }) => {
                console.log({
                    key: message.key,
                    value: message.value,
                    headers: message.headers,
                    message: message
                })
            },
        })

        // await consumer.disconnect()

    }catch (e) {

        console.error(e);

        error= e

    }

    let return_data = {}
    return_data['route1']= "Carlow Route 3 Date"
    return_data['route2'] = "Dublin Route 4 Date"

    res.setHeader('Content-Type', 'application/json');     // your JSON

    if(error){
        res.send(JSON.stringify({ "Status": `Failure: ${error}` }))
    }
    else res.send(JSON.stringify({ return_data }))
})


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

        const consumer = kafkaClient.consumer({groupId: 'my-group-id' })
        await consumer.connect()

        await consumer.subscribe({ topic: 'GetCancellation' }) 
        
        await consumer.run({
            eachMessage: async ({ topic, partition, message }) => {
                console.log({
                    key: message.key.toString(),
                    value: message.value.toString(),
                    headers: message.headers,
                })
            },
        })

        await consumer.disconnect()

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

        const consumer = kafkaClient.consumer({groupId: 'my-group-id' })
        await consumer.connect()

        await consumer.subscribe({ topic: 'GetRoutes' }) 
        
        await consumer.run({
            eachMessage: async ({ topic, partition, message }) => {
                console.log({
                    key: message.key.toString(),
                    value: message.value.toString(),
                    headers: message.headers,
                }, "This is the message I have received back -----------------------")
            },
        })

        // await consumer.disconnect()

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
  