from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields.related import ForeignKey



class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(verbose_name="category", max_length=30)
    
    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    imageUrl = models.TextField(max_length=200, null=True)
    isActive = models.BooleanField(default=True)
    createdDate = models.DateField(default=now)
    startPrice = models.FloatField()
    currentPrice = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="related_listings")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_listings")
    buyer = models.ForeignKey(User, on_delete=PROTECT, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

class Bids(models.Model):
    user = ForeignKey(User, on_delete=PROTECT, null=True)
    listing = ForeignKey(Listing, on_delete=PROTECT)
    offerPrice = models.FloatField()
    date = models.DateField(now)



class Comments(models.Model):
    user = ForeignKey(User, on_delete=CASCADE, null=True)
    listing = ForeignKey(Listing, on_delete=CASCADE, null=True, related_name="get_comments")
    content = models.TextField(max_length=200)
    date = models.DateField(default=now)
