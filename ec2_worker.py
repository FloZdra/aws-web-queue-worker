# Get the service resource
import logging

import numpy as np
import json
import sys
import boto3
from botocore.exceptions import ClientError

from ec2_instance_creation import create_key_pair, create_instance

sqs = boto3.resource('sqs')


def main():
    worker_process()


def worker_process():
    # Get the queue
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    root.info('Application is starting')

    sqs.create_queue(QueueName='requestQueue')
    sqs.create_queue(QueueName='responseQueue')
    request_queue = sqs.get_queue_by_name(QueueName='requestQueue')
    response_queue = sqs.get_queue_by_name(QueueName='responseQueue')
    while 1:
        for message in request_queue.receive_messages(MessageAttributeNames=['Numbers']):
            root.info("New messages in requestQueue")
            if message.message_attributes is not None:
                id = message.message_id
                numbers = message.message_attributes.get('Numbers')

                try:
                    array_numbers = [int(i) for i in numbers['StringValue'].split()]
                    if len(array_numbers) > 0:
                        response_queue.send_message(MessageBody=id, MessageAttributes={
                            'Result': {
                                'StringValue': json.dumps({
                                    'Mean': str(np.mean(array_numbers)),
                                    'Median': str(np.median(array_numbers)),
                                    'Max': str(np.max(array_numbers)),
                                    'Min': str(np.min(array_numbers))}),
                                'DataType': 'String'
                            },
                        }, )
                        # Let the queue know that the message is processed
                        root.info('Response sent ' + id)
                        message.delete()
                except Exception as e:
                    root.error(e)
                    message.delete()


if __name__ == "__main__":
    main()
