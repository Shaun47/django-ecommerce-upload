from email import message
from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Account
from django import forms
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from accounts.forms import RegistrationForm

# Create your views here.
def register(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
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
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            # messages.success(request,'You are not logged in')
            return redirect('dashboard')
            
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')


def clean(self):
    cleaned_data = super(RegistrationForm, self).clean

    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password != confirm_password:
        raise forms.ValidationError(
            "password does not match! "
        )
