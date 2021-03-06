from django.conf.urls import url
from rango import views

#app_name = 'rango'

urlpatterns=[
    url(r'^$', views.index, name='index'),
    #map the about() view to /rango/about/
    url(r'^about/$', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    #With our new view and associated template created, we can now add in the URL mapping
    url(r'^register/$', views.register, name= 'register'),
    #New pattern! It points the URL /rango/register/ to the register() view!
    #Also note the inclusion of a name for our new URL, register, which we used
    #in the template when we used the url template tag {% url 'register' %}.
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
]

    #now we need to map the add_category view to a URL. In the template we
    #have used the URL /rango/add_category/ in the form's action attribute.
    #We now need to create a mappting from the URL to the view. 
#the mapping in tango_with_django_project/urls.py looks for URL strings that match the patterns ^rango/. When 
#a match is made the remainder of the URL string is then passed onto and handled by rango.urls, this file, through the 
#use of the other urls.py file's include() function

#Django provides the ability to namespace URL configuration modules
#for each individual app that you employ in your project
#adding an app_name variable to your app's urls.py module is enough.
#This then means that any URL you reference from the rango app could be
#done so like "<a href='{% url 'rango:about' %}">About</a> where the colon
#in the url command separates the namespace from the URL name.
#This is an advanced feature for when multiple apps are in presence!
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
