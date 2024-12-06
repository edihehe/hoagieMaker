from django.shortcuts import render, redirect
from .models import Order
from menu.models import Menu, Topping
from django.contrib.auth.decorators import login_required


@login_required
def order_menu(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    toppings = Topping.objects.filter(menu=menu)

    if request.method == "POST":
        selected_toppings = request.POST.getlist("toppings")
        is_toasted = "is_toasted" in request.POST
        order = Order.objects.create(
            user=request.user, menu=menu, is_toasted=is_toasted
        )
        order.toppings.set(selected_toppings)
        order.save()
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


def view_orders(request):
    pending_orders = Order.objects.filter(
        is_completed=False
    )  # Orders not yet marked as done
    completed_orders = Order.objects.filter(
        is_completed=True
    )  # Orders already marked as done
    context = {"pending_orders": pending_orders, "completed_orders": completed_orders}
    return render(request, "view_orders.html", context)


# Mark order as complete (by a cook or admin interface)
def mark_order_completed(request, order_id):
    order = Order.objects.get(id=order_id)
    order.mark_as_completed()
    return redirect("view_orders")
