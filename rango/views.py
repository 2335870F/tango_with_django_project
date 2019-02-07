from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

def get_server_side_cookie(request, cookie, default_val=None):
    val=request.session.get(cookie)
    if not val:
        val=default_val
    return val

def visitor_cookie_handler(request):
    #Get the number of visits to the site
    #We use COOKIES.get() function to obtain the visits cookie.
    #If the cookie exists, the value returned is casted to an integer
    #If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    #If it's been more than a day since the last visit...
    if(datetime.now() - last_visit_time).days>0:
        visits = visits + 1
        #Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        #Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    #Update/set the visits cookie
    request.session['visits'] = visits
    
def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    #Obtain our Response object early so we can add cookie information

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context=context_dict)
    #Call the helper function to handle the cookies
    #visitor_cookie_handler(request, response)
    #Return response back to the suer, updating any cookies that need changed.
    return response

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
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
 #   context_dict={'ABOUT_URL':"/about/"}
    context_dict={'boldmessage': "Rango says here is the about page"}
    #add the HTML to link back to the index page in your response from the about() view
 #   html2="Rango says here is the about page." + '<a href="/rango/">Index</a>'
 #   return HttpResponse(html2)
    print(request.method)
    print(request.user)
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)

@login_required
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

@login_required
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

def register(request):
    #A boolean value for telling the template whether the registration was successful
    #Set false initially. True when registration succeeds.
    registered = False
    #If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        #Attempt to grab information from the raw form information.
        #Note that we make use of both UserForm and UserProfileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            #Save the user's form data to the database
            user = user_form.save()

            #Now we hash the password with the set_password method
            #Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            #Now sort out the UserProfile instance
            #Since we need to set the user attributes ourselves, we set commit=False
            #This delays saving the model until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            
            #We need to establish a link between the two model instances tht we have
            #created. After creaing a new User model instance, we reference it in
            #the UserProfile instance with the line below. This is where we
            #populate the user attribute of the UserProfileForm form, which we
            #hid this field from users
            profile.user = user

            #Did the user provide a pro pic?
            #If so, we need to get it from the input form and put it in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            #Now we save the UserProfile model instance
            profile.save()

            #Update our variable to indicate that the template registration was successful
            registered = True
        else:
            #Invalid form or forms - mistakes or something else?
            #Print problems to the terminal
            print(user_form.errors, profile_form.errors)
    else:
        #Not a HTTP POST, so we render our form using two ModelForm instances.
        #These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form=UserProfileForm()
    return render(request, 'rango/register.html', {'user_form': user_form, 
	'profile_form': profile_form, 'registered': registered})
def user_login(request):
    #If the request is a HTTP POST, try to pull out the relevant info
    if request.method== 'POST':
        #Gather the username and password provided by user
        #This information is obtained from the login form
        # We use request.POST.get('<variable>') as opposed
        # to request.POST.get['<variable>'], because the former
        #returns None if the value doesnt exist, while the latter raises a KeyError exception
        username = request.POST.get('username')
        password = request.POST.get('password')
        #Use Django's machinery to attempt to see if the username/password
        #combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        #If we have a User obj, the details are correct
        #If None(python;s way of representing the absence of a value), no user
        #with matching credentials was found
        if user:
            #Is the account active?
            if user.is_active:
                #If the account is valid and active, we can log the user in
                #We'll send the user back to the homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                #An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled")
        else:
            #Bad login details were provided, so we can't log user in
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    #The request is not a HTTP POST, so display the login form
    else:
        #No context variables to pass to the template system, hence the
        #blank dictionary object
        return render(request, 'rango/login.html', {})
                
@login_required
def restricted(request):
    #return HttpResponse("Since you're logged in, you can see this text!")
    return render(request, 'rango/restricted.html', {})
    #Our new view follows the same basic steps as our index() view.
    #We first define a context dictionary and then attempt to extract
    #the data from the models, and add the relevant data to the context
    #dictionary. We determine which category by using the value passed as
    #parameter category_name_slug to the show_category() view function.
    #If the category slug is found in the Category model, we can then pull
    #out the associated pages , and add this to the context dictionary

@login_required
def user_logout(request):
    #Since we knoe the useris logged in, we can now just log them out
    logout(request)
    return HttpResponseRedirect(reverse('index'))


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

