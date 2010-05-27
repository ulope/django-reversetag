
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

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
)
