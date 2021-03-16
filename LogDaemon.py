import tailer 
import configparser 
import requests
import os
import re

# open properties file
config = configparser.ConfigParser()
config.read('config.properties')
# get properties
token=config['dynatrace']['token']
tenantURL=config['dynatrace']['tenantURL']
entityID=config['dynatrace']['entityID']
fileName=config['log']['fileName']
patterns=config['log']['patterns']

# build a list of words from the given patterns
words=patterns.split(';')

# event json structure to send to Dynatrace
# See https://www.dynatrace.com/support/help/shortlink/api-events-post-event
content={
        "eventType": "AVAILABILITY_EVENT",
        "description": "." ,
        "source": os.path.basename(__file__) ,
        "attachRules": {
            "entityIds": [ entityID ]
            }
         }



# Check if string matches regex list 
# Using join regex + loop + re.match() 
any_regex = '(?:% s)' % '|'.join(words) 

print("Monitoring :" +fileName+" for new occurences of : "+any_regex)

# Follow the file as it grows
for line in tailer.follow(open(fileName)):

    
    print(line)

    # did we find a match ?
    if re.match(any_regex, line): 
        print("found match in :"+line)

        # fill event details with error context 
        content['description']=line

        # send event to Dynatrace
        r = requests.post(
            tenantURL+'/api/v1/events', 
            json=content,
            headers={'Authorization': "Api-Token " + token}
            )

        # eror ?
        if(r.status_code != 200):
            print(r.status_code, r.reason, r.text) 
        else:
            print(r.text)