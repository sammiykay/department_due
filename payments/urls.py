from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('make_payment/', make_payment, name='make_payment'),
    path('student_login/', student_login, name='student_login'),
    path('admin-dashboard/login/', admin_login, name='admin_login'),
    path('logout/', logout_view, name='logout'),
    path('check_payment/', check_payment, name='check_payment'),
    path('make_payment/', make_payment, name='make_payment'),
    path('admin-dashboard/', admin_dashboard , name='admin_dashboard'),
    path('all-payments/', all_payments , name='all_payments'),
    path('make_payments/', make_payments, name='make_payments'),
     path('view-receipts/', view_receipts, name='view_receipts'),
    path('payment_receipt/<int:payment_id>/', payment_receipt, name='payment_receipt'),
    path('create-account/', signup, name='signup'),
    path('all-students/', view_all_students, name='all_students'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('search_payments/', search_payments, name='search_payments'),
    path('department-fee/', department_fee, name='department_fee'),
    path('student-profile/', view_profile, name='student_profile'),
    path('search_students/', search_students, name='search_students'), 
]
