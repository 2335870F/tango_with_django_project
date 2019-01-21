from django.conf.urls import url
from rango import views

urlpatterns=[
#the mapping in tango_with_django_project/urls.py looks for URL strings that match the patterns ^rango/. When 
#a match is made the remainder of the URL string is then passed onto and handled by rango.urls, this file, through the 
#use of the other urls.py file's include() function 
    url(r'^$', views.index, name='index'),
    #map the about() view to /rango/about/
    url(r'^about/', views.about, name='about'),
    #url(r'^about/$', views.about, name='about'),
]
