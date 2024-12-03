# order/forms.py
from django import forms
from menu.models import Menu, Topping
from .models import Order


class OrderForm(forms.ModelForm):
    toppings = forms.ModelMultipleChoiceField(
        queryset=Topping.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    is_toasted = forms.BooleanField(required=False)

    class Meta:
        model = Order
        fields = ["menu_item", "toppings", "is_toasted"]
