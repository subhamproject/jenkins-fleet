#!/usr/bin/python3

import sys
import os
import logging
import boto3
import botocore
import click


@click.group()
def cli():
    pass

def connect(region):
  session = boto3.Session(region_name=region)
  ec2 = session.client('ec2')
  return ec2


def spot_config(arch, region,ami,price,instance_type):
   return  {
                'SpotPrice': price,
                'TargetCapacity': 1,
                'Type': 'maintain',
                'AllocationStrategy': 'lowestPrice',
                'TerminateInstancesWithExpiration': False,
                'IamFleetRole': 'arn:aws:iam::707015264015:role/aws-ec2-spot-fleet-tagging-role',
                'LaunchSpecifications': [
                    {
                        'ImageId': ami,
                        'KeyName': 'Testing',
                        'SecurityGroups': [
                            {
                                'GroupId': 'sg-0d6f0db8c0b658cda',
                            }
                       ],
                        'InstanceType': instance_type,
                        "SubnetId": "subnet-0b78e520b59606a9c",
                        'IamInstanceProfile': {
                           'Arn': 'arn:aws:iam::707015264015:instance-profile/S3-Push-Access'
                         },
                    }
                ],
               'TagSpecifications': [
                        {
                'ResourceType': 'spot-fleet-request',
                  'Tags': [
                      {
                      'Key': 'Name',
                      'Value': 'Jenkins Slave'
                      }
                    ]
                 }
              ],
            }

@cli.command()
@click.option('--arch', help='The spot fleet architecture')
@click.option('--region', help='The region to request instances in.', default='us-west-2')
def create_fleet(arch,region):
    """
    Spot Fleet Request Scripts
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(process)d - [%(levelname)s] %(message)s',
    )
    logger = logging.getLogger()

    # Ensure requires parameters are set.
    if arch is None:
        logger.critical('No spot fleet archirecture provided [arm or amd], cannot continue.')
        sys.exit(-1)

    logger.info("Attempting to create a fleet of \"{}\" jenkins slaves in {} region.".format(arch,region))

    if arch == 'amd':
     ami='ami-0e5b6b6a9f3db6db8'
     price=str(0.133)
     instance_type='t2.micro'
    elif arch == 'arm':
     ami='ami-0e5b6b6a9f3db6db8'
     price=str(0.33)
     instance_type='t2.small'

    try:
        ec2=connect(region)
        request = ec2.request_spot_fleet(
            SpotFleetRequestConfig=spot_config(arch, region, ami,price,instance_type)
       )
    except botocore.exceptions.ParamValidationError as err:
        logger.critical('Bad parameters provided, cannot continue: {}'.format(err))
        sys.exit(-2)
    except botocore.exceptions.ClientError as err:
        logger.critical('Failed to request spot fleet, cannot continue: {}'.format(err))
        sys.exit(-3)

    logger.info("Spot fleet requested! Reference is \"{}\".".format(request['SpotFleetRequestId']))


if __name__ == '__main__':
    cli()
