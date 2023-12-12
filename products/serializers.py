from rest_framework import serializers
from .models import Product, Order, OrderItem
from datetime import date


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def to_internal_value(self, data):
        product_id = data.get('product')
        if product_id is not None and isinstance(product_id, int):
            try:
                product_instance = Product.objects.get(pk=product_id)
                if data.get('quantity') * product_instance.weight > 150:
                    raise serializers.ValidationError(
                        "Order cumulative weight must be under 150kg.")
                data['product'] = product_instance
                return data
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Product with ID {product_id} does not exist.")
        return super().to_internal_value(data)


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date',
                  'address', 'order_item', 'order_number']
        read_only_fields = ['order_number']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_item')
        order = Order.objects.create(**validated_data)

        cumulative_weight = 0

        for order_item_data in order_items_data:
            product = order_item_data['product']
            quantity = order_item_data['quantity']

            if product.weight > 25:
                raise serializers.ValidationError(
                    "Product weight cannot be more than 25kg.")

            cumulative_weight += product.weight * quantity

            OrderItem.objects.create(order=order, **order_item_data)

        if cumulative_weight > 150:
            raise serializers.ValidationError(
                "Order cumulative weight must be under 150kg.")

        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_item')
        order = instance

        cumulative_weight = 0

        for order_item_data in order_items_data:
            product = order_item_data['product']
            quantity = order_item_data['quantity']

            if product.weight > 25:
                raise serializers.ValidationError(
                    "Product weight cannot be more than 25kg.")

            cumulative_weight += product.weight * quantity

            OrderItem.objects.update(order=order, **order_item_data)

        if cumulative_weight > 150:
            raise serializers.ValidationError(
                "Order cumulative weight must be under 150kg.")

        return order

    def validate_order_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Order date cannot be in the past.")
        return value
