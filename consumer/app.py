from flask import Flask, request, jsonify

from fetch_messages import start_message_listener

app = Flask("Message Service")

start_message_listener("localhost", "announcement")
