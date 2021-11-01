#!/usr/bin/python3
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tempfile #random file generator
import uuid
#import getpass

import pika
import uuid
import io

import cgi
import urllib
from urllib.error import URLError, HTTPError
import urllib.request
import PIL
from PIL import Image

import cgitb
import json

import BreedConst

class DogsClient( object ):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=n)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

def print_json(resonse):
  json = resonse.replace('\'','\"')
  print(json)



cgitb.enable() #output err to web


print('Content-Type: text/plain')
print('')

form = cgi.FieldStorage()


result = {"ErrCode": 0, "ErrReason": "", "Size": 0, "Dogs": []}

if 'userfile' not in form:
    result['ErrCode'] = 1001
    result['ErrReason'] = "Post error. No userfile set"
    print_json(str(result))
    raise SystemExit(0)

fileitem = form['userfile']

try:
    img = Image.open(fileitem.file)
except  FileNotFoundError:  # so be it but exception inpossible, raised in the HTTPError above if url not open. error code ENOENT - 2
    result['ErrCode'] = 1002
    result['ErrReason'] = "Can't find image location"
    print_json(str(result))
    raise SystemExit(0)
except PIL.UnidentifiedImageError:
    result['ErrCode'] = 1003
    result['ErrReason'] = 'The image cannot be opened and identified'
    print_json(str(result))
    raise SystemExit(0)
except Exception:
    result['ErrCode'] = 1004
    result['ErrReason'] = 'Unknown image open error'
    print_json(str(result))
    raise SystemExit(0)

img = img.resize((224, 224))


if 'undefined_breed' in  form:
    undefinedBreed = form.getvalue('undefined_breed')

    UNDEFINED_BREEDS_DATA_DIR = "/var/www/html/DogBreeds/undefined_breeds/" 
    breedDir = UNDEFINED_BREEDS_DATA_DIR + undefinedBreed + '/'

    try:
        if not os.path.exists(breedDir):
           os.makedirs(breedDir)
        uuid_str = str(uuid.uuid4())
        fileName = 'img_%s.png' % uuid_str
        img.save(breedDir + fileName)
    except:
        result['ErrCode'] = 1005
        result['ErrReason'] = 'Cannot save image'
        print(result)

    raise SystemExit(0)



dogs = DogsClient()

# print(" [x] Requesting .....")

img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='PNG')
img_byte_arr = img_byte_arr.getvalue()

response = dogs.call(img_byte_arr)
print_json(response.decode()) #remove b
