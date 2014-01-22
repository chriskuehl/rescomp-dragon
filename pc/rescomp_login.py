#!/usr/bin/env python3
import calnet_login, random, string, getpass, json, os.path
from urllib.request import urlopen

TEST_ADDRESS = "http://74.125.239.102/" # Google
RESCOMP_PREFIX = "https://net-auth-"
RESCOMP_SUFFIX = ".housing.berkeley.edu/"
RESCOMP_LOGIN_PATH = "cgi-bin/pub/wireless-auth/rescomp.cgi?mode=calnet"

def get_login_server():
	"""Returns the ResComp login server in use, or False if authentication
	isn't required."""

	# cache busting
	rand = "".join(random.choice(string.ascii_letters) for _ in range(20))

	with urlopen("{}?a={}".format(TEST_ADDRESS, rand)) as res:
		url = res.geturl()

		if url.startswith(RESCOMP_PREFIX) and url.endswith(RESCOMP_SUFFIX):
			return url

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
	login_server = get_login_server()

	if login_server:
		print("We appear to be using ResComp, proceeding with login.")
		print("\tLogin server: {}".format(login_server))

		username, password = get_credentials()
		attempt_login(login_server, username, password)
	else:
		print("No authentication is necessary.")
