from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader

# Function to generate the receipt PDF
def generate_school_fee_receipt(student_name, class_name, receipt_number, amount_paid, date_of_payment, school_name, school_address, school_logo):
    file_name = f"school_fee_receipt_{receipt_number}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    
    # School logo
    if school_logo:
        logo = ImageReader(school_logo)
        c.drawImage(logo, inch, height - 1.5*inch, width=2*inch, preserveAspectRatio=True, mask='auto')
    
    # School name and address
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 0.5*inch, school_name)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2.0, height - 0.75*inch, school_address)

    # Receipt Title
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2.0, height - 1.5*inch, "School Fee Receipt")
    
    # Line
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(inch, height - 1.75*inch, width - inch, height - 1.75*inch)
    
    # Student Details
    c.setFont("Helvetica", 12)
    c.drawString(inch, height - 2.5*inch, f"Student Name: {student_name}")
    c.drawString(inch, height - 3*inch, f"Class: {class_name}")
    c.drawString(inch, height - 3.5*inch, f"Receipt Number: {receipt_number}")
    c.drawString(inch, height - 4*inch, f"Date of Payment: {date_of_payment}")
    c.drawString(inch, height - 4.5*inch, f"Amount Paid: ${amount_paid}")
    
    # Footer
    c.drawString(inch, inch, "Thank you for your payment!")
    
    # Signature section
    c.line(width - 3*inch, 2*inch, width - inch, 2*inch)
    c.drawString(width - 2.5*inch, 1.75*inch, "Authorized Signature")
    
    c.save()
    print(f"Receipt saved as {file_name}")

# Usage
student_name = "John Doe"
class_name = "Grade 10"
receipt_number = "123456"
amount_paid = 500.00
date_of_payment = "2024-10-03"
school_name = "Bright Future School"
school_address = "123 Education Lane, City, Country"
school_logo = "C:\\Users\\Sammiykay\\Desktop\\projects\\DepartmentalDues\\static\\assets\\img\\aaua_logo.png"

generate_school_fee_receipt(student_name, class_name, receipt_number, amount_paid, date_of_payment, school_name, school_address, school_logo)
