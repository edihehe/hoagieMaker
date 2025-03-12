from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import TemplateView
from menu.models import Menu
from order.models import Order 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render
from menu.models import Menu 


def landing_page(request):
    menus = Menu.objects.all()
    
    if request.user.is_authenticated:
        orders_in_progress = Order.objects.filter(customer=request.user, is_completed=False)
        completed_orders = Order.objects.filter(customer=request.user, is_completed=True)
    else:
        orders_in_progress = None
        completed_orders = None

    return render(
        request,
        "home.html",
        {
            "menus": menus,
            "orders_in_progress": orders_in_progress,
            "completed_orders": completed_orders,
        },
    )

@login_required
def orders(request):
    active_orders = Order.objects.filter(customer=request.user, is_completed=False)
    completed_orders = Order.objects.filter(customer=request.user, is_completed=True)
    return render(request, "orders.html", {
        "active_orders": active_orders,
        "completed_orders": completed_orders
    })
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if order.is_completed:
        messages.error(request, "You cannot cancel a completed order.")
    else:
        order.delete()
        messages.success(request, "Your order has been canceled.")

    return redirect("orders")
def logout_confirm(request):
    return render(request, "logout_confirm.html")


def login(request):
    return render(request, "login.html")


from django.contrib.auth.views import LogoutView


class CustomLogoutView(LogoutView):
    http_method_names = ["get", "post", "head", "options"]
