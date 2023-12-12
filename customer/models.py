
from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            last_customer = Customer.objects.order_by('-id').first()
            if last_customer:
                self.id = last_customer.id + 1
            else:
                self.id = 1
        super().save(*args, **kwargs)

