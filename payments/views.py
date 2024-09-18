from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import *
from .forms import *
import uuid
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.pdfgen import canvas
from .utils import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import re
from .decorators import *
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from xhtml2pdf import pisa
import io
from django.conf import settings
from django.core.files import File



def total_money_paid():
    total_paid = Payment.objects.aggregate(total_amount=Sum('amount'))['total_amount']
    print(total_paid)
    if total_paid == None:
        return 0
    return total_paid

def validate_password(password):
    # Check if the password has at least one capital letter, one number, and one character
    if (len(password) >= 8 and
        re.search(r'[A-Z]', password) and  # At least one capital letter
        re.search(r'[a-z]', password) and  # At least one lowercase letter
        re.search(r'[0-9]', password)):    # At least one number
        return True
    else:
        return False
def generate_receipt_reportlab():
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="receipt.pdf"'  # 'attachment' to download

    # Create a PDF using ReportLab
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Details for the receipt
    matric_number = "190404061"
    session = "2024/2025"
    amount = "N1500"
    date_paid = "2024/03/20 9:40 PM"
    transaction_id = "3874292037984297"
    generated_on = datetime.now().strftime('%Y/%m/%d %I:%M %p')

    # Header
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2.0, height - 50, "Payment Receipt")

    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2.0, height - 75, "Thank you for your payment!")

    # Payment Details
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 120, "Payment Details:")

    p.setFont("Helvetica", 12)
    p.drawString(100, height - 150, f"Matric Number: {matric_number}")
    p.drawString(100, height - 170, f"Session: {session}")
    p.drawString(100, height - 190, f"Amount: {amount}")
    p.drawString(100, height - 210, f"Date Paid: {date_paid}")
    p.drawString(100, height - 230, f"Transaction ID: {transaction_id}")

    # Footer
    p.setFont("Helvetica", 10)
    p.drawString(100, height - 300, f"Receipt generated on: {generated_on}")
    p.drawString(100, height - 320, "Contact us at support@university.edu for any inquiries.")

    # Close the PDF object
    p.showPage()
    p.save()

    return response

@login_required
@student_required
def home(request):
    if request.user.student:
        payment = Payment.objects.filter(student = request.user.student)
        total_payment = len(payment) * int(DepartmentFee.objects.first().price)
        total_payment_receipt = len(payment)
        context = {
            'total_payment': total_payment,
            'total_payment_receipt': total_payment_receipt,
        }
    else:
        context = {

        }
    return render(request, 'index.html', context)


def check_payment(request):
    student = Student.objects.get(user=request.user)
    sessions = Session.objects.all()
    session = request.POST.get('session')
    if request.method == 'POST':
        if Payment.objects.filter(student=student, session=Session.objects.get(id = session)).exists():
            return JsonResponse({'status': 'error', 'message': 'You have already paid for this session.'}, status=400)
        else:
            return JsonResponse({'status': 'continue', 'message': 'Proceed'}, status=200)


@login_required
@student_required
def make_payment(request):
    student = Student.objects.get(user=request.user)
    sessions = Session.objects.all()
    fee = DepartmentFee.objects.first()
    print(request.POST)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        session = request.POST.get('session')
        session=Session.objects.get(id = session)
        payment = Payment.objects.create(amount=fee.price, session=session,transaction_id=str(uuid.uuid4()), student=student)
        generate_pdf_receipt(payment)
        return JsonResponse({'status': 'success', 'payment_id': payment.id, 'message': 'Payment successful!'})
        # else:
        #     return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
    
    form = PaymentForm()
    paystack_key = 'pk_test_108c33e6b3e38e5c4d919275f4b25331e484691e'
    return render(request, 'make_payment.html', {'form': form, 'sessions': sessions, 'paystack_key': paystack_key, 'normal_fee':fee.price, 'fee':fee.price * 100})




@csrf_exempt
def make_payments(request):
    student = Student.objects.get(user=request.user)
    sessions = Session.objects.all()
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        print(request.POST)
        session = request.POST.get('session')
        print(session)
        if Payment.objects.filter(student=student, session=Session.objects.get(id = session)).exists():
            return JsonResponse({'status': 'error', 'message': 'You have already paid for this session.'})
        else:
            payment = Payment()
            payment.session = Session.objects.get(id = session)
            payment.student = student
            payment.amount = 1500  # Set the fixed price here
            payment.transaction_id = str(uuid.uuid4())
            payment.save()
            # Generate receipt here
            receipt_buffer = generate_receipt(payment)
            payment.receipt.save(f"receipt_{payment.transaction_id}.pdf", ContentFile(receipt_buffer.read()), save=True)
            return JsonResponse({'status': 'success', 'payment_id': payment.id, 'message': 'Payment successful!'})
        # else:
        #     return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
    
    form = PaymentForm()
    return render(request, 'make_payment.html', {'form': form, 'sessions': sessions})

@login_required
@student_required
def payment_receipt(request, payment_id):
    payment = Payment.objects.get(id=payment_id, student__user=request.user)
    return render(request, 'payment_receipt.html', {'payment': payment})


def generate_pdf_receipt(payment):
    # Create absolute image URLs
    aaua_logo_url = settings.STATIC_URL + 'assets/img/aaua_logo.png'
    qr_code_url = settings.STATIC_URL + 'assets/img/qr_code.png'
    print(qr_code_url)
    # Render HTML template with context
    html_string = render_to_string('reciept.html', {
        'payment': payment,
        'aaua_logo_url': aaua_logo_url,
        'qr_code_url': qr_code_url,
        'watermark_image_url': aaua_logo_url
    })
    
    # Generate the PDF file
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html_string), dest=pdf_buffer)
    
    if not pisa_status.err:
        pdf_buffer.seek(0)
        payment_receipt_name = f'receipt_{payment.transaction_id}.pdf'
        payment.receipt.save(payment_receipt_name, ContentFile(pdf_buffer.getvalue()))
        payment.save()
    
    pdf_buffer.close()

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = StudentLoginForm()
    return render(request, 'student_login.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_staff:
            auth_login(request, user)
            return JsonResponse({'status': 'Success', 'message': 'Login successful'}, status = 200)
        else:
            return JsonResponse({'status': 'Warning', 'message': 'Invalid admin ID or password'}, status = 400)
    return render(request, 'admin_login.html')

@login_required
@student_required
def view_receipts(request):
    student = Student.objects.get(user=request.user)
    
    payments = Payment.objects.filter(student=student)
    return render(request, 'view_receipts.html', {'payments': payments, 'pk_public': 'FLWPUBK-22da3de668f7f84d3e13138c33945409-X'})

@login_required
@student_required
def view_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        faculty = request.POST.get('faculty')
        print(request.POST)
        user = User.objects.get(username=request.user.username)
        user.first_name=name
        user.email=email
        user.save()
        student = Student.objects.get(user=user)
        student.department=department
        print(request.FILES)
        student.faculty=faculty
        student.save()
        try:
            image = request.FILES['image']
            student.image.save(image.name, File(image)), 
        except:
            pass
        # return 
    payments = Payment.objects.filter(student=student)
    return render(request, 'student_profile.html', {'student': student, 'pk_public': 'FLWPUBK-22da3de668f7f84d3e13138c33945409-X'})



def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    student = Student.objects.all()
    payment = Payment.objects.all()
    student_length = len(student)
    payment_length = len(payment)
    payments = Payment.objects.all().order_by('date_paid')[:6]

    context = {
        'student': student,
        'student_length': student_length,
        'payment_length': payment_length,
        'payments': payments,
        'total_payment': total_money_paid(),
    }
    return render(request, 'admin_dashboard.html', context = context)


def search_payments(request):
    query = request.GET.get('q', '')
    payments = Payment.objects.filter(student__matric_number__icontains=query)

    # Render the payments into HTML and send it back as the response
    html = render_to_string('payment_table_rows.html', {'payments': payments})
    
    return JsonResponse(html, safe=False)

@login_required
@user_passes_test(lambda u: u.is_staff)
def all_payments(request):
    payments = Payment.objects.all().order_by('-date_paid')  # Order payments by most recent first
    paginator = Paginator(payments, 10) 

    # Get the current page number from the request
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_payments': paginator.count,
        'start_index': page_obj.start_index(),
        'end_index': page_obj.end_index(),
    }

    return render(request, 'all_payments.html', context=context)


def view_my_receipts(request):
    return render(request, 'receipt.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def view_all_students(request):
    students = Student.objects.all()  # Retrieve all students
    paginator = Paginator(students, 9)  # 9 students per page

    # Get the current page number from the request
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj,
    }
    return render(request,'all_students.html', context= context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def department_fee(request):
    departmentfee = DepartmentFee.objects.first()  # Retrieve all students
    if request.method == 'POST':
        fee = request.POST.get('fee')
        print(fee)
        departmentfee.price = int(fee)
        departmentfee.save()
    context = {
        'departmentfee':departmentfee,
    }
    return render(request,'departmentfee.html', context= context)





def search_students(request):
    query = request.GET.get('q', '')
    # Filter students by matric number or name (case insensitive)
    students = Student.objects.filter(matric_number__icontains=query) | Student.objects.filter(user__first_name__icontains=query)

    # Render the student grid into HTML and send it back as the response
    html = render_to_string('student_grid.html', {'students': students})
    return JsonResponse(html, safe=False)




# Signup View
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        name = request.POST.get('name')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        department = request.POST.get('department')
        faculty = request.POST.get('faculty')
        print(request.POST)
        image = request.FILES['image']
        print(password1)
        print(password2)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'Warning', 'message':'Matric number already exist. Please Login'}, status = 400)
        elif password1 != password2:
            return JsonResponse({'status': 'Warning', 'message':'Password Does not match'}, status = 400)
        elif not validate_password(password1):
            return JsonResponse({'status': 'Warning', 'message': 'Password must contain at least one capital letter, one lowercase letter, one number, and be at least 8 characters long'}, status = 400)

        try:
            user = User.objects.create_user(username=username, password=password1, first_name=name, email=email)
            student = Student.objects.create(user=user, matric_number=username, department=department, image=image, faculty=faculty)
            return JsonResponse({'status': 'Success', 'message': 'Account Created'}, status = 200)

        except Exception as e:
            return JsonResponse({'status': 'warning', 'message': f'{e}'}, status = 400)
        return redirect('login')  # Redirect to the login page
    
    return render(request, 'create_account.html')


# Login View
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(request.POST)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            if Student.objects.filter(user=user).exists():
                auth_login(request, user)
                return redirect('home') 
            else:
                return JsonResponse({'status': 'Warning', 'message': f'Invalid matric number or password'}, status = 400)

        else:
            return JsonResponse({'status': 'Warning', 'message': f'Invalid matric number or password'}, status = 400)
    return render(request, 'login.html')

