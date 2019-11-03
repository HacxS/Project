from django.conf.urls import url
from . import views
import django
app_name = 'myapp'

urlpatterns =[
    
    # /music/
    url(r'^$', views.index, name='index'),
    
    # /music/register/
    url(r'^user_registration/$', views.user_registration, name='user_registration'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    # /music/user_login/
    url(r'^user_login/$', views.user_login, name='user_login'),
    # /music/user_logout/
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    
     # /music/register/
    url(r'^doctor_registration/$', views.doctor_registration, name='doctor_registration'),
    # /music/user_login/
    url(r'^doctor_login/$', views.doctor_login, name='doctor_login'),
    # /music/user_logout/
    url(r'^doctor_logout/$', views.doctor_logout, name='doctor_logout'),
    
    url(r'^view_profile/$', views.view_profile, name='view_profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    # # /music/21
    # url(r'^(?P<album_id>\d+)/$', views.details, name='details'),
    # # music/21/favourite_album/
    # url(r'^(?P<album_id>\d+)/favourite_album/$', views.favourite_album, name='favourite_album'),
    # # /music/21/favourite_song/
    # url(r'^(?P<album_id>\d+)/favourite_song/(?P<song_id>\d+)/$', views.favourite_song, name='favourite_song'),
    # # /music/album/create/
    # url(r'^album/create/$', views.add_album, name='add_album'),
    # # /music/21/add_song/
    # url(r'^(?P<album_id>\d+)/add_song/$', views.add_song, name='add_song'),
    # # /music/21/update_album/
    # url(r'(?P<album_id>\d+)/update_album/$', views.update_album, name='update_album'),
    # # /music/21/update_song/1/
    # url(r'(?P<album_id>\d+)/update_song/(?P<song_id>\d+)/$', views.update_song, name='update_song'),
    # # /music/21/delete_album/
    # url(r'(?P<album_id>\d+)/delete_album/', views.delete_album, name='delete_album'),
    # # /music/21/delete_song/1/
    # url(r'^(?P<album_id>\d+)/delete_song/(?P<song_id>\d+)/$', views.delete_song, name='delete_song'),
    
    
    # # /music/register/
    # url(r'^register/$', views.register, name='register'),
    # # /music/user_login/
    # url(r'^user_login/$', views.user_login, name='user_login'),
    # # /music/user_logout/
    # url(r'^user_logout/$', views.user_logout, name='user_logout'),
    # # /music/all_songs/
    # url(r'^all_songs/$', views.all_songs, name='all_songs'),

]