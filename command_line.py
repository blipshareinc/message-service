import argparse
import logging

from publisher.publish_message import publish_new_message
from consumer.fetch_messages import start_message_listener

logging.basicConfig(level=logging.DEBUG)

def _validate_field(field, field_name):
    if not field or field == '':
        logging.error("%s is required" % field_name)
        return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Message Processor")
    parser.add_argument("-url", "--URL", dest="broker_url", help="URL to Rabbitmq borker", required=True)
    parser.add_argument("-a", "--ACTION", dest="action", help="Action to perform i.e. \"publish\", or \"fetch\"", required=True)
    parser.add_argument("-q", "--QUEUE", dest="queue", help="Queue to use for processing", required=True)
    parser.add_argument("-t", "--TITLE", dest="title", help="Message Title")
    parser.add_argument("-data_id", "--DATA_ID", dest="data_id", help="Data ID", required=True)
    parser.add_argument("-app_type", "--APP_TYPE", dest="app_type", help="App Type Integer", required=True)

    args = parser.parse_args()

    if args.action.lower() == "publish":
        # validate required fields
        if _validate_field(args.title, ' -t (Title)'):
            publish_new_message(args.broker_url, args.queue, args.title, args.data_id, args.app_type)
    else if args.action.lower() == "fetch":
        start_message_listener(args.broker_url, args.queue)
