from pygtail import Pygtail
import requests
import os
import re
import threading
import logging
from time import sleep
# coping with Python 2 vs 3 inconsistencies
try:
    import ConfigParser 
except ImportError:
    import configparser

logging.basicConfig(filename='LogDaemon.log', filemode='w',format='%(asctime)s %(message)s',level=logging.INFO)

requests.packages.urllib3.disable_warnings()

# open properties file
# coping with Python 2 vs 3 inconsistencies
try:
    config = ConfigParser.ConfigParser()
except:
    config = configparser.ConfigParser()

config.read('config.properties')
# get properties
token=config.get('dynatrace','token')
tenantURL=config.get('dynatrace','tenantURL')
entityID=config.get('dynatrace','entityID')
fileNames=config.get('log','fileNames')
patterns=config.get('log','patterns')

# build a list of file names
files=fileNames.split(';')

# build a list of words from the given patterns
words=patterns.split(';')

# Check if string matches regex list 
# Using join regex + loop + re.match() 
any_regex = '(?:% s)' % '|'.join(words) 


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








def monitor_function(fileName):
    try:
        logging.info("Monitoring :" +fileName+" for new occurences of : "+any_regex)

        while True:
            # Follow the file as it grows
            for line in Pygtail(fileName, read_from_end=True):

                logging.debug(line)

                # did we find a match ?
                if re.search(any_regex, line): 
                    logging.info("match found :"+line+" in "+fileName)

                    print("found match in "+fileName)

                    # fill event details with error context 
                    content['description']=line

                    # send event to Dynatrace
                    r = requests.post(
                        tenantURL+'/api/v1/events', 
                        json=content,
                        headers={'Authorization': "Api-Token " + token},
                        verify=False
                        )

                    # eror ?
                    if(r.status_code != 200):
                        logging.error(r.status_code, r.reason, r.text) 
                    else:
                        logging.debug(r.text)
            # wait 5 seconds
            sleep(5)
    except Exception as Argument:  
        logging.exception(msg="Exception")  

print("Starting active log monitoring...")

# start as many threads as there are input files to monitor
for file in files:
    t = threading.Thread(target=monitor_function, args=(file,))
    t.daemon=True
    t.start()

while True:
    sleep(1)
