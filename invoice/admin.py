from django.contrib import admin
from invoice.models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'bill_month', 'expense_code_root')
    
admin.site.register(Invoice, InvoiceAdmin)
