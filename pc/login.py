#!/usr/bin/env python3
import airbears_login, rescomp_login, random, string
from urllib.request import urlopen

TEST_ADDRESS = "http://74.125.239.102/" # Google

def get_redirect_url():
	"""Return the URL a user is redirect to when attempting to access
	the internet."""

	# cache busting
	rand = "".join(random.choice(string.ascii_letters) for _ in range(20))

	with urlopen("{}?a={}".format(TEST_ADDRESS, rand)) as res:
		return res.geturl()

if __name__ == "__main__":
	url = get_redirect_url()

	# strip query strings
	if "?" in url:
		url = url[:url.index("?")]

	found_mod = False

	for mod in (airbears_login, rescomp_login):
		if url.startswith(mod.REDIRECT_PREFIX) and url.endswith(mod.REDIRECT_SUFFIX):
			found_mod = True
			mod.authenticate(url)
		
	if not found_mod:
		print("No authentication is necessary.")
