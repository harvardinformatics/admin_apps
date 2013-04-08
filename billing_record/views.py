from django.shortcuts import render_to_response
from django.http import HttpResponse
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth import logout
from django.template import RequestContext, loader, Context
from billing_record.models import *
from datetime import datetime, date, timedelta
from django.utils.timezone import utc
from django_xhtml2pdf import utils
import re

def get_br_context(request, filters=None):
    #get all bills
    dd = {}
    brs = BillingRecord.objects.all().order_by('-bill_date')
    for key, value in filters.iteritems():
        if key == 'expense_code':
            brs = brs.filter(payment_code=value)
        if key == 'ec_root':
            brs = brs.filter(payment_code__endswith=value)
        if key == 'year':
            year = int(value)
            year_start = datetime(year, 1, 1).replace(tzinfo=utc)
            year_end = datetime(year + 1, 1, 1).replace(tzinfo=utc)
            brs = brs.filter(bill_date__gte=year_start, bill_date__lt=year_end)
        if key == 'month':
            month = int(value)
            if 'year' in filters.keys():
                year = filters['year']
            else:
                year = datetime.now().replace(tzinfo=utc).year
            month_start = datetime(year, month, 1).replace(tzinfo=utc)
            next_month = month + 1
            if next_month == 13:
                next_month = 1
                year = year + 1
            month_end = datetime(year, next_month, 1).replace(tzinfo=utc)
            brs = brs.filter(bill_date__gte=month_start, bill_date__lt=month_end)
    return Context({ 'brs': brs })

#@login_required
def index(request):
    filters = check_querystring(request)
    dd = get_br_context(request, filters)
    template = 'billing/index.html'
    return render_to_response('billing/index.html', 
                              dd, 
                              context_instance=RequestContext(request))

#@login_required
def pdf(request):
    filters = check_querystring(request)
    dd = get_br_context(request, filters)
    template = 'billing/index_pdf.html'
    return utils.render_to_pdf_response('billing/index_pdf.html', dd)

def check_querystring(request):
    filters = {}
    for key, value in request.GET.iteritems():
        if key == "expense_code":
            #check to make sure expense code looks like this: 123-12345-4444-666666-123455-1234-13221
            pattern = re.compile('(\d{3})-(\d{5})-(\d{4})-(\d{6})-(\d{6})-(\d{4})-(\d{5})')
            if pattern.match(value):
                filters.update({ key: value })
        if key == "ec_root":
            #check to make sure expense code looks like this: 123-12345-4444-666666-123455-1234-13221
            pattern = re.compile('(\d{5})')
            if pattern.match(value):
                filters.update({ key: value })
        if key == "year":
            #check to make sure expense code looks like this: 123-12345-4444-666666-123455-1234-13221
            pattern = re.compile('(\d{4})')
            if pattern.match(value):
                filters.update({ key: value })
        if key == "month":
            #check to make sure expense code looks like this: 123-12345-4444-666666-123455-1234-13221
            pattern = re.compile('(\d{1,2})')
            if pattern.match(value):
                filters.update({ key: value })
    return filters
