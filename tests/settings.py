from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#using-the-django-test-runner-to-test-reusable-applications

SECRET_KEY = 'fake'

INSTALLED_APPS = ['tests']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test.sqlite3'
    }}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
