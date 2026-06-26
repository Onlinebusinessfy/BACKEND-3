from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from .models import Product

def home(request):
    return JsonResponse({
        "message": "API de productos funcionando"
    })

# GET /products/ - Listar todos los productos
def list_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = [
            {
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'price': str(p.price),
                'stock': p.stock,
                'is_available': p.is_available,
            }
            for p in products
        ]
        return JsonResponse({'products': data}, status=200, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'error': 'Método no permitido'}, status=405, json_dumps_params={'ensure_ascii': False})


# GET /products/<id>/ - Ver un producto específico
def get_product(request, id):
    if request.method == 'GET':
        product = get_object_or_404(Product, id=id)
        data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'stock': product.stock,
            'is_available': product.is_available,
        }
        return JsonResponse(data, status=200, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'error': 'Método no permitido'}, status=405, json_dumps_params={'ensure_ascii': False})


# POST /products/create/ - Crear un nuevo producto
@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            product = Product.objects.create(
                name=body['name'],
                description=body['description'],
                price=body['price'],
                stock=body['stock'],
                is_available=body.get('is_available', True),
            )
            return JsonResponse({
                'message': 'Producto creado exitosamente',
                'id': product.id,
                'name': product.name,
            }, status=201, json_dumps_params={'ensure_ascii': False})
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({'error': f'Datos inválidos: {str(e)}'}, status=400, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'error': 'Método no permitido'}, status=405, json_dumps_params={'ensure_ascii': False})


# PUT /products/<id>/update/ - Actualizar un producto
@csrf_exempt
def update_product(request, id):
    if request.method == 'PUT':
        product = get_object_or_404(Product, id=id)
        try:
            body = json.loads(request.body)
            product.name = body.get('name', product.name)
            product.description = body.get('description', product.description)
            product.price = body.get('price', product.price)
            product.stock = body.get('stock', product.stock)
            product.is_available = body.get('is_available', product.is_available)
            product.save()
            return JsonResponse({
                'message': 'Producto actualizado exitosamente',
                'id': product.id,
                'name': product.name,
            }, status=200, json_dumps_params={'ensure_ascii': False})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'error': 'Método no permitido'}, status=405, json_dumps_params={'ensure_ascii': False})


# DELETE /products/<id>/delete/ - Eliminar un producto
@csrf_exempt
def delete_product(request, id):
    if request.method == 'DELETE':
        product = get_object_or_404(Product, id=id)
        product.delete()
        return JsonResponse({'message': 'Producto eliminado exitosamente'}, status=200, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'error': 'Método no permitido'}, status=405, json_dumps_params={'ensure_ascii': False})