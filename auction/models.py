from django.db import models
from authentication.models import *

# Create your models here.
status = (
    ('not begun', 'not begun'),
    ('started', 'started'),
    ('over', 'over'),
)
class Auction(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.TextField()
    startDate = models.DateTimeField(null=False, blank=False)
    endDate = models.DateTimeField(null=False, blank=False)
    status = models.CharField(max_length=30, choices=status)

class Item(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    name = models.TextField()
    image = models.ImageField(upload_to='items', blank=True, null=True, default=None)
    description = models.TextField()
    basePrice = models.IntegerField()
    bidCount = models.IntegerField(default = 0)
    

class Bids(models.Model):
    amount = models.IntegerField()
    time = models.DateTimeField()

class Bids_Users(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)