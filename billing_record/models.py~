from django.db import models
from datetime import datetime
from django.utils.timezone import utc
from django.contrib.auth.models import User
#from payment_type.models import PaymentType

# Create your models here.

class BillingRecord(models.Model):
    #logo_path = os.path.join(STATIC_ROOT, 'logos')
    name = models.CharField(max_length=100, default="", null=False)
    #payment_type = models.ForeignKey(PaymentType)
    payment_code = models.CharField(max_length=50, default="", null=False)
    amount = models.PositiveIntegerField(default=0)
    bill_date = models.DateTimeField(null=False, default=datetime.utcnow().replace(tzinfo=utc))
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True, null=False, default=datetime.utcnow().replace(tzinfo=utc))
    modified = models.DateTimeField(auto_now=True, null=False, default=datetime.utcnow().replace(tzinfo=utc))

    def __unicode__(self):
        return self.name
