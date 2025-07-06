from django.db import models
from accounts.models import CustomUser

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('complete', 'Complete'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    delivery_man = models.ForeignKey(
        CustomUser, null=True, blank=True, on_delete=models.SET_NULL,
        limit_choices_to={'role': 'delivery'}, related_name='assigned_orders'
    )
    description = models.TextField()
    delivery_address = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"
