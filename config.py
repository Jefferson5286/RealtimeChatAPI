from decouple import config


class Config:
    TYPE = config('TYPE')
    PR0JECT_ID = config('PR0JECT_ID')
    PRIVATE_KEY_ID = config('PRIVATE_KEY_ID')
    PRIVATE_KEY = eval(config('PRIVATE_KEY'))
    CLIENT_EMAIL = config('CLIENT_EMAIL')
    CLIENT_ID = config('CLIENT_ID')
    AUTH_URI = config('AUTH_URI')
    TOKEN_URI = config('TOKEN_URI')
    AUTH_PROVIDER_X509_CERT_URL = config('AUTH_PROVIDER_X509_CERT_URL')
    CLIENT_X509_CERT_URL = config('CLIENT_X509_CERT_URL')
    UNIVERSE_DOMAIN = config('UNIVERSE_DOMAIN')

    SECRET_KEY = config('SECRET_KEY')

    ORIGINS = eval(config('ORIGINS'))


env = Config()
