import pika
from pika import DeliveryMode

import logging
import argparse
import json

logging.basicConfig(level=logging.DEBUG)

def publish_new_message(broker_url, queue, title, data_id, app_type):
    logging.info("Sending message to queue: %s" % broker_url)
    successful = False

    data = {
        "title": title,
        "data_id": data_id,
        "app_type": app_type
    }

    credentials = pika.PlainCredentials('user', 'password')

    # Connect to RabbitMQ using the default parameters
    parameters = pika.ConnectionParameters(host=broker_url, credentials=credentials)
    connection = pika.BlockingConnection(parameters)

    # Create a channel
    channel = connection.channel()

    # Declare queue
    channel.queue_declare(
        queue=queue,
        durable=True,
        exclusive=False,
        auto_delete=False,
        arguments={
            "x-queue-type": "quorum"
        }
    )
    channel.confirm_delivery()

    print("Sending json message...%s" % json.dumps(data))
    try:
        channel.basic_publish(
            exchange='', 
            routing_key='announcement',
            body=json.dumps(data),
            properties=pika.BasicProperties(content_type='application/json',
                             delivery_mode=DeliveryMode.Transient))
        print('Message publish was confirmed')
        successful = True
    except pika.exceptions.UnroutableError:
        print('Message could not be confirmed')
        successful = False
    connection.close()

    return successful
