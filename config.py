# Secret key for encrypting cookies (used by Flask and in turn authlib)
SECRET_KEY = '<replace with a secret as per README.md>'

# JWT claim containing the username
USERNAME_CLAIM = "email"

# Prefix to strip from the value of the given username claim. Raises an error if
# this prefix is not present.
USERNAME_STRIP_PREFIX = None

# Suffix to strip from the value of the given username claim. Raises an error if
# this suffix is not present.
USERNAME_STRIP_SUFFIX = "@example.com"

# The URL to the ThinLinc master node webaccess page.
WEBACCESS_URL = "https://thinlinc.example.com:300/"

# OAuth2/OpenID parameters.
OIDC_DISCOVERY_URL = "<discovery url>"
OIDC_SCOPE = [ 'openid', 'email' ]
OIDC_CLIENT_ID = '<client ID>'
OIDC_CLIENT_SECRET = '<client secret>'
