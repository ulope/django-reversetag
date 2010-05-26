
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

ROOT_URLCONF = 'revtest.urls'

INSTALLED_APPS = (
    'reversetag',
    'revtest',
)
