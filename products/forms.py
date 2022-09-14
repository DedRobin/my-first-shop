from django import forms


class PurchaseForm(forms.Form):
    count = forms.IntegerField(min_value=1)


