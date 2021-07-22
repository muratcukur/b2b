from django import forms

class LoginForm(forms.Form):
	#TIP_CHOICES = (
    #    ('Depot', 'Depot'),
    #    ('Supplier', 'Supplier'),
    #)

	username = forms.CharField(max_length = 220)
	password = forms.CharField(max_length = 220, widget = forms.PasswordInput)
	#tip = forms.ChoiceField(choices=TIP_CHOICES)
	#email = forms.EmailField(required=False)

	def clean(self):
		data = self.cleaned_data

		username = data.get('username')
		password = data.get('password')
		#tip = data.get('tip')
		#email = data.get('email')

		#optional logic for custom validation

		return data