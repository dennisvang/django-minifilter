"""
test settings, based on documentation:

https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#using-the-django-test-runner-to-test-reusable-applications

"""

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECRET_KEY = 'fake'
INSTALLED_APPS = ['tests']
DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'test.sqlite3'}
}
