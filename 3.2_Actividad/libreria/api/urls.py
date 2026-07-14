from django.urls import path
from .views import LoginView

from .views import (
    RegisterView,
    MeView,
    BookListCreateView,
    BookDetailView,
    UserListView,
    AssignRoleView,
)

urlpatterns = [

    path("register/", RegisterView.as_view(), name="register"),

   path("login/", LoginView.as_view()),

    path("me/", MeView.as_view(), name="me"),

    path("books/", BookListCreateView.as_view(), name="books"),

    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),

    path("users/", UserListView.as_view(), name="users"),

    path(
        "users/<int:id>/assign-role/",
        AssignRoleView.as_view(),
        name="assign-role",
    ),
]