# order/models.py
from django.db import models
from django.utils import timezone
from menu.models import Menu, Topping


class Order(models.Model):
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping)
    is_toasted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order for {self.menu_item.name} at {self.created_at}"
