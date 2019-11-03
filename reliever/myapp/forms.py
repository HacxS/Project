from django.forms import ModelForm
from django import forms
# from .models import doctor
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.files.images import get_image_dimensions

class user_registration_form(UserCreationForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(max_length =200, help_text='Required')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name', 
            'email',
            'gender',
            'password1',
            'password2',
        ]

class user_login_form(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    # def get_absolute_url(self):
    #     return reverse('music:user_login')
    class Meta:
        model = User
        fields = [
            'username', 'password'
        ]


class doctor_registration_form(UserCreationForm):
    email = forms.CharField(max_length =200, help_text='Required')

    profile_photo = forms.ImageField()
    specialization = forms.CharField(max_length=200)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField( choices=GENDER_CHOICES)

    address = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name', 
            'email',
            
            'profile_photo',
            'specialization',
            'gender',
            
            'address',
            'password1',
            'password2',
        ]

class doctor_login_form(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    # def get_absolute_url(self):
    #     return reverse('music:user_login')
    class Meta:
        model = User
        fields = [
            'username', 'password'
        ]

class EditProfileForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password'
        ]
