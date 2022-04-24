from base64 import urlsafe_b64decode, urlsafe_b64encode
from distutils.log import error
from email import message
from email.policy import default
import imp
from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Account
from django import forms
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from accounts.forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

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

        #user activation
        current_site = get_current_site(request)
        mail_subject = 'Please activate your account'
        message = render_to_string('accounts/account_verification_email.html',
        {
            'user' : user,
            'domain': current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)  ),
            

        }
        )
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



def activate(request):
    return


def forgotpassword(request):
    if request.method == 'POST':

        email = request.POST['email']
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__iexact=email)

            current_site = get_current_site(request)
            mail_subject = 'Please activate your mail'
            message = render_to_string('accounts/reset_password_email.html',{
            'user':user,
            'domain':current_site,
            # 'uid': urlsafe_b64encode(force_bytes(user.pk)),
            'uid': user.pk,
            'token': default_token_generator.make_token(user),
            })
            


            # return HttpResponse(message)



            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email])
            send_email.send()

            messages.success(request, 'Password reset email was sent to your mail address'),   
            
            return redirect('login')  
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgotpassword')
    return render (request, 'accounts/forgotpassword.html')


def resetpassword_validate(request,uid,token):
   
    try:
        #  uid = urlsafe_base64_decode(uid)
         user = Account._default_manager.get(pk=uid) 
        

    except(TypeError, ValueError,OverflowError, Account.DoesNotExist):
        user = None
      


    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
    
        messages.success(request,"please reset your password")
        return redirect('resetPassword')

    else:
        messages.error(request,'This link has been expired')
        return redirect('resetPassword')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"Password has been reseted successfully")
            return redirect('login')
        else:
            messages.error("Password do not match")
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')