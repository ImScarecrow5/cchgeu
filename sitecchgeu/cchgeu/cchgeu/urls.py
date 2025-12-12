"""
URL configuration for cchgeu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from ed_programms import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'education'

product_patterns = [
    path('', views.index, name='index'),
]


urlpatterns = [
    path('', views.index, name='index'),
    path('get-faculty-programs/', views.get_faculty_programs, name='get_faculty_programs'),
    path('vizitka/', views.vizit, name='vizit'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)