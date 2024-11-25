from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Menu
from .forms import MenuForm
from django.shortcuts import render, get_object_or_404


# List View
def menu_list(request):
    menus = Menu.objects.all()
    return render(request, "menu_list.html", {"menus": menus})


# Create View
def menu_create(request):
    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("menu_list")
    else:
        form = MenuForm()
    return render(request, "menu_form.html", {"form": form, "action": "Create Menu"})


def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, "menu_detail.html", {"menu": menu})


# Update View
def menu_update(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            form.save()
            return redirect("menu_list")
    else:
        form = MenuForm(instance=menu)
    return render(request, "menu_form.html", {"form": form, "action": "Update Menu"})


# Delete View
def menu_delete(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        menu.delete()
        return redirect("menu_list")
    return render(request, "menu_confirm_delete.html", {"menu": menu})
