from django import forms

from profiles.models import GENDER_CHOICE


class ProfileForm(forms.Form):
    # email = forms.EmailField()
    # password = forms.CharField()
    gender = forms.ChoiceField(choices=GENDER_CHOICE, required=False)
    first_name = forms.CharField(min_length=1, required=False)
    last_name = forms.CharField(min_length=1, required=False)
    patronymic = forms.CharField(min_length=1, required=False)
    phone_number = forms.CharField(min_length=7, required=False)
    social_network_link = forms.CharField(min_length=1, required=False)
    slug = forms.CharField(min_length=1, required=False)
