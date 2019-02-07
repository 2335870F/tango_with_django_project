#you could put the forms in the models.py
from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

#helper class that allows you to create a Django form from a pre-
#existing model which is defined for ur app(like Category or Page)
class CategoryForm(forms.ModelForm):
    #Django also provides EmailField, ChoiceField, DateField; they all
    #provide error checking for you
    #Here, we repeated the max_length values for fields that we had previously
    #defined in models.py. We are repeating ourselves so refactor so we are not
    #repeating the max_length values!
    name = forms.CharField(max_length=128,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    #We have said that the field is not required by the form, rather than
    #specifying an initial or default value. This is because our model will
    #be responsible on save() for populating this field. You need to be
    #careful when you define your models and forms to make sure that the
    #form is going to contain and pass on all the data that is required to
    #populate your model correctly. 

    #An inline class to provide additional information on the form
    class Meta:
        #Provide an association between the ModelForm and a model
        #the most important aspect of a class inheriting from ModelForm is the
        #need to define which model we're wanting to provide a form for. We do
        #this thru our nested Meta class. Set the model attribute of the nested
        #Meta class to the model you wish to use. Our CategoryForm class has a
        #reference to the Category model. This enables Django to take care of
        #creating a form in the image of the specified model. It will also help
        #in handling flagging up any errors along with saving and displaying the
        #data in the form. We also use the Meta class to specify which fields that
        #we wish to include in our form thru the fields tuple.
        model = Category
        fields = ('name',)
class PageForm(forms.ModelForm):
    #class inherits from forms.ModelForm
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        #Overriding methods implemented as part of the Django framework can
        #provide you with an elegant way to add the extra bit of functionality
        #for ur app. There r many methods which u can override for ur benefit, like
        #the clean() method in ModelForm!
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        #cleaned_data is a dictionary
        #If url is not empty and doesn't start with 'http://',
        #then prepend 'http://'
        #For each form field that you wish to process (like url), check that
        #a value was retrieved. If something was entered, check what the value
        #was. If it isn't what u expect, you can then add some logic to fix this
        #issue before reassigning the value in the cleaned_data dictionary
        if url and not url.startswith('http://'):
            url = 'http://'+url
            cleaned_data['url'] = url

            return cleaned_data
        #cleaning the data being passed thru the form before being stored.
        #always end the clean() method by returning the reference to the
        #cleaned_data dictionary. otherwise, the changes won't be applied.
        
    #initial=0 sets the field to zero by default.
    #The fields with HiddenInput will be hidden and the user won't be able
    #to enter a value for these fields
    #Despite the fact that we have hidden a field, we still need to include
    #the field in the form. If in fields we excluded views, then the form
    #would not contain that field(despite it being specified) and so the
    #form would not return the value zero for that field. This may raise an error.
    #If in the model we specified that the default=0 for these fields then we can
    #rely on the model to automatically populate field with the default value-and
    #thus avoid a not null error. in this case, it would not be necessary to have
    #these hidden fields. 
    class Meta:
        #Provide an association between the ModelForm and a model
        model = Page
        #What fields do we want to include in our form?
        #This way we don't need every field in the model present
        #Some fields may allow NULL values, so we may not want to include them.
        #Here, we are hiding the foreign key.
        #we can either exclude the category fied from the form,
        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')
        #We need to specify which fields are included on the form, via 'fields',
        #or specify which fields are to be excluded, via 'exclude', as above.
        #Customising the forms we've created: We've specific the widgets that
        #we wish to use for each field to be displayed. In our PageForm class,
        #we've defined forms.CharField for the title field, and forms.URLField
        #for url field. Both fields provide text entry for users. The max_length
        #parameters we supply to our fields are identical to the maximum length
        #of each field we specified in the underlying data models (models.py)
class UserForm(forms.ModelForm):
    #there is a default password attribute for a User model instance.
    #However, it won't hide it when the user types in
    #By updating the password attribute, we can specify that the
    #Charfield instance should hide the users input through the
    #passwordinput() widget!!!
    password = forms.CharField(widget=forms.PasswordInput())

    #describes additional properties about the particular class to which it belongs.
    #each meta class must supply a model field
    #in the case of the UserForm class, the associated model is the User model
    #Need to specify the fields or the fields to exclude, to indicate
    #which should be on the rendered form!
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
