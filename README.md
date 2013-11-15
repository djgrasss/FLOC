FLOC
====


ABOUT
-----

FLOC (Facebook Login OAuth CSRF detection tool) can be used to determine if a
web application's implementation of the Facebook OAuth Login flow is vulnerable
to CSRF.

A CSRF vulnerability in the implementation of this login flow can result in
account hijacking.

Facebook explicity mentions this login flow can be vulnerable to CSRF:
https://developers.facebook.com/docs/reference/dialogs/oauth/

FLOC has been tested with Python 2.7.3.


USAGE
-----

1. You will need the URL used by a webapp implementing the Facebook OAuth Login flow.
   This is the URL your browser will request from Facebook after clicking "Sign Up with Facebook", "Login with Facebook" etc.

2. e.g. For StackOverflow.com (after clicking "Log in Up with Facebook"), the URL will look like this:
```
https://www.facebook.com/dialog/oauth?client_id=145044622175352&scope=email&redirect_uri=https%3a%2f%2fstackauth.com%2fauth%2foauth2%2ffacebook%2f1%2f...%2f&state=...
```

3. There are currently 3 ways to get FLOC to examine the URL:
  1. Run FLOC from a shell like so, and enter the URL when prompted:
```
python floc.py
[>] Please enter a Facebook OAuth Login URL:
```
 2. Enter the URL into a file and have FLOC read it using the -f argument (this
    can be useful on OSX where the terminal is limited to 1023 characters):
```
python floc.py -f url.txt
```
  3. Pass FLOC the URL directly as an argument using the -u argument, e.g:
```
python floc.py -u "<facebook_oauth_login_url>"
```

4. FLOC will determine if the implementation is vulnerable or not:
```
[*] Implementation of Facebook OAuth Login doesn't appear vulnerable to CSRF ('state' parameter is not empty)
```


AUTHOR
------

@hyprwired (Brendan Jamieson)


VERSION
-------

v1.0.5


LICENCE
-------

FLOC is licenced under the GNU GPLv3 (See LICENCE)
