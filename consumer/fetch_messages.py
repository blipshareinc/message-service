from asyncio import subprocess
from time import sleep
from os import path, environ
import subprocess
import pika
import json
import logging
import requests

logging.basicConfig(level=logging.DEBUG)


def _run_shell_command(cmd):
    sub_p = subprocess.Popen(
        args=cmd,
        env=dict(environ),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)
    stdout, stderr = sub_p.communicate()

    if stderr:
        logging.error("Error running cmd: %s" % "".join(cmd))
    if stdout:
        logging.debug("Ran command: %s" % "".join(cmd))

def _fetch_data_from_db(db_url, data_id):
    url = '%s/tts/get_tts' % db_url
    headers = {'Content-Type': 'application/json'}
    params = {'id': data_id}
    req = requests.get(url, headers=headers, params=params)
    json = req.json()     
    logging.info('Response for data_id: %s => %s' % (data_id, json))

    if json:
        audio_file_path = json['audio_file_name']
        if audio_file_path:
            audio_file_path = path.join('/app/output', audio_file_path)

            # announce the data received
            cmd = ['vlc -I dummy %s vlc://quit' % audio_file_path]
            _run_shell_command(cmd)
            # sleep for few seconds in case there are more than one announcement
            # this allows to create a gap between announcements
            sleep(3)

def start_message_listener(broker_url, db_url, queue):
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
        # start processing if data is available
        if body:
            body = json.loads(body)
            logging.info(body)
            if 'title' in body and \
                'data_id' in body and \
                'app_id' in body:
                # get and process from the database
                _fetch_data_from_db(db_url, body['data_id'])
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()  
