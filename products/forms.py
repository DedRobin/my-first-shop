from django import forms

ORDER_PRICE_CHOICES = (
    ("", "Empty"),
    ("price", "Price Asc"),
    ("-price", "Price Desc"),
)

ORDER_SOLD_CHOICES = (
    ("", "Empty"),
    ("sold", "Sold Asc"),
    ("-sold", "Sold Desc"),
)

ORDER_POPULAR_CHOICES = (
    ("", "Empty"),
    ("popular", "Popular Asc"),
    ("-popular", "Popular Desc"),
)


class PurchaseForm(forms.Form):
    count = forms.IntegerField(min_value=1)


class ProductsFilterForm(forms.Form):
    price = forms.ChoiceField(choices=ORDER_PRICE_CHOICES, required=False, label="By price")
    sold = forms.ChoiceField(choices=ORDER_SOLD_CHOICES, required=False, label="By sold")
    popular = forms.ChoiceField(choices=ORDER_POPULAR_CHOICES, required=False, label="By popular")
    price_from = forms.IntegerField(required=False)
    price_to = forms.IntegerField(required=False)
