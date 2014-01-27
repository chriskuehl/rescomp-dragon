#!/usr/bin/env python3
import calnet_login, calnet_credentials, random, string
from urllib.request import urlopen

TEST_ADDRESS = "http://74.125.239.102/" # Google
AIRBEARS_PREFIX = "http://wlan.berkeley.edu/login/"
AIRBEARS_RETURN_URL = "https://wlan.berkeley.edu/cgi-bin/login/calnet.cgi?url=&count=1"

def auth_required():
	"""Returns whether authentication is required."""

	# cache busting
	rand = "".join(random.choice(string.ascii_letters) for _ in range(20))

	with urlopen("{}?a={}".format(TEST_ADDRESS, rand)) as res:
		url = res.geturl()

		if url.startswith(AIRBEARS_PREFIX):
			return url

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

if __name__ == "__main__":
	if auth_required():
		print("We appear to be using AirBears, proceeding with login.")

		username, password = calnet_credentials.get_credentials()
		attempt_login(username, password)
	else:
		print("No authentication is necessary.")
