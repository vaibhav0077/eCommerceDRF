from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerUpdateView(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer