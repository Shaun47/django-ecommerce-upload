from email import message
from urllib import request
from django.shortcuts import redirect, render
from .models import Account
from django import forms
from django.contrib import messages

from accounts.forms import RegistrationForm

# Create your views here.
def register(request):
    form = RegistrationForm(request.POST)

    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        print(first_name)
        last_name = form.cleaned_data['last_name']
        phone_number = form.cleaned_data['phone_number']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        username = email.split("@")[0]
        user = Account.objects.create_user(first_name = first_name,last_name=last_name,email=email,username=username,password = password)
        user.phone_number = phone_number 
        user.save()
        messages.success(request, 'registration successful')
        return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html',context)

    

def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return 



def clean(self):
    cleaned_data = super(RegistrationForm, self).clean

    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password != confirm_password:
        raise forms.ValidationError(
            "password does not match! "
        )
