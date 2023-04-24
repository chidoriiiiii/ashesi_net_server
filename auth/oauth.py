from flask import current_app
from authlib.integrations.flask_client import OAuth
from config.config import config

oauth = OAuth(current_app)
oauth.register(
    name=config.MICROSOFT_REMOTE_APP,
    client_id=config.MICROSOFT_CLIENT_ID,
    client_secret=config.MICROSOFT_CLIENT_SECRET,
    api_base_url=config.API_BASE_URI,
    authorize_url=config.AUTHORIZE_URI,
    access_token_url=config.ACCESS_TOKEN_URI,
    jwks_uri=config.JWKS_URI,
    userinfo_endpoint=config.USER_INFO_ENDPOINT,
    client_kwargs=config.CLIENT_KWARGS
)
