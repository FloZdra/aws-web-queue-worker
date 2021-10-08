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
    create_key_pair()
    create_instance()

    instance_id = 'ec2_queue_worker'
    action = sys.argv[1].upper()

    ec2 = boto3.client('ec2')

    if action == 'ON':
        # Do a dryrun first to verify permissions
        try:
            ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, run start_instances without dryrun
        try:
            response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)

            worker_process()
        except ClientError as e:
            print(e)
    else:
        # Do a dryrun first to verify permissions
        try:
            ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)


def worker_process():
    # Get the queue
    logging.info("Application has started")
    request_queue = sqs.get_queue_by_name(QueueName='requestQueue')
    response_queue = sqs.get_queue_by_name(QueueName='responseQueue')
    while 1:
        for message in request_queue.receive_messages(MessageAttributeNames=['Numbers']):
            logging.info("New messages in requestQueue")
            if message.message_attributes is not None:
                id = message.message_attributes.get('Id')
                numbers = json.loads(message.message_attributes.get('Numbers'))
                if len(numbers) > 0:
                    response_queue.send_message(MessageId=id, MessagAttributes={
                        'Result': {
                            'Mean': np.mean(numbers),
                            'Median': np.median(numbers),
                            'Max': np.max(numbers),
                            'Min': np.min(numbers)
                        }
                    })
                    # Let the queue know that the message is processed
                    message.delete()



if __name__ == "__main__":
    main()
