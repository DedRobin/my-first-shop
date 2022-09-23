from django import forms

ORDER_CHOICES = (
    ("", "Empty"),
    ("favorites", "Favorites"),
    ("cost", "Price Asc"),
    ("-cost", "Price Desc"),
    ("sold", "Sold Asc"),
    ("-sold", "Sold Desc"),
    ("popular", "Popular Asc"),
    ("-popular", "Popular Desc"),
)


class PurchaseForm(forms.Form):
    count = forms.IntegerField(min_value=1)


class ProductsFilterForm(forms.Form):
    order_by = forms.ChoiceField(choices=ORDER_CHOICES, required=False, label="Order by")
    price_from = forms.IntegerField(required=False)
    price_to = forms.IntegerField(required=False)
