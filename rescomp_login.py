#!/usr/bin/env python3
import calnet_login, random, string, getpass
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

login_server = get_login_server()

if login_server:
	print("We appear to be using ResComp, proceeding with login.")
	print("\tLogin server: {}".format(login_server))

	username = input("Enter your CalNet username: ")
	password = getpass.getpass()

	attempt_login(login_server, username, password)
else:
	print("No authentication is necessary.")
