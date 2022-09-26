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
        logging.error(stderr)
    if stdout:
        logging.debug("Ran command: %s" % "".join(cmd))

def _fetch_data_from_db(db_url, data_id):
    url = '%s/tts/get_tts/%s' % (db_url, data_id)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }
    req = requests.get(url, headers=headers)
    logging.debug("TTS: getting data from database using url: %s and data_id: %s" % (url, data_id))
    json = req.json()
    logging.debug('TTS: Response for data_id: %s => %s' % (data_id, json))

    if json:
        audio_file_path = json['audio_file_name']
        if audio_file_path:
            audio_file_path = path.join('/app/output', audio_file_path)

            ## first announce that there is a new announcement
            audio_path = path.join('/app/output', 'new_announcement.wav')
            cmd = ['vlc -I dummy %s vlc://quit' % audio_path]
            _run_shell_command(cmd)
    
            # announce the data received, play it twice for the user to hear it properly
            count = 0
            while count < 2:
                cmd = ['vlc -I dummy %s vlc://quit' % audio_file_path]
                _run_shell_command(cmd)
                # sleep for few seconds in case there are more than one announcement
                # this allows to create a gap between announcements
                sleep(3)
                count+=1

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
            logging.debug('TTS: %s' % body)

            if 'title' in body and \
                'data_id' in body and \
                'app_type' in body:
                # get and process from the database
                _fetch_data_from_db(db_url, body['data_id'])
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()  
