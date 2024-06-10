from django.db import models

class Payment(models.Model):
    ref = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    is_success = models.BooleanField(default=False)

    def __str__(self):
        return self.name