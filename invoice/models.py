from django.db import models
from datetime import datetime, date
from django.utils.timezone import utc

# Create your models here.
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, null=True, blank=True)
    bill_month = models.DateField(null=True, blank=True)
    expense_code_root = models.CharField(max_length=5, null=True, blank=True)
    html_content = models.TextField(default="", null=True, blank=True)
    created = models.DateTimeField(null=False, default=datetime.utcnow().replace(tzinfo=utc))
    modified = models.DateTimeField(null=False, default=datetime.utcnow().replace(tzinfo=utc))

    def save(self, *args, **kwargs):
        """
        Save Invoice Number
        """
        if self.pk is None:
            self.created = datetime.utcnow().replace(tzinfo=utc)
        self.modified = datetime.utcnow().replace(tzinfo=utc)
        super(Invoice, self).save(*args, **kwargs)

    def get_bill_month(self):
        """
        look in html content for billing month
        """
        #default to this month
        bill_month = date(date.today().year, date.today().month, 1)
        return bill_month

    def get_expense_code_root(self):
        #placeholder 
        root = '00000'
        return root
    
