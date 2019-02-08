import json
import boto3
import urllib
import re
import uuid
import os 
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
  try:
       req_body = event['body']
       params = urllib.parse.parse_qs(req_body)
       id = str(uuid.uuid1())
       points = str(params['text'][0].count("+") - 1)
       negative_points =  params['text'][0].count("-") + 1
       name = str(re.findall(r'\@\w+', str(params['text'][0]))[0])
       table =  os.environ['TABLE_NAME']
       response = dynamodb.get_item(TableName=table, Key={'name':{'S':name}})

       try:
         item = response['Item']
       except KeyError as error:
          print(error)
          item = None

       if item != None:
          print('this will also show up in cloud watch' + response["Item"]['name']["S"])
          total_points = int(response["Item"]['karma']["S"])
          logger.info('got event{}'.format(event))
       else:
          total_points = 0
          print("I shouldn't be printed")

       new_points = total_points + int(points)

       dynamodb.put_item(TableName=table, Item={'push_id':{'S':id}, 'name':{'S':name}, 'karma':{'S':str(new_points)}})

       return {
            'statusCode': 200,
            'body': json.dumps(new_points)
            }

  except Exception as e:
        print(e)
        return {
            'statusCode': 200,
            'body': "--- HELP TOPICS --- \n To add or deduct karma, simply type /karma @user ++ (or --) where @user is the slack username \n" 
            "To see karma points, simply type /karma @user."
            }
                
