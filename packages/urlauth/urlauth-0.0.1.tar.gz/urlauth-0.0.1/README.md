Problem:
==============
On an average, a person uses 60-90 applications, it’s not fun to enter passwords anymore.
Plus millions of passwords get exposed and accounts get compromised each year.
According to a survey, users admit they reuse the same password because it’s hard to remember them.
Of course, these problems are being addressed in relatively complex ways using 2FA, password managers
and such but a passwordless sign in is much simpler and quicker. 

Solution:
==============

Djangourlauth:

Provides a unique url that enables users to sign in without a password

We have implemented a passwordless authentication that enables a user to sign in without a password. 
User A can create a unique URL and share it with user B. User B can now use this URL to sign in without
having to enter a password(need a better example here).
It also removes friction points for the user to dropout of a system. 

Use cases:

1. Unique URL’s can be used to send promotion emails that allow users to access promotion codes for a set period of time
2. They can be used to send activity reminders for interactions on social media, such as a user being tagged on a facebook post or a comment, user tags on twitter post etc. 
3. Unique URL enable users to continue placing an order which was previously dropped without having to sign in to an application 

Advantages:

1. Fast
2. Simple
3. Higher conversion rate of promotion emails, purchase emails etc

As of now djangourlauth supports only session auth.


Example Usage:
==============

Create Login URL for a User
```
from url_auth.utils to import generate_login_url

generate_login_url(user_instance, redirect_url='/admin/')
```

settings.py

```
from datetime import timedelta

URL_AUTH_CONFIG = {
    'EXPIRY_TIME_DELTA': timedelta(days=7),
    'ENCRYPTION_ALGORITHIM': 'HS256',
}
```

Requirements
============

- Python (2.7+)
- Django (1.8+)
- pyjwt (1.6+)


Install
=======

1. Install url_auth

   ```
   pip install url_auth
   ```

2.  Add `url_auth` to your INSTALLED_APPS setting like this::
```python

 INSTALLED_APPS = [
     ...
     'url_auth',
      ...
 ]
```
3. Add `url_auth.views.login_by_url` to your urls.py

```python

 # django 1.8 - 1.11
 from url_auth.views import login_by_url
  
 urlpatterns = [
     ..
     url(r'^url-auth/$', login_by_url),
     ..
 ]
 
 # Django 2.0+
  from url_auth.views import login_by_url
 
  urlpatterns = [
     ..
     path('url-auth/', login_by_url),
     ..
 ]
 
 
```



Default Value of Settings
==============


```python

DEFAULTS = {
    # Time till signin URL is valid.
    'EXPIRY_TIME_DELTA': timedelta(days=7),
	# Encryption algorithim used for creating token
	'ENCRYPTION_ALGORITHIM': 'HS256'
}

```