from django.contrib import admin
from rango.models import Category, Page, UserProfile
#To make the UserProfile model data accesible via the admin web interface


#Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
#Update the registration to include this customised interface CategoryAdmin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
#Now you can register the new model with the admin interface, with the following line
admin.site.register(UserProfile)

#Your database must be updated with the creation of a new model

# Register your models here.
#we want to solve the problems of : if you add in a category via the admin interface, Django requires you fill in the slug field too, so we want to have the slug automatically generated.
#also, the problem of : having one category called django and one called Django. Since slugify makes the slugs lowercase, it will not be possible to distinguish between what category corresponds to the django slug
#so, customise the admin interface so that it automatically pre-populates the slug field as you type in the category name.
