# django-debug-helper
Django debug error related exception search on Google/ Stack Overflow.

### Installation
```
$ pip install django-debug-helper
```

### Setting it up
Add the custom middleware to your **MIDDLEWARE** in the ```settings.py```.
```
if DEBUG:
	MIDDLEWARE += ('django-debug-helper.debug.ErrorSearchMiddleware', )
```
Next time you get an error in your applications, you will see an external link to a custom **google/ stackoverflow** search as you defined.


By default it set to **google** search, but if you want to use **stackoverflow** search instead of **google** then add this into your ```settings.py```
```
DJANGO_TRACE_SEARCH_SITE = "stackoverflow"
```

