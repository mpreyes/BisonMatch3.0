
from django import forms


class ProfileForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    lnumber = forms.CharField(label="l no", max_length=100)  # Field name made lowercase.
    emailaddress = forms.CharField(label="email add", max_length=100)  # Field name made lowercase.
    gender = forms.CharField(label="Gender", max_length=100)  # Field name made lowercase.
    bio = forms.CharField(label="bio", max_length=256,
        widget=forms.Textarea(),
        help_text='Tell us about yourself!')  # Field name made lowercase. 