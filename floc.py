#!/usr/bin/python

""" Tool to determine if a web application's implementation of the Facebook
    OAuth Login flow is vulnerable to CSRF.

    Refer to: https://developers.facebook.com/docs/reference/dialogs/oauth/"""

import argparse
from urlparse import parse_qs, urlparse

__author__ = '@hyprwired'
__version__ = '1.0.5'


class FLOC:

    def __init__(self):
        self.facebook_url = 'www.facebook.com'
        self.authenticated_path = '/dialog/oauth'
        self.unauthenticated_path = '/login.php'
        self.default_callback = '/auth/facebook/callback'
        self.valid_schemes = ['http', 'https']
        self.url_parsed = None
        self.authenticated_url = False
        self.redirect_uri = None
        self.redirect_uri_parsed = None
        self.client_id = None
        self.display = None
        self.scope = None
        self.state = None
        self.response_type = None

    def parse_raw_url(self, raw_url):
        print("[*] Parsing URL...")
        self.url_parsed = urlparse(raw_url)
        if self.url_parsed.scheme not in self.valid_schemes:
            raise Exception("[-] URL provided is not HTTP or HTTPS!")
        return True

    def check_if_url_facebook_login_oauth(self):
        print("[*] Checking if URL is Facebook OAuth Login URL...")
        known_paths = [self.authenticated_path, self.unauthenticated_path]

        if self.url_parsed.netloc == self.facebook_url:
            if self.url_parsed.path in known_paths:
                return True
            else:
                return False
        else:
            return False

    def determine_if_url_authenticated(self):
        print("[*] Determining if URL is for an authenticated user or not...")

        url_path = self.url_parsed.path
        if url_path == self.authenticated_path:
            self.authenticated_url = True
        elif url_path == self.unauthenticated_path:
            self.authenticated_url = False

        return self.authenticated_url

    def examine_url(self):
        print("[*] Examing URL...")

        parsed_qs = parse_qs(self.url_parsed.query)
        self.redirect_uri = parsed_qs['redirect_uri'][0]
        self.client_id = parsed_qs['client_id'][0]
        try:
            self.display = parsed_qs['display'][0]
        except KeyError:
            pass
        try:
            self.scope = parsed_qs['scope'][0]
        except KeyError:
            pass
        try:
            self.state = parsed_qs['state'][0]
        except KeyError:
            pass
        try:
            self.response_type = parsed_qs['response_type'][0]
        except KeyError:
            self.response_type = 'code'  # Facebook defaults to code

        print("\n" + ("=" * 21))
        print("Information from URL:")
        print("=" * 21)
        print("    'client_id': %s" % self.client_id)
        print(" 'redirect_uri': %s" % self.redirect_uri)
        print("      'display': %s" % self.display)
        print("        'scope': %s" % self.scope)
        print("        'state': %s" % self.state)
        print("'response_type': %s" % self.response_type)
        print("=" * 21)
        print("")

        if self.state is not None:
            print("[*] Implementation of Facebook OAuth Login doesn't appear" +
                  " vulnerable to CSRF ('state' parameter is not empty).")
        else:
            self.redirect_uri_parsed = urlparse(self.redirect_uri)

            if ((self.redirect_uri_parsed.path == self.default_callback) and
                    self.redirect_uri_parsed.query == ''):
                print("[!] Implementation of Facebook OAuth Login is " +
                      "vulnerable to CSRF.")
            else:
                print("[!] Implementation of Facebook OAuth Login is " +
                      "vulnerable to CSRF, IF the above redirect_uri doesn't" +
                      " contain a random string.")

        return True

    def check_vulnerable(self, raw_url):
        self.parse_raw_url(raw_url)

        if self.check_if_url_facebook_login_oauth():
            print("[*] URL is for Facebook OAuth Login.")

            self.determine_if_url_authenticated()
            if not self.authenticated_url:
                print("[*] URL is for an unauthenticated user.")
                print("[*] Attempting to get authenticated user URL...")
                try:
                    # Try to get the authenticated OAuth Dialog URL from 'next'
                    next_url = parse_qs(self.url_parsed.query)['next'][0]
                    self.parse_raw_url(next_url)
                except KeyError:
                    print("[-] ERROR: Not a Facebook OAuth Login URL.")
                    return False

            print("[*] URL being examined is for an authenticated user.")
            return self.examine_url()

        else:
            print("[-] ERROR: URL is not for Facebook OAuth Login.")


def print_tool_info():
    print("\n" + ("#" * 61))
    print("FLOC (Facebook Login OAuth CSRF detection tool) by %s" % __author__)
    print("Version: %s" % __version__)
    print(("#" * 61) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="File containing Facebook OAuth Login URL")
    parser.add_argument("-u", "--url", help="Facebook OAuth Login URL")
    args = parser.parse_args()
    print_tool_info()
    if args.file:
        print("[*] Reading URL from file: %s" % args.file)
        f = open(args.file, 'r')
        raw_url = f.readline()
        f.close()
    elif args.url:
        raw_url = args.url
    else:
        raw_url = raw_input("[>] Please enter a Facebook OAuth Login URL: ")
    floc_object = FLOC()
    floc_object.check_vulnerable(raw_url)


if __name__ == '__main__':
    main()
