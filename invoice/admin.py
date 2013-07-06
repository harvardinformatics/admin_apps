from django.contrib import admin
from invoice.models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'bill_month', 'expense_code_root', 'user')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()
    
admin.site.register(Invoice, InvoiceAdmin)
