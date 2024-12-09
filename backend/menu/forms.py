from django import forms
from django.forms import inlineformset_factory
from .models import Menu, Topping
from django.forms import modelformset_factory


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["name", "image", "ingredients", "is_toast"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "ingredients": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    # You can also override `__init__` if needed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "DELETE": forms.CheckboxInput(attrs={"class": "delete-checkbox"}),
        }


# ToppingFormSet = modelformset_factory(
#     Topping, form=ToppingForm, extra=1, can_delete=True
# )
