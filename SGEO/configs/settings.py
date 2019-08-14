import os
from decouple import config, Csv
from dj_database_url import parse as dburl
from .configs import DEFAULT_DATABASE_URL, DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS


APP_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(APP_ROOT))

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'staticfiles'))
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
# DEBUG = False

#ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())
#ALLOWED_HOSTS = ['app.SGEOerp.com.br', 'localhost']
ALLOWED_HOSTS = ['localhost']

if not DEFAULT_DATABASE_URL:
    DEFAULT_DATABASE_URL = 'sqlite:///' + os.path.join(APP_ROOT, 'db.sqlite3')

#DATABASES = {
#    'default': config('DATABASE_URL', default=DEFAULT_DATABASE_URL, cast=dburl),
#}

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'bd1',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)


# Application definition

SHARED_APPS = [
    'dal',
    'dal_select2',
    # 'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dbbackup',
    'django_tables2',
    'django_tables2_column_shifter',
    'django_filters',
    'bootstrap3',
    'django_tenants',

    # SGEO customer app
    'SGEO.apps.customer',
]

TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    # SGEO apps:
    'SGEO.apps.base',
    'SGEO.apps.login',
    'SGEO.apps.cadastro',
    'SGEO.apps.vendas',
    'SGEO.apps.compras',
    'SGEO.apps.fiscal',
    'SGEO.apps.financeiro',
    'SGEO.apps.estoque',
    'SGEO.apps.agenda',
    'SGEO.apps.crm2',
    'SGEO.apps.pdv',
    'SGEO.apps.relatorios',
    'SGEO.apps.boletos',
    'SGEO.apps.plano',
    'SGEO.apps.compra_certificado',
    'SGEO.apps.contador',
    'SGEO.apps.contratos',
    'SGEO.apps.frasesdodia',
    'SGEO.apps.integracao_financeira',
]

INSTALLED_APPS = list(set(SHARED_APPS + TENANT_APPS))

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware para paginas que exigem login
    'SGEO.middleware.LoginRequiredMiddleware',

    # Middleware para database-tenant
    'django_tenants.middleware.main.TenantMainMiddleware',
]

ROOT_URLCONF = 'SGEO.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APP_ROOT, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # contexto para a versao do sige
                'SGEO.apps.base.context_version.sige_version',
                # contexto para a foto de perfil do usuario
                'SGEO.apps.login.context_user.foto_usuario',
            ],
        },
    },
]

WSGI_APPLICATION = 'SGEO.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'pt-br'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': PROJECT_ROOT + '/backup'}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/


STATIC_URL = '/static/'

#STATIC_ROOT = os.path.join(APP_ROOT, 'static/')

STATICFILES_DIRS = [
    os.path.join(APP_ROOT, 'static'),
]

FIXTURE_DIRS = [
    os.path.join(APP_ROOT, 'fixtures'),
]

MEDIA_ROOT = os.path.join(APP_ROOT, 'media/')
MEDIA_URL = 'media/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

LOGIN_NOT_REQUIRED = (
    r'^/login/$',
    r'/login/esqueceu/',
    r'/login/trocarsenha/',
    r'/logout/',
    r'/customer/cadastro',
)

TENANT_MODEL = "customer.Client"  # app.Model

TENANT_DOMAIN_MODEL = "customer.Domain"  # app.Model
