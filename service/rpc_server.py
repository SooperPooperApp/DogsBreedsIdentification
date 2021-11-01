#!/usr/bin/python3
import pika

import BreedModel
from PIL import Image
import io

import time


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

model = BreedModel.BreedModel()
model.loadModel("breeds_model126.h5")
#model.loadBreed("norm_classes.txt")
model.loadRateBreed("norm_class_rate2.csv")

def predict(img):
    return model.predict(img)

def on_request(ch, method, props, body):

    print("Processing.....")

    start_time = time.time()
    img = Image.open(io.BytesIO(body))

    result = predict(img)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(result))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(time.time() - start_time)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
