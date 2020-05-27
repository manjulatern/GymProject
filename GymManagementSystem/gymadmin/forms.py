from django import forms
from django.core.exceptions import ValidationError
from gyms.models import Gym,User

class GymForm(forms.Form):

	name = forms.CharField(max_length=200)
	location = forms.CharField(max_length=200)
	price = forms.IntegerField(label="Average Cost")
	summary = forms.CharField(widget=forms.Textarea,required=False)
	featured_photo = forms.ImageField(required=False)
	latitude = forms.FloatField(widget=forms.HiddenInput,required=False)
	longitude = forms.FloatField(widget=forms.HiddenInput,required=False)
	user = forms.IntegerField(help_text="Please enter a valid User Id. This will be changed in future.")

	def clean_price(self):
		price = self.cleaned_data['price']
		if price < 200:
			raise ValidationError("Price can't be less than {}.".format(price))
		# Always return the data
		return price

	def clean_user(self):
		user_id = self.cleaned_data['user']
		user = User.objects.filter(pk=user_id).first()

		return user


	def save(self):

		gym = Gym.objects.create(
			name = self.cleaned_data["name"],
			location = self.cleaned_data["location"],
			price = self.cleaned_data["price"],
			summary = self.cleaned_data["summary"],
			featured_photo = self.cleaned_data["featured_photo"],
			user = self.cleaned_data["user"],
			latitude = self.cleaned_data["latitude"],
			longitude = self.cleaned_data["longitude"]
			)
		return gym