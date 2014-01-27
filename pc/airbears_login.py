#!/usr/bin/env python3
import calnet_login, random, string, getpass, json, os.path
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

def get_credentials():
	"""Gets username and password either from stored file or from the user."""

	username, password = get_stored_credentials()

	if username and password:
		print("Using stored credentials...")
	else:
		username = input("Enter your CalNet username: ")
		password = getpass.getpass()

		if input("Would you like to store these credentials? [yN] ") == "y":
			store_credentials(username, password)
			print("Credentials saved to ~/.rescompd")

	return username, password

def credentials_path():
	return os.path.expanduser("~/.rescompd")

def get_stored_credentials():
	"""Returns stored username and password, or None for both"""

	try:
		with open(credentials_path()) as f:
			return json.load(f)
	except IOError:
		return None, None

def store_credentials(username, password):
	with open(credentials_path(), "w") as f:
		json.dump((username, password), f)

if __name__ == "__main__":
	if auth_required():
		print("We appear to be using AirBears, proceeding with login.")

		username, password = get_credentials()
		attempt_login(username, password)
	else:
		print("No authentication is necessary.")
