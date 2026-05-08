# Actividad 1 — Arquitectura y configuración profesional de una REST API

## Materia

Desarrollo de Soft Backend III (Optativa)

## Unidad

Unidad 1: RestAPI

## Objetivo

Diseñar y configurar la estructura base de una REST API aplicando buenas prácticas de arquitectura backend, separación modular y manejo seguro de configuraciones mediante variables de entorno.

---

## Descripción

En esta actividad se realizó la creación de una base profesional para una API REST utilizando Python, Django y Django REST Framework.

Se implementó una estructura modular del proyecto, separación de configuraciones para distintos entornos y manejo seguro de credenciales usando variables de ambiente.

---

## Tecnologías utilizadas

* Python
* Django
* Django REST Framework
* python-dotenv

---

## Parte teórica

### ¿Qué es una REST API?

Una REST API es una interfaz que permite la comunicación entre aplicaciones mediante el protocolo HTTP. Utiliza recursos identificados por URLs y métodos como GET, POST, PUT, PATCH y DELETE.

### Principios REST

#### Stateless

Cada solicitud contiene toda la información necesaria para ser procesada. El servidor no almacena estado entre peticiones.

#### Client–Server

El cliente se encarga de la interfaz y el servidor de la lógica de negocio y acceso a datos.

#### Resource-based architecture

Los datos se organizan en recursos accesibles mediante rutas como:

* `/users`
* `/products`
* `/orders`

---

## Comparaciones

### REST vs SOAP

* REST es más ligero y flexible.
* SOAP es más estructurado y usa normalmente XML.

### API pública vs privada

* API pública: accesible para desarrolladores externos.
* API privada: restringida para uso interno.

### Monolito vs microservicios

* Monolito: toda la aplicación en una sola unidad.
* Microservicios: servicios independientes y desacoplados.

---

## Implementación

### Creación del entorno virtual

```bash
python -m venv venv
```

### Instalación de dependencias

```bash
pip install django djangorestframework python-dotenv
```

### Creación del proyecto

```bash
django-admin startproject config .
python manage.py startapp api
mkdir apps
```

---

## Estructura del proyecto

```text
Desarrollo_Backend_III/
│
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── api/
│   ├── migrations/
│   ├── views.py
│   ├── models.py
│   └── urls.py
│
├── apps/
├── .env
├── .gitignore
├── manage.py
└── README.md
```

---

## Variables de entorno

Se implementaron las siguientes variables en el archivo `.env`:

```env
SECRET_KEY=django-insecure-cambia-esta-llave
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

---

## Seguridad inicial

### Archivo `.gitignore`

```gitignore
venv/
.env
__pycache__/
db.sqlite3
*.pyc
```

### Buenas prácticas aplicadas

* No subir credenciales sensibles al repositorio.
* Separación de configuración por ambiente.
* Rotación básica de llaves de seguridad.

---

## Prueba inicial

Se ejecutó el servidor de desarrollo con:

```bash
python manage.py runserver
```

Accediendo a:

```text
http://127.0.0.1:8000/
```

Lo que permitió verificar que la estructura inicial del proyecto quedó funcionando correctamente.

---

## Conclusión

Durante esta actividad se configuró una base profesional para una REST API aplicando buenas prácticas de organización backend, separación modular, configuración por entornos y manejo seguro de variables sensibles.

Esta estructura permite escalar el proyecto de manera ordenada y facilita futuras implementaciones de endpoints, autenticación y conexión con bases de datos.
