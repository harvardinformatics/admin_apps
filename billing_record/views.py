from admin_apps.settings import local as settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.template import RequestContext, loader, Context
from billing_record.models import *
from billing_record.get_records import get_records
from invoice.models import Invoice
from datetime import datetime, date, timedelta
from time import sleep
from django.utils.timezone import utc
from django_xhtml2pdf import utils
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify

import logging
log = logging.getLogger(__name__)

#log.debug("doc_id: %s" % document_id)

import re
import sys
import urllib, urllib2
import json
from bs4 import BeautifulSoup
import base64
import cStringIO
from decimal import Decimal

class CreditSummaryAdder:
    def __init__(self, expense_code):
        self.expense_code = expense_code
        self.credit_summary_list = []
        self.billing_record_list = []
        self.total = Decimal("0.0")
        self.brs_total = Decimal("0.0")

    def add_credit_summary(self, credit_summary):
        self.credit_summary_list.append(credit_summary)
        self.total += credit_summary.total_amount_credited

    def add_billing_record(self, billing_record):
        self.billing_record_list.append(billing_record)
        self.brs_total += billing_record.amount

class CreditSummaryManager:
    def __init__(self):
        self.credit_lu = {}  #{ payment_code: CreditSummaryAdder }
    
    def add_record(self, billing_record):
        summary_adder = self.credit_lu.get(billing_record.payment_code, CreditSummaryAdder(expense_code=billing_record.payment_code))
        if billing_record.payment_code not in self.credit_lu.keys():
            summary_adder.add_credit_summary(billing_record.credit_summary)
        summary_adder.add_billing_record(billing_record)
        self.credit_lu.update({summary_adder.expense_code: summary_adder})
        
    def get_credit_summaries(self):
        keys = self.credit_lu.keys()
        keys.sort()
        sorted_list = []
        for k in keys:
            sorted_list.append(self.credit_lu.get(k))
        return sorted_list

def get_br_context(request, filters=None):
    #get all bills
    dd = {}
    #brs = BillingRecord.objects.all().order_by('-bill_date')
    brs = BillingRecord.objects.select_related('credit_summary').all().order_by('-bill_date')
    credit_summary_manager = CreditSummaryManager()
    display_filters = {}

    #initialize the year to be the current year.  If it shows up in the filters, use that instead.
    year = datetime.now().replace(tzinfo=utc).year
    display_filters.update({ 'year': year });
    for key, value in filters.iteritems():
        if key == 'expense_code':
            value = urllib.unquote_plus(value)
            display_filters.update({ 'expense_code': value });
            brs = brs.filter(payment_code=value)
        if key == 'ec_root':
            display_filters.update({ 'ec_root': value });
            brs = brs.filter(payment_code__endswith=value)
            group_name = brs[0].name
            display_filters.update({ 'group_name': group_name });
        if key == 'year':
            display_filters.update({ 'year': value });
            year = int(value)
            year_start = datetime(year, 1, 1).replace(tzinfo=utc)
            year_end = datetime(year + 1, 1, 1).replace(tzinfo=utc)
            brs = brs.filter(bill_date__gte=year_start, bill_date__lt=year_end)
        if key == 'month':
            display_filters.update({ 'month': value });
            month = int(value)
            if 'year' in filters.keys():
                year = int(filters['year'])
            month_start = datetime(year, month, 1).replace(tzinfo=utc)
            display_filters.update({ 'month': month_start });
            next_month = month + 1
            if next_month == 13:
                next_month = 1
                year = year + 1
            month_end = datetime(year, next_month, 1).replace(tzinfo=utc)
            brs = brs.filter(bill_date__gte=month_start, bill_date__lt=month_end)
    brs_total = brs.aggregate(Sum('amount'))['amount__sum']

    credits = []    
    credits_total = 0.0
    for br in brs:
        credit_summary_manager.add_record(br)
        if br.credit_summary not in credits:
            credits.append(br.credit_summary)
            credits_total += float([credit.total_amount_credited for credit in credits][0])

    for csm in credit_summary_manager.get_credit_summaries():
        print csm.__dict__

    if not brs_total:
        brs_total = 0.0
    total_due = float(brs_total) - credits_total
    return Context({ 'brs': brs, 'brs_total': brs_total, 'credit_summary_manager': credit_summary_manager.get_credit_summaries(), 
                     'credits': credits, 'credits_total': credits_total, 'total_due': total_due, 
                     'display_filters': display_filters, })

@login_required
@csrf_exempt
def index(request):
    filters = check_querystring(request)
    #print "filters: %s" % filters
    dd = get_br_context(request, filters)
    #print "dd: %s" % dd
    template = 'billing/index.html'
    return render_to_response('billing/index.html', 
                              dd, 
                              context_instance=RequestContext(request))

#@login_required
def detail(request, billing_record_id):
    br = get_object_or_404(BillingRecord, pk=billing_record_id)
    dd = {'br': br}
    return render_to_response('billing/detail.html', dd, context_instance=RequestContext(request))

#@login_required
def pdf(request):
    filters = check_querystring(request)
    dd = get_br_context(request, filters)
    template = 'billing/index_pdf.html'
    return utils.render_to_pdf_response('billing/index_pdf.html', dd, 'invoice.pdf')

def check_querystring(request):
    filters = {}
    for key, value in request.GET.iteritems():
        if key == "expense_code":
            filters.update({ key: value })
        if key == "ec_root":
            #check to make sure expense code root looks like this: 13221
            pattern = re.compile('(\d{5})')
            if pattern.match(value):
                filters.update({ key: value })
        if key == "year":
            #check to make sure year looks like this: 2013
            pattern = re.compile('(\d{4})')
            if pattern.match(value):
                filters.update({ key: value })
        if key == "month":
            #check to make sure month looks like this: 1, 12
            pattern = re.compile('(\d{1,2})')
            if pattern.match(value):
                filters.update({ key: value })
    return filters

def get_user_info(username, password):
    #get the user from dokken using tastypie
    user_url = 'http://%s/a/api/user/?format=json&username=%s' % (settings.DOCUMENT_APP_HOST, username)
    request = urllib2.Request(user_url)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json, text/html')
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)                       #open the url request object and capture the response
    user_info = json.loads(response.read())                   #read the string response and convert it to json object
    if user_info['meta']['total_count']:
        return user_info['objects']
    return False

def get_doc_version_by_name(doc_name, user_info, username, password):
    """
    Users may create various versions with the same name, "XXXX-v01, XXXX-v02, etc."
    """
    #get the user from dokken using tastypie
    doc_name = urllib.quote(doc_name)
    user_id = user_info[0]['id']

    doc_url = 'http://%s/a/api/document/?format=json&name__startswith=%s&user=%s&order_by=-name&limit=1' \
        % (settings.DOCUMENT_APP_HOST, doc_name, user_id)
    request = urllib2.Request(doc_url)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json, text/html')
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)                       #open the url request object and capture the response
    doc_info = json.loads(response.read())                   #read the string response and convert it to json object
    if doc_info['meta']['total_count']:
        doc_name = doc_info['objects'][0]['name']
        matchObj = re.search( r'-v(\d+)', doc_name, re.M|re.I)
        old_version = int(matchObj.group(1))
        new_version = old_version + 1
        version_string = 'v%02d' % new_version
        return version_string    
    #no matching objects, so default to v01
    return "v01"


@csrf_exempt
def create_doc(request):
    """
    Using the current url, assemble the data to be sent to the document app
    Send the data - the document app will send back a pdf and save copy of the invoice as a html (or just in the database)
    """
    #get the url for the current page, including the querystring
    source_url = "http://%s/%s/?%s%s" % (request.get_host(), "billing", 'format=json&', request.META['QUERY_STRING'])

    #log.debug("source_url: %s" % source_url)

    #get the user object from dokken using username and password
    username = 'helium' #move this later
    password = 'h3l1um' #move and change this later
    try:
        user_info = get_user_info(username, password)
    except:
        return HttpResponse('No such user')
    user_uri = user_info[0]['resource_uri']
    
    #construct the name
    name_list = []
    if 'year' in request.GET:
        year = int(request.GET['year'])
        name_list.append(date(year, 1, 1).strftime("%Y"))
    else:
        name_list.append(date.today().strftime("%Y"))
    month = None
    bill_month = date(date.today().year, date.today().month, 1)
    if 'month' in request.GET:
        month = int(request.GET['month'])
        bill_month = date(date.today().year, month, 1)
        name_list.append(bill_month.strftime("%m"))
    if 'expense_code' in request.GET:
        name_list.append("%s" % request.GET['expense_code'])
    ec_root = None
    if 'ec_root' in request.GET:
        ec_root = request.GET['ec_root']
        name_list.append("%s" % ec_root)
    name = '-'.join([v for v in name_list])

    #get the last version number from the document with this name
    doc_version = get_doc_version_by_name(name, user_info, username, password)
    name = '-'.join([name, doc_version])

    #get the current time
    now = str(datetime.utcnow().replace(tzinfo=utc))  #format now as a string

    #get the html for this page using urllib (is there a better way to do this?)
    sessionid = request.COOKIES['sessionid']
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'sessionid=%s' % sessionid))
    response = opener.open(source_url)
    content = response.read()
    soup = BeautifulSoup(content)
    html = str(soup.find(id="bill_content"))

    data = {
        'name':  name,
        'user': user_uri,
        'html': html,
        'url': source_url,
        'created': now,
        'modified': now,
        }
    json_data = json.dumps(data)                          #json-fy the data

    #create the invoice
    user = User.objects.get(username=username)
    inv = Invoice()
    inv.invoice_number = name
    inv.bill_month = bill_month
    inv.expense_code_root = ec_root
    inv.html_content = html
    inv.user = user
    inv.created = now
    inv.modified = now
    inv.save()

    #create the django object in the document app
    destination_url = 'http://%s/a/api/document/' % settings.DOCUMENT_APP_HOST
    request = urllib2.Request(destination_url)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json, text/html')
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    request.add_data(json_data)
    response = urllib2.urlopen(request)

    #get the uri id for the object that was created
    try:
        location = re.search( r'Location: (.+)$', response.headers.__str__(), re.M)
    except:
        return HttpResponse('No URI!')
    location = location.group(1)
    try:
        uri_id = re.search( r'http://%s/a/api/document/(\d+)/' % settings.DOCUMENT_APP_HOST, location, re.M)
    except:
        return HttpResponse('No ID!')
    uri_id = uri_id.group(1)

    #create the pdf using the uri id
    destination_url = 'http://%s/harvard_doc/pdf/%s/' % (settings.DOCUMENT_APP_HOST, uri_id)
    request = urllib2.Request(destination_url)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json, text/html')
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)                       #this request creates the pdf on dokken

    #get the pdf from dokken
    destination_url = 'http://%s/uploads/%s.pdf' % (settings.DOCUMENT_APP_HOST, slugify(name))
    pdf = urllib2.urlopen(destination_url)
    output = cStringIO.StringIO()
    output.write(pdf.read())
    response = HttpResponse(output.getvalue(), content_type="application/pdf")
    output.close()
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % slugify(name)
    return response
