from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserViewSet,
    RegisterView,
    ProjectViewSet,
    TaskViewSet,
)

router = DefaultRouter()

router.register(
    "users",
    UserViewSet
)

router.register(
    "projects",
    ProjectViewSet,
    basename="projects"
)

router.register(
    "tasks",
    TaskViewSet,
    basename="tasks"
)

urlpatterns = [
    path("", include(router.urls)),

    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    path(
        "refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
]