import boto3
import json


class CalculationService:
    """
    Calculation object
    """
    REQUEST_QUEUE_NAME = 'requestQueue'
    RESPONSE_QUEUE_NAME = 'responseQueue'

    booted = False

    def __init__(self):
        self.sqs = boto3.resource('sqs')

        try:
            # Create the queue. This returns an SQS.Queue instance
            self.request_queue = self.sqs.get_queue_by_name(QueueName=self.REQUEST_QUEUE_NAME)
            self.response_queue = self.sqs.get_queue_by_name(QueueName=self.RESPONSE_QUEUE_NAME)
            self.booted = True
        except Exception as e:
            print(e)

    def send_message(self, _nums: list):
        """
        Send calculation to Simple Queue Service
        :param _nums: list of numbers
        :return: the request id
        """
        message_attr: dict = {
            'Numbers': {
                'StringValue': json.dumps(_nums),
                'DataType': 'String'
            }
        }
        request = self.response_queue.send_message(MessageBody='Calculation', MessageAttributes=message_attr)
        return request['MessageId']

    def get_message(self, _message_id: str):
        """
        Get calculation response from Simple Queue Service
        :param _message_id:
        :return: the calculation response
        """
        for message in self.response_queue.receive_messages(MaxNumberOfMessages=10, MessageAttributeNames=['Numbers']):
            if message.message_id == _message_id:
                return message.message_attributes

        return None
