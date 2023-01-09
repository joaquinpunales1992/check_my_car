from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MechanicForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(MechanicForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.is_staff = True
		if commit:
			user.save()
		return user



# Create your forms here.
class NewClientForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		import pdb;pdb.set_trace()
		user = super(NewClientForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user