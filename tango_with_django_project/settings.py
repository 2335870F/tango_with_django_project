"""
Django settings for tango_with_django_project project.

Generated by 'django-admin startproject' using Django 1.11.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#__file__ attribute is set to the absolute path of your settings module
#the call to os.path.drname() provides the reference to the absolute path
#of the directory containing the settings.py module (removes another layer)
#BASE_DIR now contains <workspace>/tango_with_django_project!
#print(__file__)
#print(os.path.dirname(__file__))
#print(os.path.dirname(os.path.dirname(__file__)))

#you create the variable up here so it's easier to access if needed changed
TEMPLATE_DIR=os.path.join(BASE_DIR, 'templates')
#os.path.join increases project's portability by adhering to os's own syntax
#yields <workspace>/tango_with_django_project/templates/.
#we can use our new TEMPLATE_DIR variable to replace the hard coded path we
#defined earlier in TEMPLATES.

#references new templates directory. BASE_DIR makes it easy to reference
#other aspects of Django project.Joins up multiple paths 

#just like the templates directory we created earlier, we need to tell django about
#our new static directory, since we did mkdir. Add a new variable pointing to our
#static directory, and a data structure that django can parse to work out where
#the new directory is

STATIC_DIR=os.path.join(BASE_DIR, 'static')
#this will provide an absolute path to the location <workspace>/tango_with_django
#_project/static/

MEDIA_DIR = os.path.join(BASE_DIR, 'media')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@rzl7tg6^y*f2q!amh3fuzr9^a7ldl!#j$=m!1vyl5zes3%_!j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rango',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tango_with_django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #tell django where our templates are stored by
        #modifying the DIRS list
        #'DIRS': ['<workspace> /tango_with_django_project/templates'],
        #the DIRS list allowed you to specify more than one template directory
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'tango_with_django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
#allows us to specify the URL with which static files can be accessed when we run
# the django development server. the location with which clients can access
#static content. the extra slash at the end ensures that the root of the URL
# /static/ is separated from the static content you want to serve (images/rango.jpg)
STATIC_URL = '/static/'


#now create a new data structure. We're only going to be using one location for
#storing our project's static files-the path defined in static_dir
STATICFILES_DIRS=[STATIC_DIR, ]


MEDIA_ROOT = MEDIA_DIR
#both of these media variables tell Django where to look in your filesystem
#for media files (MEDIA_ROOT) that have been uploaded/stored, and what URL to
#serve them from (MEDIA_URL). 
#the extra slash at the end ensures that the root of the UR: (/media/) is
#separated from the content uploaded by your app's users
MEDIA_URL = '/media/'
