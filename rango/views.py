from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context_dict)

def show_category(request, category_name_slug):
    #Create a context dictionary which we can pass to the template rendering engine
    context_dict = {}

    try:
        #Can we find a category name slug with the given name?
        #If we can't, the .get() method raises a DoesNotExist exception
        #So the .get() method returns one model instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)
        #Retrieve all of the associated pages.
        #Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        #Adds our results list to the template context under name pages
        context_dict['pages'] = pages
        #We also add the category object from the the database to the context
        #dictionary. We'll use this in the template to verify that the category
        #exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        #We get here if we didn't find the specified category
        #The template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
    #Go render the response and return it to the client
    return render(request, 'rango/category.html', context_dict)
    #Our new view follows the same basic steps as our index() view.
    #We first define a context dictionary and then attempt to extract
    #the data from the models, and add the relevant data to the context
    #dictionary. We determine which category by using the value passed as
    #parameter category_name_slug to the show_category() view function.
    #If the category slug is found in the Category model, we can then pull
    #out the associated pages , and add this to the context dictionary


#All view functions defined as part of a django application must take at least
#one parameter. This is typically called request and provides access to
#information related to the given HTTP request made by the user. When
#parameterising URLs, you supply additional named parameters to the
#signature for the given view. That is why our show_category() view was
#defined as def show_category(request, category_name_slug).
        
    #update index() view to include a link to the about view
 #   html="Rango says hey there partner!" + '<br/> <a href="/rango/about/">About</a>'
    #reconfigure index() view to change the view to dispatch our template index.html
    #Construct a dictionary to pass to the template engine as its context.
     #construct a dictionary of key/value pairs that we want to use within the template
     #call the render helper function, which takes as input the user's request,
     #the template filename, and the context dictionary. The render() function
     #will take this data and mash it together with the template to create a complete
 #html page that is returned wih a HTTPResponse. This response is then returned and
 #dispatched to the user's web browser.
 #the boldmessage originates from the view, but is rendered in the template

 #Query the database for a list of ALL categories currently stored.
 #Order the categories by number of likes in descending order
 #Retrieve the top 5 only - or all if less than 5
 #Place the list in our context_dict dictionary that will be passed to the
 #template engine.
    
    #the above expressionqueries the Category model to retrieve the top 5.
    #the - in likes denotes descending order. without, it'd be ascending
    #since a list of Category objects will be returned, we used Python's list operators
    #to the first five objects from the list to return a subset of Category objects
    #then we pass a reference to the list to the dictionary context_dict
    
 #   context_dict={'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    #Return a rendered response to send to the client
    #We make use of the shortcut function
    #Note that the first parameter is the template we wish to use

    #return HttpResponse(html)
#in the template we created (index.html), we included a template variable name called
#boldmessage. In here, the cookie string is mapped to template variable boldmessage,
#and so replaces boldmessage anywhere in index.html template
#create a new view method called about which returns the following HttpResponse:
def about(request):
    context_dict={'ABOUT_URL':"/about/"}
    #add the HTML to link back to the index page in your response from the about() view
 #   html2="Rango says here is the about page." + '<a href="/rango/">Index</a>'
 #   return HttpResponse(html2)
    return render(request, 'rango/about.html', context=context_dict)
	
