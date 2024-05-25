from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, ResetPasswordForm
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

import logging

logger = logging.getLogger(__name__)


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('events:list-events')
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('login')	


	else:
		return render(request, 'userauth/login.html', {})
	

def logout_user(request):
	logout(request)
	messages.success(request, ("You Were Logged Out..."))	
	return redirect('events:list-events')



def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)

			recipient_email = [request.POST.get('email')]

			email_subject = 'Welcome to EventHub'
			email_body = f'Hi {username}, thank you for registering in EventHub.ca'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email]
			send_mail(email_subject, email_body, email_from, recipient_email, fail_silently=True)

			messages.success(request, ("Registration Successful!"))
			return redirect('events:list-events')
		
	else:
		form = RegisterUserForm()


	return render(request, 'userauth/register_user.html', 
			   {'form': form})



def reset_password(request):
    form = ResetPasswordForm()  # Initialize form outside the condition
    
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  # Assuming the form has an 'email' field
            
            # Check if a user with the provided email exists
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(bytes(user.pk)).decode()
                
                # Generate the reset password URL
                reset_url = f"http://{request.get_host()}/reset/{uid}/{token}/"
                
                # Prepare the email
                email_subject = 'Reset your password'
                email_body = f'Hi,\n\nPlease use the following link to reset your password:\n\n{reset_url}\n\nThank you.'
                email = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_HOST_USER, recipient_list=[user.email])
                email.send()
                
                messages.success(request, ("Your password-reset instructions have been sent."))
            else:
                messages.warning(request, ("We couldn't find an account with that email address. Please try again."))

            return redirect('events:list-events')
    
    context = {"form": form}
    return render(request, 'userauth/reset_password.html', context)



# def reset_password(request):
	
# 	form = ResetPasswordForm()

# 	context = {
# 		"form": form
# 	}

# 	return render(request, 'userauth/reset_password.html', context)



# def reset_password_confirm(request, uidb64, token):
#     User = get_user_model()
#     try:
#         # Decode the user ID from base64
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     # Check the token
#     if user is not None and default_token_generator.check_token(user, token):
#         # Render the password reset form
#         return render(request, 'userauth/password_reset_confirm.html')
#     else:
#         # Return an error response
#         return render(request, 'userauth/password_reset_invalid_link.html')