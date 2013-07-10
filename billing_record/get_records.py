import sys, os, re, json
import httplib2
from datetime import datetime, timedelta
from django.utils.timezone import utc

sys.path.append('/var/www/admin_apps/')
sys.path.append('/Users/ericmattison/code/admin_apps/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_apps.settings.local'

from admin_apps.settings import local as settings
from billing_record.models import BillingRecord, CreditSummary
from django.contrib.auth.models import User
from decimal import Decimal

def get_records(month_string=None):
    all_additions = {}
    cs_added = []
    brs_added = []
    for external_user, external_source in settings.EXTERNAL_SOURCES.iteritems():

        #parse the supplied month, or use the previous month
        #month_string = None
        if not month_string:
            try:
                month_string = sys.argv[1]
            except:
                pass
        try:
            #check if the supplied arg matches "YYYY-mm"
            datestring = month_string + "-01"
            entered_date = datetime.strptime(datestring, "%Y-%m-%d")
            month_string = "=".join(["month", month_string])
        except:
            #get last month
            today = datetime.today()
            first = datetime(year=today.year, month=today.month, day=1)
            last_month = first - timedelta(days=1)
            month_string = "=".join(["month", last_month.strftime("%Y-%m")])

        #get the info from MiniLims
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
        #print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        #for k,v in data.iteritems():
        #    print k,v
        for k,v in data.iteritems():
            group_name = k
            credit_summary = None
            credit_info = None
            if 'Billing_Notes' in v[0]:
                credit_info = v[0]
                #finalized = False
                finalized = True #used only for testing
                if credit_info['Status'] == 'Finalized':
                    finalized = True

                if finalized:
                    month = datetime.strptime(credit_info['Month'] + "-1", '%Y-%m-%d').replace(tzinfo=utc)
                    credit_summary, created = CreditSummary.objects.get_or_create(name=credit_info['Billing_Notes'], 
                                                                                  group=credit_info['Group'],
                                                                                  total_amount_credited=credit_info['Total_Amount_Credited'],
                                                                                  total_cost_of_dewars=credit_info['Total_Cost_Of_Dewars'],
                                                                                  total_volume_recovered=credit_info['Total_Volume_Recovered_(SCF)'],
                                                                                  defaults={'month': month}
                                                                                  )
                    if created:
                        cs_added.append(credit_summary)
                    #print "cs: %s, %s" % (credit_summary, created)

            all_additions.update({'credits': cs_added})

            for item in v[1:]:
                if 'Billing_Record' in item:
                    #finalized = False
                    finalized = True #used only for testing
                    if item['Status'] == 'Finalized':
                        finalized = True

                    if finalized:
                        name = item['Group']
                        payment_code = ": ".join(item['Expense_Code'].split('_:_'))
                        amount = Decimal(item['Dewar_Cost'])
                        bill_date = datetime.strptime(item['Month'] + "-1", '%Y-%m-%d').replace(tzinfo=utc)
                        notes = item['Description'].replace("_", " ").replace("\\", "")\
                            .replace(" %", "%").replace("dollars credit", "dollar credit")
                        user = User.objects.get(username=external_user) #username is the same as the name of the application
                        external_unique_id = item['Billing_Record']
                        br, created = BillingRecord.objects.get_or_create(name=name,
                                                                          credit_summary=credit_summary,
                                                                          payment_code=payment_code,
                                                                          amount=amount,
                                                                          notes=notes,
                                                                          user=user,
                                                                          external_unique_id=external_unique_id,
                                                                          defaults={'bill_date': bill_date})
                        if created:
                            brs_added.append(br)
                        #print "br: %s, %s" % (br, created)
            
            all_additions.update({'billing_records': brs_added})
    return all_additions

if __name__ == '__main__':
    aa = get_records()
    print aa
    #print "Billing Records added: "
    #for br in brs:
    #    print "\t%s, %s, %s, %s" % (br.name, br.payment_code, br.bill_date, br.user)
