import json
import pika
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from products.models import Product
from products.producer import publish
from products.serializers import ProductSerializer

params = pika.URLParameters('amqps://lomrcqnm:NdMxUBJz2NR7d2tnT9oGmIhGb-kcffi7@chimpanzee.rmq.cloudamqp.com/lomrcqnm')
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Recieved in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    serializer = ProductSerializer(product)
    product.likes = product.likes + 1
    product.save()
    publish('product-liked', serializer.data)
    print('Product likes increased')


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
