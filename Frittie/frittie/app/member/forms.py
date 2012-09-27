from django import forms
from django.contrib.auth.models import User
from frittie.app.main.models import Member, USA_STATES, GENDER
from django.utils import html
from frittie.helper.common_helper import setup_constant_day, setup_constant_month, setup_constant_year

DAY = setup_constant_day()
MONTH = setup_constant_month()
YEAR = setup_constant_year()

# Not done yet - Need to test and modify more
class SettingForm(forms.Form):
	username = forms.CharField(label='Username',max_length=50,widget=forms.TextInput())
	first_name = forms.CharField(label='FirstName',max_length=50,widget=forms.TextInput())
	last_name = forms.CharField(label='LastName',max_length=50,widget=forms.TextInput())
	email = forms.EmailField(label='Email',max_length=100,widget=forms.TextInput())
	gender = forms.CharField(label='Gender',required=False,max_length=10,widget=forms.Select(choices=GENDER))
	basic_info = forms.CharField(label='Basic_Info',required=False,max_length=200,widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}))
	birthdate_day = forms.CharField(label='Birthdate_Day',required=False,max_length=2,widget=forms.Select(choices=DAY))
	birthdate_month = forms.CharField(label='Birthdate_Month',required=False,max_length=1,widget=forms.Select(choices=MONTH))
	birthdate_year = forms.CharField(label='Birthdate_Year',required=False,max_length=4,widget=forms.Select(choices=YEAR))
	avatar = forms.ImageField(label='Avatar',required=False)
	city = forms.CharField(label='City',required=False,max_length=100)
	state = forms.CharField(label='State',required=False,max_length=2,widget=forms.Select(choices=USA_STATES))