"""
URL configuration for sistema_comercial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('entidades/', include('entidades.urls')),
    path('balanza/', include('balanza.urls')),
    path('lotes/', include('lotes.urls')),
    path('laboratorio/', include('laboratorio.urls')),
    path('costos/', include('costos.urls')),
    path('valorizacion/', include('valorizacion.urls')),
    path('liquidaciones/', include('liquidaciones.urls')),
    path('reportes/', include('reportes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
