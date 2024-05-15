from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    mobile_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)

    USERNAME_FIELD = 'name'

class Image(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    action = models.CharField(max_length=10)  # 'accept' or 'reject'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} -- {self.image} -- {self.action}'