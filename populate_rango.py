import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page
#When importing django models, make sure you have imported your project's settings by importing django and
#setting the environment variable DJANGO_SETTINGS_MODULE to be your projects settings file.
#Then call django.setup to import your Django project's settings.
#You need to do this stuff before importing your models because we first need to initialise our Django
#infrastructure

#run the population script everytime this is modified

#what is going on is essentially a series of function calls to two small
#functions, add_page(), and add_cat() defined towards the end of the module.
#Reading through the code, we find that execution starts at the bottom of the module
#above the execution, we define functions; these are not executed unless we call
#them. we call on the defined populate() function in execution at the bottom.
def populate():
    #First we will create lists of dictionaries containing the pages
    #we want to add into each category
    #Then we will create a dictionary of dictionaries for our categories.
    #Allows us to iterate through each data structure, and add the data to our models.

    python_pages = [
        {"title": "Official Python Tutorial",
         "url":"http://docs.python.org/2/tutorial/",
         "views": 200},
        {"title":"How to Think like a Computer Scientist",
         "url":"http://www.greenteapress.com/thinkpython/",
         "views": 300},
        {"title":"Learn Python in 10 Minutes",
         "url":"http://www.korokithakis.net/tutorials/python/",
         "views":400} ]
    
    django_pages = [
        {"title":"Official Django Tutorial",
         "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "views": 40},
        {"title":"Django Rocks",
         "url":"http://www.djangorocks.com/",
         "views": 30},
        {"title":"How to Tango with Django",
         "url":"http://www.tangowithdjango.com/",
         "views": 1000} ]

    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/",
         "views": 50},
        {"title":"Flask",
         "url":"http://flask.pocoo.org",
         "views": 100} ]
    #each key/value pairing represents the name of the category as the key, and
    #an additional dictionary containing additional information relating to the
    #category as the value.
    cats = {"Python": {"pages": python_pages, "views":128, "likes":64},
            "Django": {"pages": django_pages, "views":64, "likes":32},
            "Other Frameworks": {"pages": other_pages, "views":32, "likes":16} }
    #If you want to add more categories or pages, add them to the dictionaries above.

    #The code below goes through the cats dictionary, then adds each category,
    #and then adds all the associated pages for that category.
    #add_cat() and add_page() are responsible for the creation of new categories and pages
    #the function populate() keeps tabs on categories that are created.
    #A reference to a new category is stores in local variable c. This is stored because a Page (in order to be added)
    #requires a Category reference. After add_cat and add_page are called inside this populate function we
    #are in, the function concludes by looping through all new Category and associated Page objects, displaying
    #their names.
    for cat, cat_data in cats.items():
        #cat is the key (python, django, other) and cat_data is the value so
        #to access value you would do cat_data["pages"]
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    #Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


#in the two functions below, we make use of the get_or_create() method for creating model instances
#and because we don't want to create duplicates of the same entry. it removes a lot of repetitive code for us.
#it checks if the entry exists in the database
#if it doesn't exist, the get_or_create() method creates it. if it does exist, then a reference to the specific model
#instance is returned
def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

#Start execution here!
if __name__== '__main__':
    #code within a conditional if __name__=='__main__' statement will only be executed when the module is run as a
    #standalone Python script. Importing the module will not run this code; any classes or functions will
    #however be fully accessible to you. 
    print("Starting Rango population script...")
    populate()
    
