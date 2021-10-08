# Get the service resource
import boto3

sqs = boto3.resource('sqs')

# Create the queue. This returns an SQS.Queue instance
request = sqs.create_queue(QueueName='requestQueue', Attributes={'DelaySeconds': '500'})
response = sqs.create_queue(QueueName='responseQueue', Attributes={'DelaySeconds': '500'})

print(request.url)
print(request.attributes.get('DelaySeconds'))
print(response.url)
print(response.attributes.get('DelaySeconds'))
