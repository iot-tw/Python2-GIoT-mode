#!/usr/bin/env python
# revceive.py
# This is for rabbitMQ connect
import pika
credentials = pika.PlainCredentials('cloudservice', '9Hxp5xi7')
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='52.196.119.165',
        port=5671,
        virtual_host='cloudservice',
        credentials=credentials,
        ssl=True))
channel = connection.channel()

channel.queue_declare(queue='hello')

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)


channel.basic_consume(callback,
                      queue='df.cloudservice.uldata',
                      no_ack=True)

channel.start_consuming()
