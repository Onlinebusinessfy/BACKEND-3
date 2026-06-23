from django.db.models import Sum, Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    Customer,
    Product,
    Order,
    OrderItem
)

from .serializers import (
    CustomerSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False)
    def top_customers(self, request):

        customers = Customer.objects.annotate(
            total_orders=Count("orders")
        ).order_by("-total_orders")

        data = []

        for customer in customers:
            data.append({
                "id": customer.id,
                "name": customer.name,
                "total_orders": customer.total_orders
            })

        return Response(data)


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]

    search_fields = ["name"]

    ordering_fields = [
        "name",
        "price",
        "stock"
    ]

    @action(detail=False)
    def low_stock(self, request):

        products = Product.objects.filter(
            stock__lt=10
        )

        serializer = self.get_serializer(
            products,
            many=True
        )

        return Response(serializer.data)

    @action(detail=False)
    def by_category(self, request):

        category = request.GET.get("category")

        products = Product.objects.filter(
            category=category
        )

        serializer = self.get_serializer(
            products,
            many=True
        )

        return Response(serializer.data)

    @action(detail=False)
    def top_products(self, request):

        products = OrderItem.objects.values(
            "product__name"
        ).annotate(
            sold=Sum("quantity")
        ).order_by("-sold")[:5]

        return Response(products)


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False)
    def date_range(self, request):

        start = request.GET.get("start")
        end = request.GET.get("end")

        orders = Order.objects.filter(
            order_date__range=[start, end]
        )

        serializer = self.get_serializer(
            orders,
            many=True
        )

        return Response(serializer.data)

    @action(detail=False)
    def sales_by_category(self, request):

        sales = OrderItem.objects.values(
            "product__category"
        ).annotate(
            total_sales=Sum("subtotal")
        )

        return Response(sales)


class OrderItemViewSet(viewsets.ModelViewSet):

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer