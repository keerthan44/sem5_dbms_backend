from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    # photo = models.ImageField(upload_to='pics')

roles = (
    ('super admin', "super admin"),
    ('admin', "admin"),
    ('user', "user"),
)
class Roles(models.Model):
    role = models.CharField(max_length=20, choices=roles, default="user")

class UserProfiles(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    contact_email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
