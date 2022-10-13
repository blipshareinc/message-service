from flask import Flask, request, jsonify

from fetch_messages import start_message_listener
from os import environ

app = Flask("Message Service")

broker_url = environ["BROKER_URL"]
db_url = "%s:%s" % (environ["DATABASE_URL"], environ["DATABASE_PORT"])
start_message_listener(broker_url, database_url , "announcement")
