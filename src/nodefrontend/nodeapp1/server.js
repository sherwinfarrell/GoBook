// const http = require('http')
// const rs = require('fs')
const express = require('express')
const { Kafka } = require('kafkajs')

// const Json = require('json')

const  bodyParser = require('body-parser')


const port = 3000
const app = express()

let kafkaClient = new Kafka({
    clientId: 'my-group-id',

    brokers: ['kafka_kafka_1:9093']
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

app.post('/bookTrip', async (request, response) => {
    // print(request.body)
    console.log("request came in "); 
    console.log(request.body)

    let error  = null


    data = {'route': request.body['route'], 'city': request.body['city']}


    try{
        const producer = kafkaClient.producer()

        let routeValue = request.body['route']
        let cityValue = request.body['city']
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

        await consumer.subscribe({ topic: 'Booking' }) 
        
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

    let return_data = {}
    return_data['route1']= "Carlow Route 3 Date"

    response.setHeader('Content-Type', 'application/json');     // your JSON
    if(error){
        response.send(JSON.stringify({ "Status": `Failure: ${error}` }))
    }
    else response.send(JSON.stringify({ return_data }))
  });


app.post('/getBookedTrips', async (req, res)=> {
    console.log(req.body)
    let userId = req.body['user_id']
    data = userId
    let error = null
    try{
        const producer = kafkaClient.producer()

        await producer.connect()
        await producer.send({
        topic: 'Booking',
        acks: -1,
        timeout: 30000,
        messages: [
            { value: JSON.stringify(data)},
        ],  
        })  

        await producer.disconnect()

        const consumer = kafkaClient.consumer({groupId: 'my-group-id' })
        await consumer.connect()

        await consumer.subscribe({ topic: 'Booking' }) 
        
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
    data = trip_id
    let error = null
    try{
        const producer = kafkaClient.producer()

        await producer.connect()
        await producer.send({
        topic: 'Booking',
        acks: -1,
        timeout: 30000,
        messages: [
            { value: JSON.stringify(data)},
        ],  
        })  

        await producer.disconnect()

        const consumer = kafkaClient.consumer({groupId: 'my-group-id' })
        await consumer.connect()

        await consumer.subscribe({ topic: 'Booking' }) 
        
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



app.listen(port)
  