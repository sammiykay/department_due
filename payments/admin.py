from django.http import HttpResponse
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Student)
admin.site.register(Balance)
admin.site.register(Session)
admin.site.register(DepartmentFee)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'amount', 'date_paid', 'transaction_id')

    def generate_csv_report(self, request, queryset):
        report_data = "Student, Session, Amount, Date Paid, Transaction ID\n"
        for payment in queryset:
            report_data += f"{payment.student}, {payment.session}, {payment.amount}, {payment.date_paid}, {payment.transaction_id}\n"

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="payment_report.csv"'
        response.write(report_data)
        return response

    actions = ['generate_csv_report']

admin.site.register(Payment, PaymentAdmin)