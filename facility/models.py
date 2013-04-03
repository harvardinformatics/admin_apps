from django.db import models
from datetime import datetime
from django.utils.timezone import utc

# Create your models here.

class Facility(models.Model):
    #logo_path = os.path.join(STATIC_ROOT, 'logos')
    name = models.CharField(max_length=100, default="", null=False)
    logo_filename = models.ImageField(upload_to="logos")
    street = models.CharField(max_length=100, default="", null=False)
    street2 = models.CharField(max_length=100, default="", null=True, blank=True)
    city = models.CharField(max_length=30, default="", null=False)
    state = models.CharField(max_length=30, default="", null=False)
    zip = models.CharField(max_length=10, default="", null=False)
    created = models.DateTimeField(auto_now_add=True, null=False, default=datetime.utcnow().replace(tzinfo=utc))
    modified = models.DateTimeField(auto_now=True, null=False, default=datetime.utcnow().replace(tzinfo=utc))

    def __unicode__(self):
        return self.name
