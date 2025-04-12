from django.shortcuts import render, redirect
from .models import Order
from menu.models import Menu, Topping
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from lunch.utils import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from django.utils.timezone import localtime
def order_menu(request, menu_id):
    if not request.user.is_authenticated:
        return redirect("account_login")  # Redirect to the Allauth login page
    
    menu = Menu.objects.get(id=menu_id)
    toppings = Topping.objects.filter(menu=menu)
    
    if request.method == "POST" and  is_lunch_period_valid(request.user, get_current_period()):
        print(is_lunch_period_valid(request.user, get_current_period()))
        selected_toppings = request.POST.getlist("toppings")
        is_toasted = "is_toasted" in request.POST
        order = Order.objects.create(
            user=request.user, menu=menu, is_toasted=is_toasted
        )
        order.toppings.set(selected_toppings)
        order.save()
        print('hergeroerkgergergergoekrver')
        return redirect("order_success", order_id=order.id)

    return render(request, "order_menu.html", {"menu": menu, "toppings": toppings})

from django.shortcuts import render
from .models import Order


def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "success.html", {"order": order})


from django.shortcuts import render, redirect
from .models import Order
from menu.models import Menu, Topping

@login_required
def view_orders(request):
    pending_orders = Order.objects.filter(
        is_completed=False
    )  # Orders not yet marked as done
    completed_orders = Order.objects.filter(
        is_completed=True
    )  # Orders already marked as done
    context = {"pending_orders": pending_orders, "completed_orders": completed_orders}
    return render(request, "view_orders.html", context)


def mark_order_completed(request, order_id):
    order = Order.objects.get(id=order_id)
    order.is_completed = True
    order.completed_at = timezone.now()
    order.save()

    # Send WebSocket message to the specific user
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{order.customer.id}_notifications',
        {
            'type': 'send_order_completed',
            'order_id': order.id,
            "completed_at": localtime(order.completed_at).strftime("%I:%M %p"),
        }
    )


    return redirect("view_orders")

def order_detail(request, order_id):
    order = Order.objects.get(id = order_id)
    return render(request, 'order_detail.html', {"order":order})

@login_required
def kitchen_delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Ensure only the owner or an admin can delete
    # if request.user == order.customer or request.user.is_staff:
    if request.user:
        order.delete()
        return redirect("view_orders")  # Redirect to the orders page after deletion
    else:
        return redirect("view_orders")  # Redirect if unauthorized
    

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # if request.user == order.customer or request.user.is_staff:
    if request.user == order.customer or request.user.is_staff:
        order.delete()

    previous_url = request.META.get('HTTP_REFERER')

    if previous_url:
        return redirect(previous_url)  # Redirect to the previous page
    else:
        return redirect("view_orders")