from flask import Flask, request, jsonify

from os import environ
from publish_message import publish_new_message

app = Flask("Message Service")

@app.route('/announce', methods=['POST'])
def announce():
    '''
    Description: Function to listen for user request with json parameters to add as
    an announcement in RabbitMQ
    It takes in the following parameters:
    title: Message title
    data_id: Data id to the tts table 
    app_type: Integer to indicate the application that create the message
    @return: jsonify string.
    '''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        print('Host: %s' % host)
        if json and 'title' in json \
            and 'data-id' in json \
            and 'app-type' in json:
            if publish_new_message(
                environ['BROKER_URL'],
                'announcement',
                json['title'],
                json['data-id'],
                json['app-type']):
                return jsonify({"status_code": 200, "message": "Message successfully sent."})
            return jsonify({"status_code": 500, "message": "Message was now sent."})

