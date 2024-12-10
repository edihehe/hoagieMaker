from django.shortcuts import render, get_object_or_404, redirect
from .models import Menu, Topping
from .forms import MenuForm, ToppingForm
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from order.models import Order
import json


# List View
def menu_list(request):
    menus = Menu.objects.all()
    return render(request, "menu_list.html", {"menus": menus})


def menu_create(request):
    ToppingFormSet = modelformset_factory(Topping, form=ToppingForm, extra=1)

    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES)
        formset = ToppingFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            menu = form.save()
            toppings = formset.save(commit=False)
            for topping in toppings:
                topping.menu = menu
                topping.save()
            return redirect("menu_list")
    else:
        form = MenuForm()
        formset = ToppingFormSet(queryset=Topping.objects.none())
    return render(
        request,
        "menu_form.html",
        {"form": form, "formset": formset, "action": "Create Menu"},
    )


from order.forms import OrderForm


def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)  # Fetch the specific menu item
    toppings = menu.toppings.all()  # Fetch toppings associated with the specific menu
    is_toasted = (
        "toastOption" in request.POST
    )  # Check if the toasted option is selected

    if request.method == "POST":
        toppings_selected = request.POST.get(
            "toppings", ""
        )  # Selected toppings as a string
        order = Order.objects.create(menu_item=menu, is_toasted=is_toasted)

        if toppings_selected:  # Ensure toppings_selected is not empty
            try:
                topping_ids = [
                    int(tid) for tid in toppings_selected.split(",")
                ]  # Convert to a list of integers
                order.toppings.set(topping_ids)  # Add selected toppings to the order
            except ValueError:
                # Handle invalid topping IDs gracefully
                return render(
                    request,
                    "menu_detail.html",
                    {
                        "menu": menu,
                        "toppings": toppings,
                        "error": "Invalid topping selection.",
                    },
                )

        order.save()
        return redirect("order_success", order_id=order.id)

    return render(
        request,
        "menu_detail.html",
        {
            "menu": menu,
            "toppings": toppings,  # Pass filtered toppings to the template
        },
    )


# Delete View


def menu_delete(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    # Initialize toppings only if needed
    toppings = None

    if hasattr(menu, "toppings"):
        toppings = menu.toppings.all()  # Safe access to toppings if they exist

    if request.method == "POST":
        menu.delete()
        return redirect("menu_list")  # Redirect to a relevant page after deletion

    # Ensure toppings is defined before rendering (even if empty)
    return render(
        request,
        "menu_delete.html",
        {
            "menu": menu,
            "toppings": toppings or [],  # Provide an empty list if toppings is None
        },
    )


import logging

# Set up logging
logger = logging.getLogger(__name__)


def delete_topping(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            topping_id = data.get("topping_id")

            if not topping_id or not topping_id.isdigit():
                return JsonResponse(
                    {"status": "error", "message": "Invalid topping ID."}, status=400
                )

            topping = Topping.objects.get(id=int(topping_id))
            topping.delete()

            return JsonResponse({"status": "success"})
        except Topping.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Topping does not exist."}, status=404
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


# Updated Menu Update Logic to Handle Topping Management
def menu_update(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    # Set up the formset with modelformset_factory
    ToppingFormSet = modelformset_factory(
        Topping, form=ToppingForm, extra=1, can_delete=True
    )

    if request.method == "POST":
        # Handle the main menu form
        form = MenuForm(request.POST, request.FILES, instance=menu)

        # Handle the formset with all submitted data
        formset = ToppingFormSet(
            request.POST, queryset=Topping.objects.filter(menu=menu)
        )

        if form.is_valid() and formset.is_valid():
            # Save the main menu
            form.save()

            # Save only valid toppings (ignore empty ones)
            for topping_form in formset:
                if topping_form.cleaned_data.get("DELETE", False):
                    # Delete the item if marked for deletion
                    if topping_form.instance.pk:
                        topping_form.instance.delete()
                else:
                    # Only save if essential fields are not empty
                    name = topping_form.cleaned_data.get("name")
                    description = topping_form.cleaned_data.get("description")

                    if name or description:  # Ensure at least one field is populated
                        topping = topping_form.save(commit=False)
                        topping.menu = menu
                        topping.save()

            return redirect("menu_list")
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)

    else:
        # Render empty menu with an initialized formset
        form = MenuForm(instance=menu)
        formset = ToppingFormSet(queryset=Topping.objects.filter(menu=menu))

    return render(
        request,
        "menu_form.html",
        {"form": form, "formset": formset, "action": "Update Menu"},
    )
