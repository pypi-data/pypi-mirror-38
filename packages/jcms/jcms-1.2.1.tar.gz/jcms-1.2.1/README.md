# Jcms

Jcms is an easy to use cms for Django(python)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The only thing that you need to have installed is pip. But if you haven't this means you are also not using django which you should.

### Installing

Jcms is easy to install. First you install it via pip

```
pip install jcms
```

<br/>
Now you can add Jcms to INSTALLED_APPS in your settings file.

```python
INSTALLED_APPS = [
    'jcms'
]
```

<br/>
After this you need to add the urls to your urls.py. You can replace admin with everything you want.

```python
from django.conf.urls import path, include

urlpatterns = [
    path('admin/', include('jcms.urls')),
]
```

Now to add a user you can do this via the commandline. Find more on this in the [documentation of Django](https://docs.djangoproject.com/en/1.11/topics/auth/default/)

<br/>
Now go to your site's url and do the /admin/ (or if you have chosen another path type that). You can now log in with the credentials you just created.


## Before using
### <span style="color:red;">Be aware of the following things </span>
There can only be one model with the same name

These model names are in use:
- User
- Group
- Option


## jcms.py

You can add menu items and urls to jcms. This means that the urls you add are connected to the Jcms app.

What you first have to do is add the jcms.py file to the app. The file structure of the app is underneath

```
practice-app
    jcms.py
    migrations
    static
    templates
    other-folders
```

Everything for jcms can be done in the jcms.py file.

> You can disable the warning for each setting if you don't want to add it by adding this to jcms.py
```python
from jcms.components import NoConfig

menu_item = NoConfig
```

### Adding crud views


```python
from jcms.generators import CMSGenerator
from jcmstest.models import Test, PK

urlpatterns = [
    CMSGenerator(Test, ['type', 'value', 'content'], ['type', 'value']),
    CMSGenerator(PK, ['name'], ['name'])
]
```

The following options can be given:
- **model** = The model this crud is for
- **create_edit_list** = This is an array of items which you can create and edit in these views
- **list_fields** = This is a list of fields of the model which are shown in the list view

CMSGenerator makes the following views:
- Create. Viewname is ${model_name_lower}Create
- Edit. Viewname is ${model_name_lower}Edit
- List. Viewname is ${model_name_lower}List
- Delete. Viewname is ${model_name_lower}Delete

### Adding api views

This is a basic example of a api view for jcms.

```python
from jcms.generators import APIGenerator
from jcmstest.models import Test

urlpatterns = [
    APIGenerator(Test, ['type', 'value', 'content'], lookup_field='type'
            method_fields={'overview_fields': ['id', 'type', 'value', 'content']})
]
```

Required variables are:
- **model** = model used for the api
- **basis_fields** = default fields that the api uses to serialize
- **lookup_field** = The field that is used for the retrieving of a single object

The options you can give to APIGenerator are:
- **methods** = A list that has the methods that are allowed ([see below](#methods))
- **method_fields** = A dict that has the fields for each method

#### methods
- **overview** = Gets the models by a GET request to /api/${model_name_lower}. You can also filter on these fields using query parameters. If no overview fields are given is goes back to the basis fields
- **create** = Creates a model by a POST request to /api/${model_name_lower}
- **update** = Updates a model by a PUT for a full update and a PATCH for partial update to /api/${model_name_lower}/${id}
- **retrieve** = Gets the model by GET request to /api/${model_name_lower}/${id}
- **delete** = Deletes a model by DELETE request to /api/${model_name_lower}/${id}
- **lookup_field** = Field used for the ${model_name_lower}-detail view

For every each option (overview, create, update, retrieve, delete) you can pass certain fields if you don't want to use the basic ones. You can pass them in the dict object of method_fields

The names for the views are:
- all or overview and create = ${model_name_lower}-list
- all or update, retrieve and delete = ${model_name_lower}-detail

### Making the menu items

First you need to create a menu_item.py in the jcms.py file.

```python
from jcms.models import GenericMenuItem, SingleMenuItem
from jcmstest.models import Test, PK

menu_item = GenericMenuItem('Test',  [
    SingleMenuItem('Test', 'testList'),
    SingleMenuItem('PK', 'pkList'),
])
```

You can give the following options:
* name = The name seen on the menu item
* items = List of the menu item. This HAS to be a SingleMenuItem Object.
* slug = The slug used in the url. The slug is optional

### Adding your menu item to jcms

The last step is to add the menu item to jcms. You can do this by going to your django settings and adding this line.

```python
JCMS_APPS = ['practice-app']
```

This are only the apps that should be in Jcms.

## Icons
You can use these icons like this:
```
{% include "icons/[icon-name].svg" %}
```

The icons you can use are =:
- add
- delete
- dropdown-caret
- edit
- groups
- hamburger
- home
- logout
- options
- standard-menu-item
- users
- cancel

## Templatetags

These are the template tags that you can use that are in Jcms

### add_item

Add a item to an array

```
{% load add_item %}
{% add_item array new_item as array %}
```

### crud_url

Load a crud url based upon the model

```
{% load crud_url %}
{% url "Create"|crud_url:model %}
```

### get_menu_items

Get menu items for the cms

```
{% load get_menu_items %}
{% get_menu_items as menu_items %}
```

### get_model_name

Gets the name of a model

```
{% load get_model_name %}
{{ view.model|get_model_name }}
```

### get_object_attr

Gets the attribute of a object dynamically

```
{% load get_object_attr %}
{{ object|get_object_attr:field }}
```

## Deployment

Ask **[Jessie Liauw A Fong](https://github.com/jessielaf)** to for deployment

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Pip](https://pypi.python.org/pypi/pip) - Dependency Management
* [Yarn](https://yarnpkg.com/) - Npm package manager

## Authors

* **[Jessie Liauw A Fong](https://github.com/jessielaf)**
