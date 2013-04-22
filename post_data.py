#Add a billing record
import sys
import urllib, urllib2
import json
from datetime import datetime
from django.utils.timezone import utc
import base64

if len(sys.argv) < 4 or len(sys.argv) > 5:
    print "Usage: python post_data.py http://billy.rc.fas.harvard.edu/a/api/billingrecord/ <username> <password> [<data_dictionary>]"
    sys.exit()

url = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

now = str(datetime.utcnow().replace(tzinfo=utc))  #format now as a string

#The data
if len(sys.argv) == 5:
    data = sys.argv[4]
else:
    data = {
        'amount': 20,
        'bill_date': now,
        'created': now,
        'modified': now,
        'name': 'Tapes',
        'payment_code': '123-12345-4444-666666-123455-1234-99999',
        'user': '/a/api/user/1/'
        }

request = urllib2.Request(url)                        #create the request object
json_data = json.dumps(data)                          #json-fy the data
if len(sys.argv) == 5:
    json_data = data
request.add_data(json_data) 

request.add_header('Content-Type', 'application/json')
request.add_header('Accept', 'application/json, text/html')
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
response = urllib2.urlopen(request)                       #open the url request object and capture the response

output = response.read()                                  #read the string response
if output:
    print output
else:
    print "Billing Record Added."

"""
Example:
python post_data.py http://billy.rc.fas.harvard.edu/a/api/billingrecord/ billyidol apiswithoutaface "{\"amount\": 30, \"bill_date\": \"2013-04-08 15:22:01.478283+00:00\", \"created\": \"2013-04-08 17:22:01.478283+00:00\", \"modified\": \"2013-04-09 11:22:01.478283+00:00\", \"payment_code\": \"123-12345-1234-123456-123456-1234-12345\", \"name\": \"Bryan Adams Mix Tape\", \"user\": \"/a/api/user/1/\"}"
"""
