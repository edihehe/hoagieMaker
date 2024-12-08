from django import forms
from django.forms import inlineformset_factory
from .models import Menu, Topping


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["name", "image", "ingredients", "is_toast"]


class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}
