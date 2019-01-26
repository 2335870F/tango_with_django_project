from django.conf.urls import url
from rango import views

urlpatterns=[
#the mapping in tango_with_django_project/urls.py looks for URL strings that match the patterns ^rango/. When 
#a match is made the remainder of the URL string is then passed onto and handled by rango.urls, this file, through the 
#use of the other urls.py file's include() function 
    url(r'^$', views.index, name='index'),
    #map the about() view to /rango/about/
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name='show_category'),
]
    #invokes view.show_category() when the URL pattern in quotes is matched 
    #we have added a parameter name within the URL pattern here. When you
    #create a paramtereised URL you need to ensure that the parameters that you
    #include in the URL are declared in the corrsponding view. The regular
    #expression [\w\-]+) will look for any sequence of alphanumeric characters
    #denoted by \w and any hyphens (-) denoted by \-, and we can match as many
    #of these as we like denoted by the []+ expression
    #The url pattern will match a sequence of alphanumeric characters and
    #hyphens which are between the rango/category/ and the trailing /.
    #This seuqence will be stored in the parameter category_name_slug and
    #passed to views.show_category(). For example, the URL rango/category/python-books/
    #would result in the category_name_slug variable having the value
    #python-books. However if the URL was rango/category/$$$$$-&&&&&/ then the
    #sequence of characters would not match  the regular expression and a 404
    #not found error would result because there would be no matching URL pattern.
