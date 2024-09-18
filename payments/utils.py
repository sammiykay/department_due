from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas

def generate_receipt(payment):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Receipt for {payment.student.user.get_full_name()}")
    p.drawString(100, 780, f"Transaction ID: {payment.transaction_id}")
    p.drawString(100, 760, f"Session: {payment.session}")
    p.drawString(100, 740, f"Amount: {payment.amount}")
    p.drawString(100, 720, f"Date: {payment.date_paid}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
