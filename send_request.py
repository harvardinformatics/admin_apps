import sys
import urllib, urllib2
import json
from datetime import datetime
import base64

url = sys.argv[1]                                #make the url the first argument passed to this script
password = sys.argv[2]

request = urllib2.Request(url)                   #create the url request object
base64string = base64.encodestring('%s:%s' % ('billyidol', password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
response = urllib2.urlopen(request)              #open the url request object and capture the response

output = response.read()                         #read the string response
json_output = json.loads(output)                 #load the string into a json object
print json.dumps(json_output, sort_keys=True, indent=4, separators=(', ', ': '))   #spit out the json object, formatted
