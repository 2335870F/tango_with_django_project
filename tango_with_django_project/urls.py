"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rango import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #this maps the basic URL to the index view in the rango app.
    url(r'^about/', views.about, name='about'),
    #this maps the about/ URL to the about view in the rango app.
    #NOT SURE IF THE ABOUT ONE IS NEEDED BUT SEC 4.4 SAYS SO
    url(r'^rango/', include ('rango.urls')),
    #above maps any URLs starting with rango/ to be handled by the rango application
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#once this is complete, you should be able to serve content from the media
#directory from the /media/ URL.
