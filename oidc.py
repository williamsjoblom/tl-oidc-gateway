from authlib.integrations.flask_client import OAuth
from flask import Flask, url_for, render_template

app = Flask(__name__)
app.config.from_object('config')

oauth = OAuth()
oauth.init_app(app)
oauth.register(
    name='client',
    client_id=app.config['OIDC_CLIENT_ID'],
    client_secret=app.config['OIDC_CLIENT_SECRET'],
    server_metadata_url=app.config['OIDC_DISCOVERY_URL'],
    client_kwargs={'scope': ' '.join(app.config['OIDC_SCOPE'])}
)

def strip_username(username):
    '''
    Remove `USERNAME_STRIP_PREFIX` and `USERNAME_STRIP_SUFFIX` from `username`.
    '''
    prefix = app.config['USERNAME_STRIP_PREFIX']
    suffix = app.config['USERNAME_STRIP_SUFFIX']

    if prefix:
        if not username.startswith(prefix):
            raise Exception(
                f"Username '{username}' does not start with required prefix"
            )
        username = username[len(prefix):]
    if suffix:
        if not username.endswith(suffix):
            raise Exception(
                f"Username '{username}' does not end with required suffix"
            )
        username = username[:-len(suffix)]

    return username

@app.route('/')
def index():
    client = oauth.client
    if client is None:
        raise Exception("Remote application not registered")
    redirect_uri = url_for('authorize', _external=True)
    return client.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    client = oauth.client
    if client is None:
        raise Exception("Remote application not registered")

    token = client.authorize_access_token()

    username_claim = token['userinfo'][app.config['USERNAME_CLAIM']]
    username = strip_username(username_claim)
    id_token = token['id_token'] # What's passed as the password to PAM

    # Redirecting straight to the Web Access URL with the credentials in the
    # query parameters will result in a browser history entry containing the
    # token. Let's avoid this by doing a POST instead of a redirect (and GET).
    return render_template(
        'post-to-webaccess.html', username=username, token=id_token,
        webaccess_url=app.config['WEBACCESS_URL']
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
