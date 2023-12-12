"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from customer.views import (CustomerListCreateView, CustomerUpdateView)
from products.views import (ProductListCreateView,
                            OrderListCreateView,
                            OrderItemCreateView,
                            OrderUpdateView
                            )

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/customers/', CustomerListCreateView.as_view(),
         name='customer-list-create'),
    path('api/customers/<int:pk>/',
         CustomerUpdateView.as_view(), name='customer-update'),
    path('api/products/', ProductListCreateView.as_view(),
         name='product-list-create'),
    path('api/orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('api/order-items/', OrderItemCreateView.as_view(),
         name='order-item-create'),
    path('api/orders/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
]


