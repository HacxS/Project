from django.conf.urls import url
from . import views
app_name = 'paytm'

urlpatterns = [
    # Examples:
    url(r'^response/', views.response, name='response'),
]
