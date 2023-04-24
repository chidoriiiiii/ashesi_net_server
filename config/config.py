import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    MICROSOFT_CLIENT_SECRET = os.environ.get("MICROSOFT_CLIENT_SECRET")
    MICROSOFT_CLIENT_ID = os.environ.get("MICROSOFT_CLIENT_ID")
    MICROSOFT_REMOTE_APP = os.environ.get("MICROSOFT_REMOTE_APP")
    MICROSOFT_CALLBACK = "http://localhost:5000/auth/microsoft/callback"
    API_BASE_URI = "https://graph.microsoft.com/",
    AUTHORIZE_URI = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    ACCESS_TOKEN_URI = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    JWKS_URI = 'https://login.microsoftonline.com/common/discovery/v2.0/keys'
    USER_INFO_ENDPOINT = 'https://graph.microsoft.com/oidc/userinfo'
    CLIENT_KWARGS = {'scope': 'openid profile email'}
    DATABASE_URI = os.environ.get("DATABASE_URI")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'


config = Config()
