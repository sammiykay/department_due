from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    image = models.ImageField()
    faculty = models.CharField(max_length=200)

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def __str__(self):
        return self.user.get_full_name()

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.session} - {self.amount} - {self.date_paid}"


class DepartmentFee(models.Model):
    price = models.IntegerField(default=1500)


class Balance(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    amount_withdraw = models.IntegerField(default=0)
    bank_code = models.CharField(max_length=202, default='')
    account_number = models.CharField(max_length=202, default='')
    bank_name = models.CharField(max_length=200, default='')
    price = models.IntegerField(default=0)
    account_name = models.CharField(max_length=444, default='')