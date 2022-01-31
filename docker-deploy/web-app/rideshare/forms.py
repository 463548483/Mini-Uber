from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from rideshare.models import Rides,sharer_search

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)
        
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class ClaimRideForm(forms.Form):
        class Meta:
                model = Rides
                fields = ['destination','arrive_date','number_passenger','share','vehicle_type','special_request', 'status']

        def send_email(self):
                # send email using the self.cleaned_data dictionary
                pass

class SharerUpdateForm(forms.ModelForm):
        class Meta:
                model = sharer_search
                fields = ['destination','number_passenger']

