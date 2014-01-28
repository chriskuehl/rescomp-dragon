#!/usr/bin/env python3
import calnet_login, calnet_credentials
from urllib.request import urlopen

REDIRECT_PREFIX = "https://net-auth-"
REDIRECT_SUFFIX = ".housing.berkeley.edu/"
RESCOMP_LOGIN_PATH = "cgi-bin/pub/wireless-auth/rescomp.cgi?mode=calnet"

def attempt_login(login_server, username, password):
	"""Attempts to authenticate to ResComp with the given credentials."""

	return_url = login_server + RESCOMP_LOGIN_PATH

	try:
		url = calnet_login.login(return_url, username, password)
		print("Authenticated successfully, welcome to the internet.")
	except calnet_login.LoginError as ex:
		print("Authentication failed with the following error:")
		print("\t{}".format(ex))
	except Exception as ex:
		print("Authentication failed with unexpected error:")
		print("\t{}".format(ex))

def authenticate(login_server):
	print("We appear to be using ResComp, proceeding with login.")
	print("\tLogin server: {}".format(login_server))

	username, password = calnet_credentials.get_credentials()
	attempt_login(login_server, username, password)
