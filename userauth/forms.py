from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):	
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
		widgets = {
            'username': forms.TextInput(attrs={'class': 'register-form'}),
            'first_name': forms.TextInput(attrs={'class': 'register-form'}),
            'last_name': forms.TextInput(attrs={'class': 'register-form'}),
            'email': forms.TextInput(attrs={'class': 'register-form'}),
            'password1': forms.TextInput(attrs={'class': 'register-form'}),
            'password2': forms.TextInput(attrs={'class': 'register-form'}),
        }


	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'



class ResetPasswordForm(UserCreationForm):	
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('email',)
		widgets = {
            'email': forms.TextInput(attrs={'class': 'register-form'}),
        }


	# def __init__(self, *args, **kwargs):
	# 	super(PasswordResetForm, self).__init__(*args, **kwargs)

	# 	self.fields['email'].widget.attrs['class'] = 'form-control'
	