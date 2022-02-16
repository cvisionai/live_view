#!/usr/bin/python3
import boto3
import argparse
import time
import yaml
import requests
import datetime
from dateutil.parser import parse
import pytz

from collections import defaultdict

if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("config")
  args = parser.parse_args()

  with open(args.config, 'r') as fp:
    config = yaml.safe_load(fp)

  print("Publishing to " + config.get('arn'))
  host = config.get('host')
  token = config.get('token')
  server_names = config.get('server_names')
  server_bad = defaultdict(lambda: False)
  server_last = defaultdict(lambda: pytz.utc.localize(datetime.datetime.fromtimestamp(0)))
  while True:
    for server_name in server_names:
       url = f"{host}/rest/StationInfoByName/{server_name}"
       headers = {"Authorization": f"Token {token}"}
       print(url)
       resp = requests.get(url, headers=headers)
       data = resp.json()
       utc_now = datetime.datetime.utcnow()
       utc_now = pytz.utc.localize(utc_now)
       last_hb = parse(data['last_updated'])
       delta = utc_now - last_hb
       name = data['name']
       time_since_last_alert = utc_now - server_last[server_name]
       if delta > datetime.timedelta(hours=1):
         if time_since_last_alert > datetime.timedelta(hours=6):
           server_last[server_name] = utc_now
           msg=f"{name} if out of communication. Last update at {last_hb}"
           print(msg)
           sns = boto3.resource('sns', region_name=config.get('region','us-east-1'))
           topic = sns.Topic(config.get('arn'))
           topic.publish(Message=msg)
           server_bad[server_name] = True
       elif server_bad[server_name] and delta < datetime.timedelta(hours=1):
         server_bad[server_name] = False
         last_alert = pytz.utc.localize(datetime.datetime.fromtimestamp(0))
         msg=f"{name} is back in range. Last update at {last_hb}"
         print(msg)
         sns = boto3.resource('sns', region_name=config.get('region','us-east-1'))
         topic = sns.Topic(config.get('arn'))
         topic.publish(Message=msg)
       else:
         pass

    time.sleep(config.get('interval', 600))
