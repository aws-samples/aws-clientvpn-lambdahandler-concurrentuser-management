#    Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#    SPDX-License-Identifier: MIT-0
  
#    Permission is hereby granted, free of charge, to any person obtaining a copy of this
#    software and associated documentation files (the "Software"), to deal in the Software
#    without restriction, including without limitation the rights to use, copy, modify,
#    merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#    permit persons to whom the Software is furnished to do so.
  
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#    PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import boto3
client_vpn = boto3.client('ec2', region_name='<Region>')
#<Region>: Replace with AWS ClientVPN Endpoint Region
def lambda_handler(event, context):
  # Get user ID
  print(event)
  user_id = event["username"]
  client_vpn_endpoint_id = event["endpoint-id"]
  # Check for existing connections
  print(user_id)
  response = client_vpn.describe_client_vpn_connections(
     ClientVpnEndpointId=client_vpn_endpoint_id,
      Filters=[
          {
              "Name": "username",
              "Values": [user_id]
          },
          {
              "Name": "status",
              "Values": ["active"]
          }
      ]
  )
  if len(response["Connections"]) > 0:
      # Close existing connection
      print(response["Connections"])
      connection_id = response["Connections"][0]["ConnectionId"]
      client_vpn.terminate_client_vpn_connections( ClientVpnEndpointId=client_vpn_endpoint_id,ConnectionId=connection_id)
      print("Closed existing connection as conncurrent connection from same user is not allowed.")
  # Allow new connection
  return {
    "allow": True,
        "error-msg-on-failed-posture-compliance": "Failed",
        "posture-compliance-statuses": [],
        "schema-version": "v1"
  }