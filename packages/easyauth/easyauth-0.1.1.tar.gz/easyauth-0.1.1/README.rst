easyauth: A simplified authentication lib based on Django and Rest Framework
===========================================

.. image:: https://img.shields.io/travis/qingfeng0820/easyauth/master.svg
    :target: https://travis-ci.org/qingfeng0820/easyauth


License
-------

`BSD License <LICENSE.txt>`_


Installation
--------

from pypi

.. code-block:: python

    pip install easyauth


Tutorial
--------


Add easyauth to your app
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add easyauth in {Your app}/settings.py like below:

.. code-block:: python

    INSTALLED_APPS += (
        # Default Django apps:
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Rest framework app
        'rest_framework',
        # easyauth app                                                                  #<----  Add easyauth app here
        'easyauth',
        # Your own app                                                                  #<----  Add your own app
        'test'
    )

    # If add django-filter app to INSTALLED_APPS, the easyauth APIs can support filter by fields' values

    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        'DEFAULT_PERMISSION_CLASSES': (
            'easyauth.permissions.IsAuthenticated',                                      #<---- Default permission check
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'easyauth.authentication.CsrfExemptSessionAuthentication',                   #<---- Disable crsf check
            'rest_framework.authentication.BasicAuthentication'
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            #  Enable BrowsableAPI
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser'
        ),
        'DEFAULT_PAGINATION_CLASS': 'easyauth.pagination.CustomizedPageNumberPagination', #<--- Set default pagination
        'PAGE_SIZE': 500
    }


Specify your own User Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create your own User Model (extends easyauth.models.AbstractUser) in {Your app}/models.py:

.. code-block:: python

    from easyauth.models import AbstractUser


    class User(AbstractUser):
        # you can define additional fields for your User Model

        # You can specify the USERNAME_FIELD field.
        # Default is phone
        # USERNAME_FIELD = {Other field to stand for username}
        # {Other field} = models.CharField(...)

        # You can specify the USER_DEPART_FIELD field if you user model is grouped by department or company
        # In this case, an admin in a company cannot maintain the users in other company
        # Default value is None
        # USER_DEPART_FIELD = "company"
        # company = models.ForeignKey(Company, related_name='users', null=True)

        pass


Change AUTH_USER_MODEL to be your own User Model in {Your app}/settings.py:

.. code-block:: python
        
    AUTH_USER_MODEL = 'test.User'
    

Expose easyauth APIs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Expose user admin APIs and user authentication related APIs in {Your app}/urls.py by below code:

.. code-block:: python

    from easyauth import urls as auth_urls
    from easyauth import admin_urls as user_admin_urls

    urlpatterns = [
        # auth apis including login, password reset
        url(r'^api-auth/', include(auth_urls)),
        # user admin crud apis - only used by administrator
        url(r'^api/', include(user_admin_urls)),
    ]


API List:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- user group/role admin APIs (admin or super user)
    - /api/groups GET: Get all user groups
    - /api/groups POST: Create an user group  (Only accessed by super user)
    - /api/groups/[group_id] GET: Get an user group
    - /api/groups/[group_id] POST or PUT: Modify an user group (Only accessed by super user)
    - /api/groups/[group_id] DELETE: Delete an user group (Only accessed by super user)

- user admin APIs (admin or super user, if department enabled for user model, admin can only maintain users in the same department)
    - /api/users GET: Get all users
    - /api/users POST: Create an user (With default password. Cannot create a super user via Rest API)
    - /api/users/[user_id] GET: Get a specific user
    - /api/users/[user_id] POST or PUT: Modify a specific user
    - /api/users/[user_id] DELETE: Delete a specific user
    - /api/users/[user_id]/reset/password POST: Reset to default password for a specific user

- authentication APIs
    - /api-auth/login POST: User login
    - /api-auth/logout POST (or GET if enabled): User logout
    - /api-auth/me POST or PUT: Modify current login user
    - /api-auth/me GET: Get current login user
    - /api-auth/password/change POST: Change the current login user's password
    - /api-auth/register POST: Register User (This API can be disabled by configuration)

You must start with creating a superuser in backend (operate DB directly or use command "python manage.py createsuperuser")

easyauth Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add EASYAUTH_CONF in {Your app}/settings.py if you need to do some specific configuration:

.. code-block:: python

    EASYAUTH_CONF = {
        'USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN': "12345678",
        'ACCOUNT_LOGOUT_ON_GET': False,
        'DISABLE_REGISTER': False,
    }

+----------------------------------------+------------+--------------------------------------------------------------+
| Configuration Item                     | Type       | Description                                                  |
+----------------------------------------+------------+--------------------------------------------------------------+
| USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN     | string     | Define the default password for maintaining by administrator.|
|                                        |            | Default value is 123456 for absent                           |
+----------------------------------------+------------+--------------------------------------------------------------+
| ACCOUNT_LOGOUT_ON_GET                  | bool       | Switch for enabling GET method for logout API.               |
|                                        |            | Default value is False for absent                            |
+----------------------------------------+------------+--------------------------------------------------------------+
| DISABLE_REGISTER                       | bool       | Switch for disabling register API.                           |
|                                        |            | Default value is False for absent                            |
+----------------------------------------+------------+--------------------------------------------------------------+

More examples please see the test app in this repo