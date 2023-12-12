
from rest_framework import generics
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer
from django.db.models import Q


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_update(self, serializer):
        existing_order = Order.objects.get(pk=self.kwargs['pk'])
        serializer.save()

        existing_order.orderitem_set.all().delete()

        order_items_data = self.request.data.get('order_item', [])
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=existing_order, **order_item_data)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()

        products_param = self.request.query_params.get('products')
        if products_param:
            products_list = products_param.split(',')
            queryset = queryset.filter(
                orderitem__product__name__in=products_list)

        customer_param = self.request.query_params.get('customer')
        if customer_param:
            queryset = queryset.filter(
                customer__name__icontains=customer_param)

        return queryset
