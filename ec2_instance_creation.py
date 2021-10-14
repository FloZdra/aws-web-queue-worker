import logging
import os

import boto3


def create_key_pair():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    response = ec2_client.describe_key_pairs(
        KeyNames=['ec2-key-pair'],
    )

    logging.info("Checking if a ec2-key-pair KeyPair already exist")
    if len(response['KeyPairs']) > 0:
        logging.info("KeyPair found :")
        logging.info(response['KeyPairs'][0])
    else:
        logging.info("KeyPair not found")
        logging.info("Creating a new KeyPair : ec2-key-pair")

        key_pair = ec2_client.create_key_pair(KeyName="ec2-key-pair")
        private_key = key_pair["KeyMaterial"]

        # write private key to file with 400 permissions
        with os.fdopen(os.open("/tmp/aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
            handle.write(private_key)


def create_instance():
    logging.info("Checking if a ec2_queue_worker instance already exist")

    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(Filters=[
        {'Name': 'tag:Name', 'Values': ['ec2_queue_worker']}], )
    print(response)

    if len(response['Reservations']) > 0 and len(response['Reservations'][0]):
        logging.info("Instance found")
        logging.info(response['Reservations'][0]['Instances'])
        return response['Reservations'][0]['Instances'][0]['InstanceId']
    else:
        logging.info("Instance not found")
        logging.info("Creating a new instance : ec2-ec2_queue_worker-pair")

        ec2 = boto3.client("ec2", region_name="us-east-1")
        instances = ec2.run_instances(
            ImageId="ami-087c17d1fe0178315",
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName="ec2-key-pair",
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'ec2_queue_worker'}]
            }]
        )
        return instances[0]['ImageId']