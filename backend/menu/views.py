from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Menu, Topping
from .forms import MenuForm, ToppingFormSet
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from order.models import Order


# List View
def menu_list(request):
    menus = Menu.objects.all()
    return render(request, "menu_list.html", {"menus": menus})


def menu_create(request):
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
        formset = ToppingFormSet()
    return render(
        request,
        "menu_form.html",
        {"form": form, "formset": formset, "action": "Create Menu"},
    )


def menu_update(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES, instance=menu)
        formset = ToppingFormSet(request.POST, instance=menu)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("menu_list")
    else:
        form = MenuForm(instance=menu)
        formset = ToppingFormSet(instance=menu)
    return render(
        request,
        "menu_form.html",
        {"form": form, "formset": formset, "action": "Update Menu"},
    )


from order.forms import OrderForm


def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)  # Use pk to fetch the menu item
    toppings = request.POST.getlist("toppings")  # Get the selected toppings
    is_toasted = "toastOption" in request.POST  # Check if toasted option is selected

    if request.method == "POST":
        order = Order.objects.create(menu_item=menu, is_toasted=is_toasted)
        order.toppings.set(toppings)  # Add selected toppings to the order
        order.save()

        return redirect("order_success", order_id=order.id)

    return render(
        request,
        "menu_detail.html",
        {
            "menu": menu,
            "toppings": Topping.objects.all(),  # Optionally, pass available toppings to the template
        },
    )


# Delete View
def menu_delete(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    toppings = get_object_or_404(toppings)
    if request.method == "POST":
        menu.delete()
        return redirect("menu_list")
    return render(request, "menu_confirm_delete.html", {"menu": menu})
