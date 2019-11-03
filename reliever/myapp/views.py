from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import UserSave,Doctor
from .forms import user_registration_form, user_login_form
from .forms import doctor_registration_form, doctor_login_form, EditProfileForm 
from django.contrib.auth import authenticate, login, logout
from django.utils.http import quote_plus
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import cognitive_face as CF
from chatapp.models import ChatSave
from .models import Doctor
from django.contrib.auth.decorators import login_required
# import urllib
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#@login_required(login_url='/myapp')
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'myapp/base_visitor.html', context=None)
    else:
        is_doctor = Doctor.objects.filter(username=request.user)
        if is_doctor:
            is_doctor =True
        else:
            is_doctor = False
        if is_doctor:
            clients = set()
            clts = ChatSave.objects.filter(is_doctor=False)
            for i in clts:
                clients.add(i.from_user)
            context = {
                'username': request.user.get_username(),
                'clients': list(clients),
            }
            print(clients)
            return render(request,'myapp/doctor_index.html',context)
        else:
            docs = get_doctors()
            context = {
            'docs': docs,
                # 'albums': Album.objects.filter(user=request.user),
                'username': request.user.get_username(),
            }
            return render(request, 'myapp/index.html', context)

def user_registration(request):
    form = user_registration_form(request.POST or None, request.FILES or None)
    if form.is_valid():

        if request.method == 'POST':
            username = request.POST['username']

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user = form.save(commit=True)
            # user.is_active = False
            # user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('myapp/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            UserSave(username=username,first_name=first_name,last_name=last_name,email=to_email,gender=request.POST['gender']).save()
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    
            
    else:
        j=0
        context ={}
        for i in form:
            t = 'form'+str(j)
            print(i)
            context[t]=i
            j+=1
        #return render(request, 'myapp/user_registration_form.html')
    return render(request, 'myapp/user_registration_form.html', context=context)


def faceapi():
    key = '559a32ee606a4df9a23230da26c3aa79' # make sure to fill in the key you obtained for Face API
    CF.Key.set(key)
    BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
    CF.BaseUrl.set(BASE_URL)
    img_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmWlPlC8LV_n7rAifQD_CqadRGRIfG4v_Gq4ZBRIII6L7WrCIG"
    result = CF.face.detect(img_url)
    result_faceId = result[0]['faceId']

    test_url = "https://www.dailypioneer.com/uploads/2017/story/images/big/167975_Untitled-19.gif"
    test_result = CF.face.detect(test_url)
    test_faceId = test_result[0]['faceId']
    ans = CF.face.verify(result_faceId, test_faceId)
    return ans

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        login(request, user)
        return redirect('myapp:index')
    else:
        return HttpResponse('Activation link is invalid!')


# def user_registration(request):
#     form = user_registration_form(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user.set_password(password)
#         user.save()
#         return redirect('myapp:user_login')
#     return render(request, 'myapp/user_registration_form.html', context={'form': form, 'caption':'register',})

def user_login(request):
    #form = user_login_form(request.POST or None)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('myapp:index')
                #return render(request, 'myapp/index.html')

            else:
                return render(request, 'myapp/user_login_form.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'myapp/user_login_form.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'myapp/user_login_form.html')

def user_logout(request):
    logout(request)
    return redirect('myapp:index', permanent=True)

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'myapp/profile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('myapp:view_profile'))
        else:
            return redirect(reverse('myapp:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'myapp/change_password.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('myapp:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'myapp/edit_profile.html', args)

def doctor_registration(request):
    form = doctor_registration_form(request.POST or None, request.FILES or None)
    # print(form.error_messages)
    if form.is_valid():
        _,ext = request.FILES['profile_photo'].content_type.split('/')
        if request.method == 'POST':
            file = request.FILES['profile_photo']
            
            username = request.POST['username']
            with open('myapp/media/'+username+'.'+ext, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            profile_photo = request.FILES['profile_photo']
            print(request.POST)

            # print(profile_photo.name)
            # print(profile_photo.size)
            user = form.save(commit=True)
            # user.is_active = False
            # user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('myapp/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            Doctor(username=username,first_name=first_name,last_name=last_name,email=to_email,gender=request.POST['gender'],address=request.POST['address'],specialization=request.POST['specialization']).save()
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    
            
    else:
        j=0
        context ={}
        for i in form:
            t = 'form'+str(j)
            print(i)
            context[t]=i
            j+=1
        #return render(request, 'myapp/user_registration_form.html')
    return render(request, 'myapp/doctor_registration_form.html', context=context)

def doctor_login(request):
    form = doctor_login_form(request.POST or None)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('myapp:index')
                
            else:
                return render(request, 'myapp/doctor_login_form.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'myapp/doctor_login_form.html', {'form': form, 'error_message': 'Invalid login'})
    return render(request, 'myapp/doctor_login_form.html', {'form': form,})

def doctor_logout(request):
    logout(request)
    return redirect('myapp:index', permanent=True)

def get_doctors():
    doctors =Doctor.objects.all()
    doc = []
    for i in doctors:
        doc.append(i.username)
    return doc




# def index(request):
#     if not request.user.is_authenticated:
#         return render(request, 'music/login_form.html', {'form': login_form(None)})
#     else:
#         context = {
#             'albums': Album.objects.filter(user=request.user),
#             'username': request.user.get_username(),
#         }
#         return render(request, 'music/index.html', context)

# def details(request, album_id):

#     album = get_object_or_404(Album, pk=album_id)
#     # share_string = quote_plus(album.album_title)
#     context = {
#         'album':album,
#         # 'share_string':share_string,
#     }
#     return render(request, 'music/details.html', context)

# def favourite_album(request,album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     if album.is_favourite:
#         album.is_favourite = False
#     else:
#         album.is_favourite = True
#     album.save()
#     return redirect('music:index')

# def favourite_song(request, album_id, song_id):
#     album = get_object_or_404(Album, pk=album_id)
#     song = get_object_or_404(Song, pk=song_id)
#     if song.is_favourite:
#         song.is_favourite = False
#     else:
#         song.is_favourite = True
#     song.save()
#     return HttpResponseRedirect(album.get_absolute_url())
#     # try:
#     #     selected_song = get_object_or_404(Song, pk=request.POST['checked'])
#     # except (KeyError, Song.DoesNotExist):
#     #     context = {
#     #         'album': album,
#     #         'error_message':'you did not select the valid song',
#     #     }
#     #     return render(request, 'music/details.html', context)
#     # else:
#     #     selected_song.is_favourite = True
#     #     selected_song.save()
#     #     context = {
#     #         'album':album,
#     #     }
#     #     return HttpResponseRedirect(album.get_absolute_url())

# def add_album(request):
#     if not request.user.is_authenticated:
#         return redirect("music:user_login")
#     else:
#         form = album_form(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             return HttpResponseRedirect(instance.get_absolute_url())
#         context = {
#             'form':form,
#             'caption': 'Add Album',
#         }
#         return render(request, 'music/album_form.html',context)
    
# def add_song(request, album_id):
#     form = song_form(request.POST or None, request.FILES or None)
#     album = get_object_or_404(Album, pk=album_id)
#     if form.is_valid():
#         song_title = request.POST.get('song_title')
#         audio_file = request.FILES.get('audio_file')
#         album.song_set.create(song_title=song_title, audio_file=audio_file)
#         return HttpResponseRedirect(album.get_absolute_url())
#     context = {
#         'form':form,
#         'caption': 'Add Song',
#     }
#     return render(request, 'music/song_form.html', context)

# def update_album(request, album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     form = album_form(request.POST or None, instance=album, files=request.FILES or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         return HttpResponseRedirect(album.get_absolute_url())
#     context = {
#         'form':form,
#         'caption': 'Update Album',
#     }
#     return render(request, 'music/album_form.html',context)

# def update_song(request, album_id, song_id):
#     song = get_object_or_404(Song, pk=song_id)
#     _ = get_object_or_404(Album, pk=album_id)
#     form = song_form(request.POST or None, request.FILES or None, instance=song)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         return HttpResponseRedirect(_.get_absolute_url())
#     context = {
#         'form': form,
#         'caption': 'Update Song',
#     }
#     return render(request, 'music/song_form.html', context)

# def delete_album(request, album_id):
#     album = get_object_or_404(Album, id=album_id)
#     album.delete()
#     return redirect('music:index')

# def delete_song(request, album_id, song_id):
#     album =get_object_or_404(Album, pk=album_id)
#     song = get_object_or_404(Song, pk=song_id)
#     song.delete()
#     return HttpResponseRedirect(album.get_absolute_url())

# def register(request):
#     form = registration_form(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         # username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user.set_password(password)
#         user.save()
#         return redirect('music:user_login')
#     return render(request, 'music/registration_form.html', context={'form': form, 'caption':'register',})

# def user_logout(request):
#     logout(request)
#     return redirect('music:user_login', permanent=True)


# def user_login(request):
#     form = login_form(request.POST or None)
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('music:index')
#             else:
#                 return render(request, 'music/login_form.html', {'error_message': 'Your account has been disabled'})
#         else:
#             return render(request, 'music/login_form.html', {'form': form, 'error_message': 'Invalid login'})
#     return render(request, 'music/login_form.html', {'form': form,})

# def all_songs(request):
#     context ={
#         'albums': Album.objects.all(),
#     }
#     return render(request, 'music/all_songs.html', context)
