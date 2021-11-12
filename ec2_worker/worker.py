import logging
import numpy as np
import json
import sys
import boto3
import uuid
from datetime import datetime

# datetime object containing current date and time

sqs = boto3.resource('sqs')


def main():
    worker_process()


def worker_process():
    log_bucket = retrieve_bucket()
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
                        result = {
                            'Mean': str(np.mean(array_numbers)),
                            'Median': str(np.median(array_numbers)),
                            'Max': str(np.max(array_numbers)),
                            'Min': str(np.min(array_numbers))}

                        response_queue.send_message(MessageBody=id, MessageAttributes={
                            'Result': {
                                'StringValue': json.dumps(result),
                                'DataType': 'String'
                            },
                        }, )

                        # Let the queue know that the message is processed
                        root.info('Response sent ' + id)

                        add_log(log_bucket, {
                            "id": id,
                            "params": array_numbers,
                            "result": result,
                        })

                        message.delete()
                except Exception as e:
                    root.error(e)
                    message.delete()


def retrieve_bucket():
    s3_client = boto3.client('s3')
    bucket_name = 'log-bucket-681f6689c44546458ae5910ffc3a504a'

    try:
        return boto3.resource("s3").Bucket(bucket_name)
    except Exception:
        # Create bucket
        s3_client.create_bucket(Bucket=bucket_name)
        return boto3.resource("s3").Bucket(bucket_name)


def add_log(log_bucket, log):
    json.load_s3 = lambda k: json.load(log_bucket.Object(key=k).get()["Body"])
    json.dump_s3 = lambda obj, k: log_bucket.Object(key=k).put(Body=json.dumps(obj))

    data = json.load_s3("logs.json")

    date_str = datetime.now().strftime("%Y_%m_%dT%H_%M_%S")
    data[date_str] = log  # Add log into log file

    json.dump_s3(data, "logs.json")


if __name__ == "__main__":
    main()
