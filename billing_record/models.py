from django.db import models
from datetime import datetime
from django.utils.timezone import utc
from django.contrib.auth.models import User
#from payment_type.models import PaymentType

# Create your models here.

class CreditSummary(models.Model):
    name = models.CharField(max_length=50, default="", null=False)
    group = models.CharField(max_length=50, default="", null=False)
    month = models.DateTimeField(null=False, default=datetime(datetime.today().year, datetime.today().month, 1))
    total_amount_credited = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total_cost_of_dewars = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total_volume_recovered = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=False, default=datetime.utcnow().replace(tzinfo=utc))
    modified = models.DateTimeField(auto_now=True, null=False, default=datetime.utcnow().replace(tzinfo=utc))

    def __unicode__(self):
        return "%s - $%s - $%s - %s - %s" % (self.name, str(self.total_amount_credited), 
                                       str(self.total_cost_of_dewars), str(self.total_volume_recovered), self.modified)

class BillingRecord(models.Model):
    #logo_path = os.path.join(STATIC_ROOT, 'logos')
    name = models.CharField(max_length=200, default="", null=False)
    #payment_type = models.ForeignKey(PaymentType)
    credit_summary = models.ForeignKey(CreditSummary, null=True, blank=True, on_delete=models.SET_NULL)
    payment_code = models.CharField(max_length=100, default="", null=False)
    amount = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    bill_date = models.DateTimeField(null=False, default=datetime.utcnow().replace(tzinfo=utc))
    notes = models.TextField(default="", null=True, blank=True)
    user = models.ForeignKey(User)
    external_unique_id = models.CharField(max_length=40, default="", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=False, default=datetime.utcnow().replace(tzinfo=utc))
    modified = models.DateTimeField(auto_now=True, null=False, default=datetime.utcnow().replace(tzinfo=utc))

    def __unicode__(self):
        return "%s - %s - $%s - %s" % (self.name, self.payment_code, str(self.amount), self.bill_date)

