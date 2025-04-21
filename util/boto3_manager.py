import json
import logging

from botocore.exceptions import ClientError

import constants.server_constants
from constants.server_constants import aws_constants
import boto3


class boto3_client:

    def __init__(self):
        self.client = boto3.client('ec2')
        self.ssm_client = boto3.client('ssm')
        self.response = None
        self.spot_id = None

    def start_server(self, template_id: str, version: str, min_ram: int, max_ram: int):
        try:
            self.response = self.client.request_spot_fleet(
                SpotFleetRequestConfig={
                    'AllocationStrategy': 'priceCapacityOptimized',
                    'IamFleetRole': "arn:aws:iam::654654487262:role/aws-service-role/spotfleet.amazonaws.com/AWSServiceRoleForEC2SpotFleet",
                    'InstanceInterruptionBehavior': "terminate",
                    'LaunchTemplateConfigs': [
                        {
                            'LaunchTemplateSpecification': {
                                'LaunchTemplateId': template_id,
                                'Version': version
                            },
                            'Overrides': [
                                {
                                    'InstanceRequirements': {
                                        "VCpuCount": {
                                            "Min": 2,
                                            "Max": 2
                                        },
                                        "MemoryMiB": {
                                            "Min": min_ram * 1024,
                                            "Max": max_ram * 1024
                                        },
                                    },
                                },
                            ],
                        },
                    ],
                    'TargetCapacity': 1,
                    'ReplaceUnhealthyInstances': False,
                    'TerminateInstancesWithExpiration': True,
                    'Type': 'request',
                }
            )
            self.spot_id = self.response["SpotFleetRequestId"]
        except ClientError as e:
            print("FAILED!!!")
            if 'DryRunOperation' not in str(e):
                raise

    def stop_server(self):
        try:
            self.client.stop_instances(InstanceIds=[aws_constants.SERVER_ID.value], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise
        try:
            response = self.client.stop_instances(InstanceIds=[aws_constants.SERVER_ID.value], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)

    def get_client(self):
        return self.client

    def is_open(self, channel):
        try:

            if channel == 1149356729675563028:
                eip_settings = self.client.describe_addresses(AllocationIds=["eipalloc-0425d30af78b9e27e"])
                for index in eip_settings["Addresses"]:
                    if index["InstanceId"] is not None:
                        return True

            if channel == 1191571678803808266:
                eip_settings = self.client.describe_addresses(AllocationIds=["eipalloc-0306e6f3f785630ee"])
                for index in eip_settings["Addresses"]:
                    if index["InstanceId"] is not None:
                        return True

        except KeyError:
            return False

