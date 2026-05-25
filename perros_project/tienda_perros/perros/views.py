from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Perro
from django.db.models import Q
from django.shortcuts import render



def home_page(request):
    return render(request, "perros/index.html")

# CONVERTIR OBJETO A JSON
def perro_json(perro):

    return {
        "id": perro.id,
        "nombre": perro.nombre,
        "raza": perro.raza,
        "edad": perro.edad,
        "tamaño": perro.tamaño,
        "peso": perro.peso,
        "color": perro.color,
        "vacunado": perro.vacunado,
        "adoptado": perro.adoptado,
        "energia": perro.energia,
        "genero": perro.genero
    }


# HOME
def inicio(request):

    return JsonResponse({
        "message": "Esta es una pagina de Tienda de perros que permite encontrar perros por raza, edad, tamaño, etc. Hecha por: Samuel Dominguez"
    }, status=200)


# 1. GET /dogs/
def listar_perros(request):

    perros = Perro.objects.all()

    # FILTROS

    min_age = request.GET.get("min_age")
    max_age = request.GET.get("max_age")
    vacunado = request.GET.get("vaccinated")
    tamaño = request.GET.get("size")
    adoptado = request.GET.get("adopted")
    ordering = request.GET.get("ordering")

    if min_age:
        perros = perros.filter(edad__gte=min_age)

    if max_age:
        perros = perros.filter(edad__lte=max_age)

    if vacunado:
        perros = perros.filter(
            vacunado=vacunado.lower() == "true"
        )

    if tamaño:
        perros = perros.filter(
            tamaño__iexact=tamaño
        )

    if adoptado:
        perros = perros.filter(
            adoptado=adoptado.lower() == "true"
        )

    if ordering:
        perros = perros.order_by(ordering)

    data = [perro_json(p) for p in perros]

    return JsonResponse({
        "message": "Perros encontrados",
        "total": len(data),
        "data": data
    }, status=200)


# 2. GET /dogs/1/
def obtener_perro(request, id):

    try:

        perro = Perro.objects.get(id=id)

        return JsonResponse({
            "message": "Perro Econtrado",
            "data": perro_json(perro)
        }, status=200)

    except Perro.DoesNotExist:

        return JsonResponse({
            "error": "Perro no encontrado"
        }, status=404)


# 3. GET /dogs/breed/pug/
def perros_por_raza(request, raza):

    perros = Perro.objects.filter(
        raza__iexact=raza
    )

    data = [perro_json(p) for p in perros]

    return JsonResponse({
        "message": "Perros filtrados por raza",
        "total": len(data),
        "data": data
    }, status=200)


# 4. GET /dogs/search/wal/
def buscar_perro(request, nombre):

    perros = Perro.objects.filter(
        nombre__icontains=nombre
    )

    data = [perro_json(p) for p in perros]

    return JsonResponse({
        "message": "Resultados de la busqueda",
        "total": len(data),
        "data": data
    }, status=200)


# 5. ENDPOINT PERSONALIZADO
# GET /dogs/adoptable/
def perros_adoptables(request):

    perros = Perro.objects.filter(
        adoptado=False
    )

    data = [perro_json(p) for p in perros]

    return JsonResponse({
        "message": "Perros disponibles para adopcion",
        "total": len(data),
        "data": data
    }, status=200)