from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User



class Product(models.Model):
    name = models.CharField(max_length=100)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField(validators=[
        MinValueValidator(0.00), MaxValueValidator(17500.00)])
    description = models.TextField()
    quantity = models.IntegerField()
    favorited_by = models.ManyToManyField(User, through="Favorite", related_name="favorited_by")
    image_path = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name='products')


    @property
    def average_rating(self):
        """Average rating calculated attribute for each product
        Returns:
            number -- The average rating for the product
        """
       
        try:
            ratings = self.ratings.all()
            total_rating = 0
            for rating in ratings:
                total_rating += rating.score

            avg = total_rating / self.ratings.count()
            return avg
        except ratings.DoesNotExist:
            total_rating=0
            avg = total_rating
            return avg

    def __str__(self):
        return self.name
    @property
    def is_favorited(self):
        """liked by setter"""
        return self.__is_favorited
    @is_favorited.setter
    def is_favorited(self, value):
        self.__is_favorited = value
