import sys, os, json
import httplib2
from datetime import datetime
from django.utils.timezone import utc

sys.path.append('/var/www/admin_apps/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_apps.settings.local'

from admin_apps.settings import local as settings
from billing_record.models import BillingRecord
from django.contrib.auth.models import User

if __name__ == '__main__':
    for k,v in settings.EXTERNAL_SOURCES.iteritems():
        h = httplib2.Http()
        resp, content = h.request(v, "GET")
        data = json.loads(content)
        already_entered = BillingRecord.objects.exclude(external_unique_id='')
        already_entered_ids = [br.external_unique_id for br in already_entered]
        for item in data['Billing_Record']:
            if not item['Billing_Record'] in already_entered_ids: # don't re-enter
                name = item['Group']
                payment_code = ": ".join(item['Expense_Code'].split('_:_'))
                amount = int(round(float(item['Amount'])))
                bill_date = datetime.strptime(item['Delivery_Date'], "%Y-%m-%d").replace(tzinfo=utc)
                notes = item['Description']
                user = User.objects.get(username=k) #username is the same as the name of the application
                external_unique_id = item['Billing_Record']
                
                br = BillingRecord(name=name,
                                   payment_code=payment_code,
                                   amount=amount,
                                   bill_date=bill_date,
                                   notes=notes,
                                   user=user,
                                   external_unique_id=external_unique_id)
                br.save()
                print "Entered %s" % br
