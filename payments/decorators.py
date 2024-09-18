from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from functools import wraps

# Custom decorator to check if user is a student
def student_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'student'):  # Check if the user has a 'student' attribute (related to Student model)
                return function(request, *args, **kwargs)
            else:
                messages.error(request, "You don't have permission to access this page.")
                return redirect('login')  # Redirect to login or home page if not a student
        else:
            return redirect('login')
    return wrap
