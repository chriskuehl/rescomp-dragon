#!/usr/bin/env python3
import calnet_login, calnet_credentials

REDIRECT_PREFIX = "http://wlan.berkeley.edu/login/"
REDIRECT_SUFFIX = ""
AIRBEARS_RETURN_URL = "https://wlan.berkeley.edu/cgi-bin/login/calnet.cgi?url=&count=1"

def attempt_login(username, password):
	"""Attempts to authenticate to AirBears with the given credentials."""

	try:
		url = calnet_login.login(AIRBEARS_RETURN_URL, username, password)
		print("Authenticated successfully, welcome to the internet.")
	except calnet_login.LoginError as ex:
		print("Authentication failed with the following error:")
		print("\t{}".format(ex))
	except Exception as ex:
		print("Authentication failed with unexpected error:")
		print("\t{}".format(ex))

def authenticate(url):
	print("We appear to be using AirBears, proceeding with login.")

	username, password = calnet_credentials.get_credentials()
	attempt_login(username, password)
