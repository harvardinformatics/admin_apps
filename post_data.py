#Add a billing record
import sys
import urllib, urllib2
import json
from datetime import datetime
from django.utils.timezone import utc
import base64

username = sys.argv[1]
password = sys.argv[2]

base_url = 'localhost:8000'

now = str(datetime.utcnow().replace(tzinfo=utc))  #format now as a string

#The data
data = {
    'amount': 20,
    'bill_date': now,
    'created': now,
    'modified': now,
    'name': 'Eric\'s Love',
    'payment_code': '123-12345-4444-666666-123455-1234-99999',
    'user': '/a/api/user/1/'
}

url = "http://" + base_url + "/a/api/billingrecord/"
request = urllib2.Request(url)                        #create the request object
json_data = json.dumps(data)                          #json-fy the data 
request.add_data(json_data) 
#headers = {'Content-Type': 'application/json', 
#           'Accept': 'application/json, text/html',
#           }  #Add headers (necessary for POSTS)

request.add_header('Content-Type', 'application/json')
request.add_header('Accept', 'application/json, text/html')
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)


response = urllib2.urlopen(request)                       #open the url request object and capture the response
output = response.read()                                  #read the string response
print output

