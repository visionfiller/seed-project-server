from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store.name} favorited by {self.customer.get_full_name()}'
