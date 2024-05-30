from google.cloud import firestore
from config import env

client = firestore.Client.from_service_account_info({
    "type": env.TYPE,
    "project_id": env.PR0JECT_ID,
    "private_key_id": env.PRIVATE_KEY_ID,
    "private_key": env.PRIVATE_KEY,
    "client_email": env.CLIENT_EMAIL,
    "client_id": env.CLIENT_ID,
    "auth_uri": env.AUTH_URI,
    "token_uri": env.TOKEN_URI,
    "auth_provider_x509_cert_url": env.AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url": env.CLIENT_X509_CERT_URL,
    "universe_domain": env.UNIVERSE_DOMAIN
})
