from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet,
    ProductViewSet,
    OrderViewSet,
    OrderItemViewSet
)

router = DefaultRouter()

router.register(
    r'customers',
    CustomerViewSet
)

router.register(
    r'products',
    ProductViewSet
)

router.register(
    r'orders',
    OrderViewSet
)

router.register(
    r'orderitems',
    OrderItemViewSet
)

urlpatterns = router.urls