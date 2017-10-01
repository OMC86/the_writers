from base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Stripe environment test variables
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_mNb1dKaAFoLSHyj2BAcDMl99')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_blRbu4P14RH0LjZMT2jDpwxy')