import json

import pika

params = pika.URLParameters('amqps://lomrcqnm:NdMxUBJz2NR7d2tnT9oGmIhGb-kcffi7@chimpanzee.rmq.cloudamqp.com/lomrcqnm')
connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
