from django.db import models
from django.contrib import admin

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    #update the Category model to include the additional atttributes views and likes
    #where the default values for each are both zero (0).
    #if you were to add a new field then you can use the migration tools to update DB
    #To make the migrations for ur app do python manage.py makemigrations rango
    #followed by migrating your DB, committing the changes to the database by issuing python manage.py migrate
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    class Meta:
        #to fix the automatic spelling of plural set to Categorys
        verbose_name_plural='Categories'
    def __str__(self):
        return self.name
    
class Page(models.Model):
    #the field category in model Page is of type ForeignKey. This allows
    #us to create a one-to-many relationship with model/table Category above!
    #which is specified as an argument to the field's constructor
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
#in Python 3, strings are Unicode by default so only need to use __str__
    #method. It generates a string representation of the class.
    #implementing the __str__() methods allows for a display of the string representation
    #of the object

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    
