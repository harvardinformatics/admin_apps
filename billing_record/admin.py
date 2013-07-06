from django.contrib import admin
from billing_record.models import BillingRecord, CreditSummary

class BillingRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_code', 'amount', 'bill_date',)
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

class CreditSummaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'month',)

admin.site.register(BillingRecord, BillingRecordAdmin)
admin.site.register(CreditSummary, CreditSummaryAdmin)
