# Get the service resource
import boto3

sqs = boto3.resource('sqs')

# Create the queue. This returns an SQS.Queue instance
response_queue = sqs.get_queue_by_name(QueueName='responseQueue')

# Create a new message
response = response_queue.send_message(MessageBody='Kamil', MessageAttributes={
    'Author': {
        'StringValue': 'Daniel',
        'DataType': 'String'
    }
})
# The response is NOT a resource, but gives you a message ID and MD5
print(response.get('MessageId'))
print(response.get('MD5OfMessageBody'))
print(response)
