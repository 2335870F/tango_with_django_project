from django.shortcuts import render
from django.http import HttpResponse
def index(request):
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
    context_dict={'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    #Return a rendered response to send to the client
    #We make use of the shortcut function
    #Note that the first parameter is the template we wish to use
    return render(request, 'rango/index.html', context=context_dict)
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
	
