from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'status', 'is_paid', 'created_at']
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class AssignDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery_man']
