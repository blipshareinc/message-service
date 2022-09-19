import pika
import json
import logging

logging.basicConfig(level=logging.DEBUG)

def start_message_listener(broker_url, queue):
    logging.info("Starting listener for host=%s and queue=: %s" % (broker_url, queue))

    credentials = pika.PlainCredentials('user', 'password')

    # Connect to RabbitMQ using the default parameters
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker_url, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(
        queue=queue,
        durable=True,
        exclusive=False,
        arguments={
            "x-queue-type": "quorum"
        }
    )

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()  
