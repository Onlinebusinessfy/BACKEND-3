from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializers import (
    BookSerializer,
    RegisterSerializer,
    UserSerializer,
)
from .permissions import IsAdmin, IsLibrarianOrAdmin
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

class HomeView(APIView):

    def get(self, request):
        return Response({
            "mensaje": "API Biblioteca funcionando correctamente"
        })


# -----------------------------
# Registro de usuarios
# -----------------------------
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# -----------------------------
# Usuario autenticado
# -----------------------------
class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)


# -----------------------------
# Libros
# -----------------------------
class BookListCreateView(ListCreateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):

        if self.request.method == "POST":
            return [IsAuthenticated(), IsLibrarianOrAdmin()]

        return [IsAuthenticated()]


# -----------------------------
# Editar / Eliminar libro
# -----------------------------
class BookDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):

        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsAdmin()]

        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated(), IsLibrarianOrAdmin()]

        return [IsAuthenticated()]


# -----------------------------
# Lista de usuarios
# -----------------------------
class UserListView(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# -----------------------------
# Asignar rol
# -----------------------------
class AssignRoleView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, id):

        try:
            user = User.objects.get(id=id)

        except User.DoesNotExist:

            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        role = request.data.get("role")

        if role not in ["ADMIN", "LIBRARIAN", "CLIENT"]:

            return Response(
                {"error": "Rol inválido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group, created = Group.objects.get_or_create(name=role)

        user.groups.clear()
        user.groups.add(group)

        return Response(
            {
                "message": "Rol actualizado correctamente",
                "user": user.username,
                "role": role,
            }
        )