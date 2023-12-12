from django.db import models
from customer.models import Customer
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MaxValueValidator(25)])

class Order(models.Model):
    order_number = models.CharField(max_length=10, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            if last_order:
                order_number = f"ORD{str(last_order.id + 1).zfill(5)}"
            else:
                order_number = "ORD00001"
            self.order_number = order_number
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def clean(self):
        if self.product.weight * self.quantity > 150:
            raise ValidationError("Order cumulative weight must be under 150kg")
