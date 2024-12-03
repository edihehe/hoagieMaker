from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="menu_images/")
    ingredients = models.TextField()
    is_toast = models.BooleanField(
        default=False
    )  # Boolean field to indicate if it's toasted

    def __str__(self):
        return self.name


class Topping(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="toppings")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
