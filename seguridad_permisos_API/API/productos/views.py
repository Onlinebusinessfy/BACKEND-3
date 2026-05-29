from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Producto
from .serializers import ProductoSerializer
from .permissions import EsDuenoOsoloLectura

class ProductoViewSet(viewsets.ModelViewSet):

    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        EsDuenoOsoloLectura
    ]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)