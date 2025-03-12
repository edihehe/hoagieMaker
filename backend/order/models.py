from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from menu.models import Menu, Topping


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping)
    is_toasted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)  # To track order status
    completed_at = models.DateTimeField(null=True, blank=True)  # Track completion time
    created_at = models.DateTimeField(default=timezone.now)

    def mark_as_completed(self):
        """Method to mark the order as completed and set timestamp."""
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
            self.save()

    def __str__(self):
        return f"Order by {self.customer.username} for {self.menu_item.name} at {self.created_at} - {'Completed' if self.is_completed else 'Pending'}"
