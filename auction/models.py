from django.db import models
from authentication.models import *

# Create your models here.
status = (
    ('not begun', 'not begun'),
    ('started', 'started'),
    ('over', 'over'),
)
class Auction(models.Model):
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    title = models.TextField()
    startDate = models.DateTimeField(null=False, blank=False)
    endDate = models.DateTimeField(null=False, blank=False)
    status = models.CharField(max_length=30, choices=status, default="not_begun")

class Item(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    name = models.TextField()
    image = models.ImageField(upload_to='items', blank=True, null=True)
    description = models.TextField()
    basePrice = models.IntegerField()
    bidCount = models.IntegerField(default = 0)
    

class Bids(models.Model):
    amount = models.FloatField()
    time = models.DateTimeField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=None)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        # Check if the amount is greater than the basePrice
        if self.amount <= self.item.basePrice:
            raise ValueError("Amount must be greater than the basePrice.")

        # Check if the amount is greater than previous bids for the same item
        previous_bids = Bids.objects.filter(item=self.item).exclude(pk=self.pk)
        if previous_bids.exists() and self.amount <= previous_bids.latest('time').amount:
            raise ValueError("Amount must be greater than previous bids for the same item.")

        super().save(*args, **kwargs)