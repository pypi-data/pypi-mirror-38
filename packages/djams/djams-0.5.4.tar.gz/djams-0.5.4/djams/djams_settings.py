import os
from decouple import config
import dj_database_url
from unipath import Path

SERVER_NUMBER = os.environ.get('SERVER_NUMBER')
SERVER_ENV = os.environ.get('SERVER_ENV')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = Path(__file__).parent

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if SERVER_ENV == None:
    SERVER_ENV = 'local'

print("SERVER NUMBER: %s" %(SERVER_NUMBER))
print("CURRENT ENVRIONMENT: %s" %(SERVER_ENV))

SERVER_SETTINGS_DICT = {'local': { 'SECRET_KEY': '^_r4l3q4jk_hg78qz%f^ab2ri=xy(yor30)9n%#c@39bnoz3%x',
                                    'DEBUG': True,
                                    'TEMPLATE_DEBUG': True,
                                    'ALLOWED_HOSTS' : ['*', 'localhost', '127.0.0.1'],
                                    'SECURE_SSL_REDIRECT': False,
                                    'SECURE_PROXY_SSL_HEADER': None,
                                    'STATICFILES_STORAGE': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
                                    'STATICFILES_DIRS': ['static'],
                                    'MEDIAFILES_DIRS': ['media',],
                                    'app_launch_url_field': 'user_launch_view',
                                    'MEDIA_ROOT': 'media',
                                    'STATIC_ROOT': 'static',
                                    'SHARED_MEDIA_LOC': '../media',
                                    'CACHES': {
                                                "default": {
                                                    "BACKEND": "django_redis.cache.RedisCache",
                                                    "LOCATION": "redis://127.0.0.1:6379/1",
                                                    "OPTIONS": {
                                                        "CLIENT_CLASS": "django_redis.client.DefaultClient"
                                                    },
                                                    "KEY_PREFIX": "REPLACE_ME"
                                                             },

                                                    'select2': {
                                                        "BACKEND": "django_redis.cache.RedisCache",
                                                        "LOCATION": "redis://127.0.0.1:6379/2",
                                                        "OPTIONS": {
                                                            "CLIENT_CLASS": "django_redis.client.DefaultClient",
                                                        },

                                                    "KEY_PREFIX": "select2"
                                                    },

                                                'redis': {
                                                    'BACKEND': 'django_redis.cache.RedisCache',
                                                    'LOCATION': 'redis:127.0.0.1:6379/1',
                                                    'OPTIONS': {
                                                                'CLIENT_CLASS': 'django_redis.client.DefaultClient'
                                                                 },

                                                    'KEY_PREFIX': 'REPLACE_ME'
                                                },

                                                },
                                            
                                    'LOGGING': {'version': 1,
                                                'disable_existing_loggers': False,
                                                'handlers': {'console': {'class': 'logging.StreamHandler',},
                                                            },
                                                'loggers': {'django': {'handlers': ['console'],
                                                                        'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
                                                                      },
                                                            },
                                                },

                                    },




                        'heroku': {'SECRET_KEY': config('SECRET_KEY', default='donotusemeassecretkey3'),
                                    'DEBUG': config('DEBUG', default=False, cast=bool),
                                    'TEMPLATE_DEBUG' : config('DEBUG', default=False, cast=bool),
                                    'ALLOWED_HOSTS': ['*', 'admin_portal.herokuapp.com', 'www.burmicz.com'],
                                    'SECURE_SSL_REDIRECT': True,
                                    'SECURE_SSL_HOST': 'https://www.burmicz.com',
                                    'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
                                    'STATICFILES_STORAGE': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
                                    'STATICFILES_DIRS': None,
                                    'MEDIAFILES_DIRS': None,
                                    'MEDIA_ROOT': os.path.join(BASE_DIR, 'media'),
                                    'STATIC_ROOT': os.path.join(BASE_DIR, 'static'),
                                    'SHARED_MEDIA_LOC': 'media',
                                    'app_launch_url_field': 'launch_heroku_url',
                                    'CACHES': {
                                                "default": {
                                                    "BACKEND": "django_redis.cache.RedisCache",
                                                    "LOCATION": "redis://127.0.0.1:6379/1",
                                                    "OPTIONS": {
                                                        "CLIENT_CLASS": "django_redis.client.DefaultClient"
                                                    },
                                                    "KEY_PREFIX": "dpd-admin_portal"
                                                             },

                                                'select2': {
                                                        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                                                        'LOCATION': '10.151.60.89:11211',
                                                        'TIMEOUT': 60 * 60 * 24,
                                                    },

                                                'redis': {
                                                                'BACKEND': 'django_redis.cache.RedisCache',
                                                                'LOCATION': 'redis:127.0.0.1:6379/1',
                                                                'OPTIONS': {
                                                                            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
                                                                            },

                                                                'KEY_PREFIX': 'REPLACE_ME'
                                                            },
                                                },
                                    'CACHE_DEFAULT_LOCATION': '10.151.68:11211',
                                    'login_url': 'login/',
                                    'login_redirect_url': 'appsession/',

                                    'LOGGING': {'version': 1,
                                                'disable_existing_loggers': False,
                                                'handlers': {'console': {'class': 'logging.StreamHandler',},
                                                            },
                                                'loggers': {'django': {'handlers': ['console'],
                                                                        'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
                                                                      },
                                                            },
                                                }



                    },

                        'PROD': {'SECRET_KEY': os.environ.get('SECRET_KEY'),
                                 'HOST': 'somesqlserver.company.net\INST1',
                                 'DEBUG': False,
                                 'TEMPLATE_DEBUG': False,
                                 'ALLOWED_HOSTS' : ['*', 'localhost', '127.0.0.1', 'somecompany.net'],
                                 'SECURE_SSL_REDIRECT': False,
                                 'SECURE_SSL_HOST': 'https://www.burmicz.com',
                                 'SECURE_PROXY_SSL_HEADER': None,
                                 'STATICFILES_STORAGE': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
                                 'STATICFILES_DIRS': ['../static'],
                                 'MEDIAFILES_DIRS': ['../media'],
                                 'app_launch_url_field': 'launch_local_url',
                                 'STATICFILES_DIRS': ['../static'],
                                 'MEDIAFILES_DIRS': ['../media'],
                                 'MEDIA_ROOT': ['BASE_DIR', 'media'],
                                 'STATIC_ROOT': ['BASE_DIR', 'static'],
                                 'SHARED_MEDIA_LOC': 'media',
                                 'CACHE_DEFAULT_LOCATION': '10.151.68:11211',
                                  'CACHES': {
                                                "default": {
                                                    "BACKEND": "django_redis.cache.RedisCache",
                                                    "LOCATION": "redis://127.0.0.1:6379/1",
                                                    "OPTIONS": {
                                                        "CLIENT_CLASS": "django_redis.client.DefaultClient"
                                                    },
                                                    "KEY_PREFIX": "dpd-admin_portal"
                                                             },

                                                'select2': {
                                                        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                                                        'LOCATION': '10.151.60.89:11211',
                                                        'TIMEOUT': 60 * 60 * 24,
                                                    },

                                                'redis': {
                                                                'BACKEND': 'django_redis.cache.RedisCache',
                                                                'LOCATION': 'redis:127.0.0.1:6379/1',
                                                                'OPTIONS': {
                                                                            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
                                                                            },

                                                                'KEY_PREFIX': 'REPLACE_ME'
                                                            },
                                                },

                                 'login_url': 'login/',
                                 'login_redirect_url': 'appsession/',
                                 'LOGGING': {'version': 1,
                                                'disable_existing_loggers': False,
                                                'handlers': {'console': {'class': 'logging.StreamHandler',},
                                                            },
                                                'loggers': {'django': {'handlers': ['console'],
                                                                        'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
                                                                      },
                                                            },
                                                },

                                'SECURE_SSL_HOST': None,
                                'SECURE_SSL_REDIRECT' : True,
                                # SESSION_COOKIE_SECURE = True
                                # CSRF_COOKIE_SECURE = True
                                # SECURE_CONTENT_TYPE_NOSNIFF = True
                                # SECURE_BROWSER_XSS_FILTER = True
                                # SECURE_HSTS_SECONDS = 30
                                # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
                                # SECURE_HSTS_PRELOAD = True
                                # X_FRAME_OPTIONS = 'DENY'
                                #SECURE_PROXY_SSL_HEADER =(settings_dict[ENV]['SECURE_PROXY_SSL_HEADER'], 'https')

                                # BASE_URL = settings_dict[ENV]['BASE_URL']


                                    },
}

DJAMS_USER_MODEL = 'djams.ADM_CustomUser'

DJAMS_AUTH_PASSWORD_VALIDATORS = [
                            {
                                'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
                            },
                            {
                                'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
                                'OPTIONS': {'min_length': 10}
                            },
                            {
                                'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
                            },
                            {
                                'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
                            },
                        ]

DJAMS_SESSION_EXPIRE_AT_BROWSER_CLOSE = True
DJAMS_SESSION_EXPIRE_AFTER = 1800
DJAMS_SESSION_WARN_AFTER = 1680
DJAMS_CLIENT_DB_ROUTER = 'djams.middleware.SubClientDBRouter'
DJAMS_SESSION_ROUTER = 'djams.middleware.UserSessionRouter'


def get_DATABASES_dict(server_env, test_client_db_name=None):

    if 'local' in server_env and test_client_db_name:
        databases = {}
        
    else:
        databases = {}

    return databases

DATABASES_DICT = {'local': {'default': {
                                        'ENGINE': 'sql_server.pyodbc',
                                        'DSN': 'local_sql_server_conn_1',
                                        'OPTIONS': {'driver': 'ODBC Driver 13 for SQL Server'},
                                        'NAME': 'MDS',
                                       },
                            'MDS': {
                                        'ENGINE': 'sql_server.pyodbc',
                                        'DSN': 'local_sql_server_conn_1',
                                        'OPTIONS': {'driver': 'ODBC Driver 13 for SQL Server'},
                                        'NAME': 'MDS',
                                       },

                            'RDS_CL1': {
                                        'ENGINE': 'sql_server.pyodbc',
                                        'DSN': 'local_sql_server_conn_1',
                                        'OPTIONS': {'driver': 'ODBC Driver 13 for SQL Server'},
                                        'NAME': 'RDS_CL1',
                                       },
                            'RDS_CL2': {
                                        'ENGINE': 'sql_server.pyodbc',
                                        'DSN': 'local_sql_server_conn_1',
                                        'OPTIONS': {'driver': 'ODBC Driver 13 for SQL Server'},
                                        'NAME': 'RDS_CL2',
                                       },
                            'TDS_CL1': {
                                        'ENGINE': 'sql_server.pyodbc',
                                        'DSN': 'local_sql_server_conn_1',
                                        'OPTIONS': {'driver': 'ODBC Driver 13 for SQL Server'},
                                        'NAME': 'TDS_CL1',
                                       },
                            'TDS_CL2': {
                                        'ENGINE': 'sql_server.pyodbc',
                                        'DSN': 'local_sql_server_conn_1',
                                        'OPTIONS': {'driver': 'ODBC Driver 13 for SQL Server'},
                                        'NAME': 'TDS_CL2',
                                       },
                            'ADS_CL1': {
                                        'ENGINE': 'sql_server.pyodbc',
                                        'DSN': 'local_sql_server_conn_1',
                                        'OPTIONS': {'driver': 'ODBC Driver 13 for SQL Server'},
                                        'NAME': 'ADS_CL1',
                                       },
                            'ADS_CL2': {
                                        'ENGINE': 'sql_server.pyodbc',
                                        'DSN': 'local_sql_server_conn_1',
                                        'OPTIONS': {'driver': 'ODBC Driver 13 for SQL Server'},
                                        'NAME': 'ADS_CL2',
                                       },
                            },
                  
                  'heroku': {'default': dj_database_url.config(default=config('DATABASE_URL', default='')),
                             'MDS': dj_database_url.config(default=config('DATABASE_URL', default='')),
                             'RDS_CL1': dj_database_url.config(default=config('DATABASE_URL', default='')),
                             'RDS_CL2': dj_database_url.config(default=config('DATABASE_URL', default='')),
                             'TDS_CL1': dj_database_url.config(default=config('DATABASE_URL', default='')),
                             'TDS_CL2': dj_database_url.config(default=config('DATABASE_URL', default='')),
                             'ADS_CL1': dj_database_url.config(default=config('DATABASE_URL', default='')),
                             'ADS_CL2': dj_database_url.config(default=config('DATABASE_URL', default='')),
                            }
            
            
}