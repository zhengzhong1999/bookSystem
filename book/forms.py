from django import forms
from django.contrib.auth.models import User
from .models import Flight, Customer, Payment


class PassengerInfoForm(forms.Form):
    departure_city = forms.CharField(label='departure_city', max_length=100)
    arrive_city = forms.CharField(label='arrive_city', max_length=100)
    departure_date = forms.DateField(label='departure_date')



class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        exclude = ['user']



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PaymentForm(forms.ModelForm):
   class Meta:
       model = Payment
       fields = ['bank_account']


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['email','name','distance']