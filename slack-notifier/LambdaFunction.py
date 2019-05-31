'''
This is a sample function to send AWS Health event messages to a Slack channel. 

Follow these steps to configure the webhook in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/apps

  2. Search for and select "Incoming WebHooks".

  3. Select "Add Configuration" and choose the default channel where messages will be sent. Then click "Add Incoming WebHooks Integration".

  4. Copy the webhook URL from the setup instructions and use it in the configuration section bellow

You can also use KMS to encrypt the webhook URL as shown here: https://aws.amazon.com/blogs/aws/new-slack-integration-blueprints-for-aws-lambda/
'''

from __future__ import print_function

import boto3
import json
import logging
import os

from urllib2 import Request, urlopen, URLError, HTTPError

#configuration

# The Slack channel to send a message to stored in the slackChannel environment variable
SLACK_CHANNEL = "#awshealth"
# Add the webhook URL from Slack below
HOOK_URL = "https://hooks.slack.com/services/example"
# Setting up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#main function

def lambda_handler(event, context):
    message =  str("Account: "+event['account']
    +"\nService: "+event['detail']['service']+", EventType: "+event['detail']['eventTypeCategory']
    +"\n"+event['detail']['eventDescription'][0]['latestDescription']
    +"\n<https://phd.aws.amazon.com/phd/home?region=us-east-1#/event-log?eventID="+event['detail']['eventArn']+"|Click here> for details.") 
    json.dumps(message)
    slack_message = {
        'channel': SLACK_CHANNEL,
        "text": "*_A new AWS event has been scheduled_*",
        "username": "AWS - Personal Health Updates",
        "icon_url": "https://s3-us-west-2.amazonaws.com/slack-files2/avatars/2019-05-31/651576919984_505d9b9fef6b87d7bcb7_72.png",
        "pretty": "1",
        "attachments": [
            {
                "fallback": "This is attachment with event",
                "title": event['detail']['eventTypeCategory'],
                "text": message,
                "color": "#d8a500",
                "footer": "Send from lambda",
            }
        ]
    }
    logger.info(str(slack_message))
    
    req = Request(HOOK_URL, json.dumps(slack_message))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)