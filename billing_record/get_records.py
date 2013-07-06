import sys, os, re, json
import httplib2
from datetime import datetime
from django.utils.timezone import utc

sys.path.append('/var/www/admin_apps/')
sys.path.append('/Users/ericmattison/code/admin_apps/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_apps.settings.local'

from admin_apps.settings import local as settings
from billing_record.models import BillingRecord, CreditSummary
from django.contrib.auth.models import User

def get_records():
    brs_added = []
    for external_user, external_source in settings.EXTERNAL_SOURCES.iteritems():

        #parse the month, or use the current month
        month_string = None
        try:
            #check if the supplied arg matches "YYYY-mm"
            datestring = sys.argv[1] + "-01"
            entered_date = datetime.strptime(datestring, "%Y-%m-%d")
            month_string = "=".join(["month", sys.argv[1]])
        except:
            month_string = "=".join(["month", datetime.today().strftime("%Y-%m")])

        url_string = "?".join([external_source, month_string])
        h = httplib2.Http()
        resp, content = h.request(url_string, "GET")
        
        try:
            resp['status'] == '200'
        except:
            print "No response from MiniLims!"
            sys.exit()

        p = re.compile('<pre>')
        json_string = p.split(content)[2].replace("JSON_DATA", "").replace("</pre>", "").strip()
        data = json.loads(json_string)
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        for k,v in data.iteritems():
            print k,v
        for k,v in data.iteritems():
            group_name = k
            credit_summary = None
            credit_info = None
            if 'Total_Amount_Credited' in v[0]:
                credit_info = v[0]
                month = datetime.strptime(credit_info['Month'] + "-1", '%Y-%m-%d').replace(tzinfo=utc)
                credit_summary, created = CreditSummary.objects.get_or_create(name=credit_info['Billing_Notes'], 
                                                                      group=credit_info['Group'],
                                                                      month=month,
                                                                      total_amount_credited=credit_info['Total_Amount_Credited'],
                                                                      total_cost_of_dewars=credit_info['Total_Cost_Of_Dewars'],
                                                                      total_volume_recovered=credit_info['Total_Volume_Recovered_(SCF)']
                                                                      )
                print "cs: %s, %s" % (credit_summary, created)

            for item in v[1:]:
                if 'Status' in item:
                    name = item['Group']
                    payment_code = ": ".join(item['Expense_Code'].split('_:_'))
                    amount = int(round(float(item['Dewar_Cost'])))
                    bill_date = datetime.strptime(item['Month'] + "-1", '%Y-%m-%d').replace(tzinfo=utc)
                    notes = item['Description']
                    user = User.objects.get(username=external_user) #username is the same as the name of the application
                    external_unique_id = item['Billing_Record']
                    br, created = BillingRecord.objects.get_or_create(name=name,
                                                                      credit_summary=credit_summary,
                                                                      payment_code=payment_code,
                                                                      amount=amount,
                                                                      bill_date=bill_date,
                                                                      notes=notes,
                                                                      user=user,
                                                                      external_unique_id=external_unique_id)
                    print "br: %s, %s" % (br, created)


        sys.exit()
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
                brs_added.append(br)
    return brs_added

if __name__ == '__main__':
    brs = get_records()
    #print "Billing Records added: "
    #for br in brs:
    #    print "\t%s, %s, %s, %s" % (br.name, br.payment_code, br.bill_date, br.user)
