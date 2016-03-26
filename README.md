# project
Text your door!
# Requirements
Twilio API Key
AWS IAM identity. 
# Dependecies
Python: Flask, boto3, twilio
# The Backend

The server is a flask server on an AWS EC2 instance running behind nginx for static file serving and load balancing. 
The server waits for webhooks from twilio to engage authentication and opening/closing the door and texts the user the door's status.
The server is connected to the doors through AWS's IoT solution. 
The server state saves and loads information form AWS's DynamoDB. Data analytics is performed with AWS's elastic MapReduce/Hadoop/Hive.
