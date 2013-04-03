#Add a billing record
import urllib, urllib2
import json
from datetime import datetime
from django.utils.timezone import utc
import base64

base_url = 'localhost:8000'

now = str(datetime.utcnow().replace(tzinfo=utc))  #format now as a string

#The data
data = {
    'amount': 30,
    'bill_date': now,
    'created': now,
    'modified': now,
    'name': 'Clocks',
    'payment_code': '123-12345-4444-666666-123455-1234-13221',
    'user': '/a/api/user/1/'
}

url = "http://" + base_url + "/a/api/billingrecord/"
json_data = json.dumps(data)                       #json-fy the data
headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/html'}  #Add headers (necessary for POSTS)
request = urllib2.Request(url, json_data, headers)        #create the request object
response = urllib2.urlopen(request)                       #open the url request object and capture the response
output = response.read()                                  #read the string response
print output

