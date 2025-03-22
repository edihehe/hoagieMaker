from django import forms
from django.forms import inlineformset_factory
from .models import Menu, Topping
from django.forms import modelformset_factory


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = [
            "name",
            "image",
            "ingredients",
            "is_toast",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "aria-label": "Sizing example input",
                    "aria-describedby": "inputGroup-sizing-default",
                }
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "ingredients": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Leave a comment here",
                    "row": 3,
                }
            ),
            "is_toast": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch"}
            ),
            # Specific logic for checkboxes
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ingredients"].widget = forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Leave a comment here",
                "style": "height: 100px",
                "id": "floatingTextarea2",
            }
        )
        self.fields["is_toast"].widget.attrs.update({"class": "form-check-input"})
        # Dynamically set default classes for other fields except `is_toast`.
        for field_name, field in self.fields.items():
            if field_name != "is_toast":  # Skip the checkbox
                field.widget.attrs["class"] = "form-control"
            else:
                # Ensure only the checkbox has its own specific classes
                field.widget.attrs.update({"class": "form-check-input"})


class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ['id',"name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Default input",
                    "aria-label": "Topping's name",
                }
            ),
        }


# ToppingFormSet = modelformset_factory(
#     Topping, form=ToppingForm, extra=1, can_delete=True
# )
