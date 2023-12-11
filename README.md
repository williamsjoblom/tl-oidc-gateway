# ThinLinc OpenID Connect Gateway

`tl-oidc-gateway` is a web service sitting in front of ThinLinc's web client Web
Access that enables authentication with OpenID Connect.

In essence, it authenticates against an OpenID Connect provider and passes the
resulting token as the password to ThinLinc Web Access. On the server-side, the
token is then verified by the PAM module `pam_oidc`.

## PAM Configuration on the ThinLinc nodes

On both the master and agent nodes, install the PAM module `pam_oidc`:

https://github.com/salesforce/pam_oidc/releases

Then, make that PAM module part of your PAM stack. One example on how this can
be done is adding the following to the top of `/etc/pam.d/sshd` on all ThinLinc
nodes:

```
auth sufficient pam_oidc.so.0.0.5 issuer=https://example.com [user_template={{ .Extra.email | trimSuffix "@example.com"}}] aud=<OIDC client ID>
```

- The value of `issuer` has to match the `iss` claim of the OpenID Connect
  token, character by character. Therefore -- it is sensitive to a trailing
  slash.
- The above snippet takes the `email` claim of the OpenID Connect token, removes
  `@example.com` from the end of that email address, and then uses the result as
  the username.
- `aud` is the client ID.

## Patching the ThinLinc nodes

In available ThinLinc versions, a small patch to the obfuscated Python code is
needed:

```
--- /opt/thinlinc/modules/thinlinc/tlwebaccess/pamconversation.py	2023-12-06 17:54:49.798748781 +0100
+++ /opt/thinlinc/modules/thinlinc/tlwebaccess/pamconversation.py	2023-12-06 17:55:42.209365082 +0100
@@ -136,7 +136,7 @@
  def _read_line ( self , fd ) :
   IIIi1111iiIi1 = b""
   if 4 - 4: ooo000 % I1I - i1i1i1111I
-  iI11i1iI1I1Ii = 1024
+  iI11i1iI1I1Ii = 4096
   while iI11i1iI1I1Ii :
    oOoOO0O0 = os . read ( fd , 1 )
    if oOoOO0O0 == b"" :
```

This patch resolves the following known issue that is scheduled to be included
in ThinLinc 4.19.0:

https://bugzilla.cendio.com/show_bug.cgi?id=8262

## Install dependencies

```
$ pip install -r requirements.txt
```

## Configuration and running a development server

Set the configuration parameters in `config.py`
appropriately. `USERNAME_STRIP_SUFFIX` should match the `trimSuffix` argument in
the PAM `auth`-line configured above.

Note that it is instrumental to change `SECRET_KEY` before deployment. Such a
random key can be generated as follows:

```
python3 -c 'import secrets; print(secrets.token_urlsafe(16))'
```

The development server can then be run as follows:

```
python3 ./oidc.py
```

Then, navigate to `locahost:8080`. You will then be redirected to the OAuth
login portal, then redirected back to `localhost:8080/authorize`, and then
redirected and logged in to the ThinLinc server.

# Production deployment

Production deployment tested with Gunicorn behind Nginx.
