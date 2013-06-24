from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.template import RequestContext, loader, Context
from billing_record.models import *
from billing_record.get_records import get_records
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
import base64
import cStringIO

def get_br_context(request, filters=None):
    #get all bills
    dd = {}
    brs = BillingRecord.objects.all().order_by('-bill_date')
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
                year = filters['year']
            month_start = datetime(year, month, 1).replace(tzinfo=utc)
            display_filters.update({ 'month': month_start });
            next_month = month + 1
            if next_month == 13:
                next_month = 1
                year = year + 1
            month_end = datetime(year, next_month, 1).replace(tzinfo=utc)
            brs = brs.filter(bill_date__gte=month_start, bill_date__lt=month_end)
    total = brs.aggregate(Sum('amount'))['amount__sum']
    if not total:
        total = 0
    return Context({ 'brs': brs, 'total': total, 'display_filters': display_filters, })

@login_required
@csrf_exempt
def index(request):
    filters = check_querystring(request)
    dd = get_br_context(request, filters)
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
            #check to make sure expense code looks like this: 123-12345-4444-666666-123455-1234-13221
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
    user_url = 'http://dokken.rc.fas.harvard.edu/a/api/user/?format=json&username=%s' % username
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

@csrf_exempt
def create_doc(request):
    source_url = "http://%s/%s/?%s%s" % (request.get_host(), "billing", 'format=json&', request.META['QUERY_STRING'])

    username = 'helium' #move this later
    password = 'h3l1um' #move and change this later

    try:
        user_info = get_user_info(username, password)
    except:
        return HttpResponse('No such user')

    user_uri = user_info[0]['resource_uri']
    name_list = []
    if 'month' in request.GET:
        name_list.append(date(2013, int(request.GET['month']), 1).strftime("%b"))
    if 'year' in request.GET:
        name_list.append(date(request.GET['year'], 1, 1).strftime("%Y"))
    else:
        name_list.append(date.today().strftime("%Y"))
    if 'expense_code' in request.GET:
        name_list.append("Exp. Code: %s" % request.GET['expense_code'])
    if 'ec_root' in request.GET:
        name_list.append("Exp. Code Root: %s" % request.GET['ec_root'])
    name = ', '.join([v for v in name_list])
        
    now = str(datetime.utcnow().replace(tzinfo=utc))  #format now as a string

    data = {
        'name':  name,
        'user': user_uri,
        'url': source_url,
        'created': now,
        'modified': now,
        }
    json_data = json.dumps(data)                          #json-fy the data

    #create the django object
    destination_url = 'http://dokken.rc.fas.harvard.edu/a/api/document/'
    request = urllib2.Request(destination_url)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json, text/html')
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    request.add_data(json_data)
    response = urllib2.urlopen(request)

    try:
        location = re.search( r'Location: (.+)$', response.headers.__str__(), re.M)
    except:
        return HttpResponse('No URI!')
    location = location.group(1)
    try:
        uri_id = re.search( r'http://dokken.rc.fas.harvard.edu/a/api/document/(\d+)/', location, re.M)
    except:
        return HttpResponse('No ID!')
    uri_id = uri_id.group(1)

    #create the pdf
    destination_url = 'http://dokken.rc.fas.harvard.edu/harvard_doc/pdf/%s/' % uri_id
    request = urllib2.Request(destination_url)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json, text/html')
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)                       #this request creates the pdf on dokken

    #get the pdf from dokken
    destination_url = 'http://dokken.rc.fas.harvard.edu/uploads/%s.pdf' % slugify(name)
    pdf = urllib2.urlopen(destination_url)
    output = cStringIO.StringIO()
    output.write(pdf.read())
    response = HttpResponse(output.getvalue(), content_type="application/pdf")
    output.close()
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % slugify(name)
    return response

""" No longer used
@csrf_exempt
def generate_doc(request, file_format='html'):
    if not file_format in ('html', 'pdf'):
        file_format = 'html'
    url = 'http://dokken.rc.fas.harvard.edu/harvard_doc/' + file_format + '/'
    request_url = ''.join(['http://', request.get_host(), request.get_full_path()]) 
    data = urllib.urlencode({
            'request_url': request_url,
            })
    req = urllib2.Request(url, data)
    #req.add_data(json_data)
    #req.add_data(data)
    #req.add_header('Content-Type', 'application/json')
    #req.add_header('Accept', 'application/json, text/html')
    #username = request.user.username
    #password = request.user.password
    #base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    #req.add_header("Authorization", "Basic %s" % base64string)

    #response = urllib2.urlopen(req)                       #open the url request object and capture the response
    response = urllib.urlopen(url, data)                       #open the url request object and capture the response
    output = response.read()                                  #read the string response
    print output
    return render_to_response('billing/index.html', data, context_instance=RequestContext(request))

"""
