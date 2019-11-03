from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address','email','mobno']


HOSTEL_LIST = (
    (0, ("CVRaman")),
    (1, ("Limbdi")),
)

class OrderCreate(forms.Form):
	name = forms.CharField(label='Name',required=True)
	address = forms.CharField(label='address',required=True)
	email = forms.EmailField(label='Email',required=True)
	mobno = forms.CharField(label='Mobile No.',max_length=17,required=True)


