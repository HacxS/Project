from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
# Create your models here.

# def upload_location(doctor, filename):
#     return '%s/%s' %(doctor.id, filename)
    
class Doctor(models.Model):
    # user = models.ForeignKey(on_delete=models.CASCADE, default=1)
    # user   = models.OneToOneField(User, on_delete = models.CASCADE)
    username = models.CharField(max_length =200)
    first_name = models.CharField(max_length =200)
    last_name = models.CharField(max_length =200)
    email = models.CharField(max_length =200)
    is_doctor = models.BooleanField(default=True)
    specialization = models.CharField(max_length=200)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=200)


    def __str__(self):
        return self.username

class UserSave(models.Model):
    username = models.CharField(max_length =200)
    first_name = models.CharField(max_length =200)
    last_name = models.CharField(max_length =200)
    email = models.CharField(max_length =200)
    is_doctor = models.BooleanField(default=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


# models for song lie in particular album
# class Song(models.Model):
#     # album = models.ForeignKey(Album, on_delete=models.CASCADE)
#     song_title = models.CharField(max_length = 200)
#     audio_file = models.FileField()
#     is_favourite = models.BooleanField(default= False)
#     def __str__(self):
#         return self.song_title    


