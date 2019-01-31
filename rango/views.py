from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context=context_dict)

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

def about(request):
    context_dict={'ABOUT_URL':"/about/"}
    #add the HTML to link back to the index page in your response from the about() view
 #   html2="Rango says here is the about page." + '<a href="/rango/">Index</a>'
 #   return HttpResponse(html2)
    return render(request, 'rango/about.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    #A HTTP POST?
    if request.method =='POST':
        form = CategoryForm(request.POST)
        #Have we been provided with a valid form?
        if form.is_valid():
            #Save the new category to the database.
            category=form.save(commit=True)
            print(category, category.slug)

            return index(request)
        else:
           
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except category.DoesNotExist:
        category = None
        
    form=PageForm()
    if request.method=='POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category=category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
            else:
                print(form.errors)
    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)



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
    #The new add_category() view adds several key pieces of functionality for handling forms.
    #First, we create a CategoryForm(), then we check if the HTTP request was
    #a POST i.e. if the user submitted data via the form. We can then handle the
    #POST request through the same URL. The add_category() view function can
    #handle 3 diff scenarios: showing a new, blank form for adding a category;
    #saving form data provided by the user to the associated model, and rendering
    #the Rango homepage; and,
    #if there are errors, redisplay the form with error messages
            #Now that the category is saved
            #We could give a confirmation message
            #But since the most recent category added is on the index page
            #Then we can direct the user back to the index page
 #The supplied form contained errors -
            #just print them to the terminal
            #This error I think is "Please fill out this field!"
            #actually i think Please fill out this field isnt an error we
            #wrote, it's an automatic one given by django which could come from
            #print form.errors?
#Will handle the bad form, new form, or no form supplied cases.
    #Render the form with error messages if any.
#A HTTP GET is used to request a representation of the specified resource.
#We use a HTTP GET to retrieve a particular resource, whether it is a webpage,
#image, file. In contrast, a HTTP POST submits data from the clinet's
#web browser to be processed. This type of request is used when submitting
#the contents of a HTML form. Ultimately, a HTTP POST may end up being
#programmed to create a new resource (a new DB entry) on the server, which can
#later be accessed through a HTTP GET request.
#Django's form handling machinery processes the data returned from a user's
#browser via a HTTP POST request. It not only handles the saving of form
#data into the chosen model, but will also automatically generate error
#messages for each form field if required. Django will not store any
#submitted forms with missing information that could potentially cause
#problems for your database's referential integrity is what this means.
#So, supplying no value in the category name field will return an error as the
#field cannot be blank.
#add_category.html will contain the relevant Django template code and HTML for the form and page.

#Questions at the end of ch7 of TWD: If you don't enter in a category name on the add category form
# and hit Submit, you get an error message "Please fill out this field.". This is because we required
#this field be filled in by making it visible in forms.py and listing it as one of the
#fields for the CategoryForm class!
#When you try to add a category that already exists, you get an error message
#saying "Category with this Name already exists.
#When you visit a category that does not exist (http://127.0.0.1:8000/rango/category/pumpkin/)
#you get an error message "The specified category does not exist!" which comes
#from the template message we created in category.html

