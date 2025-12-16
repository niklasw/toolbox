#!/bin/bash

REGION=eu-north-1
TYPE=${1:-"r6a.xlarge"}

aws ec2 describe-instance-type-offerings \
  --region "$REGION" \
  --location-type availability-zone \
  --filters Name=instance-type,Values="$TYPE" \
  --query 'InstanceTypeOfferings[].Location' --output json

