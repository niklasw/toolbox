#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
import logging


class ec2_simple:

    def __init__(self, aws_profile='default',
                 ami_name=None,
                 instance_type=None):
        boto3.setup_default_session(profile_name=aws_profile)
        self.client = boto3.client('ec2')
        self.ami_name = ami_name
        self.instance_type = instance_type
        self.instance_id = None
        self.instance_ip = None

    def run_checks(self):
        try:
            assert self.ami_name in self.list_amis()
        except AssertionError:
            logging.error('ec2_simple checks failed')
            sys.exit(1)

    def get_ami_id(self):
        amis = self.client.describe_images(Owners=['self'])
        for ami in amis.get("Images"):
            if ami.get("Name") == self.ami_name:
                return ami.get("ImageId")

    def list_amis(self):
        amis = self.client.describe_images(Owners=['self'])
        return [a.get('Name') for a in amis.get('Images')]

    def list_security_groups(self):
        security_groups = {}
        try:
            response = self.client.describe_security_groups()
            security_groups_data = response.get('SecurityGroups', [])
        except ClientError as e:
            print("An error occurred while fetching security groups:", str(e))

        for group in security_groups_data:
            group_name = group.get('GroupName')
            group_id = group.get('GroupId')
            description = group.get('Description')
            vpc_id = group.get('VpcId')

            security_groups[group_name] = {
                'GroupID': group_id,
                'Description': description,
                'VPCID': vpc_id
            }

        return security_groups

    def get_security_group_id(self, name):
        groups = self.list_security_groups()
        group_info = groups.get(name)
        if group_info:
            return group_info.get('GroupID')

    def list_key_pairs(self):
        response = self.client.describe_key_pairs()
        key_pairs = response['KeyPairs']
        available_key_pairs = [key_pair['KeyName'] for key_pair in key_pairs]
        return available_key_pairs

    def launch_instance_from_ami(self,
                                 key_name,
                                 security_group_id):
        response = self.client.run_instances(
            ImageId=self.get_ami_id(),
            InstanceType=self.instance_type,
            KeyName=key_name,
            SecurityGroupIds=[security_group_id],
            MinCount=1,
            MaxCount=1
        )

        instance_id = response['Instances'][0]['InstanceId']
        print("Instance created with ID:", instance_id)

        ec2_resource = boto3.resource('ec2')
        instance = ec2_resource.Instance(instance_id)

        instance.wait_until_running()
        instance.load()

        instance_public_ip = instance.public_ip_address
        print("Public IP:", instance_public_ip)

        self.client.create_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'Name', 'Value': 'MyInstance'}
                # Add any additional tags as needed
            ]
        )

        # # Associate the public key with the instance
        # self.client.associate_key_pair(
        #     KeyName=key_name,
        #     InstanceId=instance_id
        # )

        self.instance_id = instance_id
        self.instance_ip = instance_public_ip

        return {'instance_id': instance_id,
                'instance_ip': instance_public_ip}

    def terminate_instance(self):
        try:
            response = self.client.terminate_instances(
                InstanceIds=[self.instance_id]
            )

            if response['TerminatingInstances'][0]['InstanceId'] \
                    == self.instance_id:
                print("Instance terminated successfully.")

        except ClientError as e:
            print("An error occurred while terminating the instance:", str(e))
        self.instance_id = None

    def stop_instance(self):
        instance_id = self.instance_id
        try:
            response = self.client.stop_instances(
                InstanceIds=[instance_id]
            )

            if response['StoppingInstances'][0]['InstanceId'] == instance_id:
                print("Instance stopped successfully.")

        except ClientError as e:
            print("An error occurred while stopping the instance:", str(e))


def main():
    args = {
        'aws_profile': 'default',
        'ami_name': 'cfd-server-230608',
        'instance_type': 'c5a.4xlarge',
    }

    ec2_mgr = ec2_simple(**args)
    ec2_mgr.run_checks()
    print(f'AMI id = {ec2_mgr.get_ami_id()}')
    for pair in ec2_mgr.list_key_pairs():
        print(f'Key pair: {pair}')


if __name__ == '__main__':
    main()
    if 'start' in sys.argv:
        pass
    elif 'stop' in sys.argv:
        pass
