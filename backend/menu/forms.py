from django import forms
from django.forms import inlineformset_factory
from .models import Menu, Topping


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["name", "image", "ingredients", "is_toast"]


ToppingFormSet = inlineformset_factory(
    Menu,
    Topping,
    fields=["name"],  # Fields to display for Topping
    extra=1,  # Extra empty forms
    can_delete=True,  # Allow deletion of toppings
)
