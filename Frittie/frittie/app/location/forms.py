from django import forms
from frittie.app.main.models import *

class LocationForm(forms.Form):
    name=forms.CharField(max_length=50)
    description = forms.CharField(required=False,widget=forms.Textarea())
    category = forms.CharField(max_length=20,widget=forms.Select(choices=CATEGORY))
    address1 = forms.CharField(max_length=100)
    address2 = forms.CharField(required=False,max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=2,widget=forms.Select(choices=USA_STATES))
    zip_code = forms.IntegerField()
    avatar = forms.ImageField(required=False) 
