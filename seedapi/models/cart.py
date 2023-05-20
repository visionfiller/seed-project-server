from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    payment_type = models.ForeignKey(
        "PaymentType", on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='carts')
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    products = models.ManyToManyField(
        "Product", through="CartProduct", related_name='carts')
