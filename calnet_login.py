from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
from http.cookiejar import CookieJar
import re

CALNET_LOGIN_URL = "https://auth.berkeley.edu/cas/login"
CALNET_HIDDENFIELD_REGEX = r'<input type="hidden" name="lt" value="(.*?)" />'

def login(return_url, username, password):
	url = get_login_url(return_url)
	token = get_token(url)

	post_data = {
		"username": username,
		"password": password,
		"_eventId": "submit",
		"lt": token
	}

	req = Request(url, urlencode(post_data).encode("utf-8"))
	processor = HTTPCookieProcessor(CookieJar())
	opener = build_opener(processor)

	with opener.open(req) as res:
		new_url = res.geturl()

		if new_url.lower().startswith(CALNET_LOGIN_URL):
			raise LoginError("Redirected back to login form ({})".format(new_url))

		return new_url

def get_login_url(return_url):
	params = {"renew": True, "service": return_url}
	return CALNET_LOGIN_URL + "?" + urlencode(params)

def get_token(url):
	"""Fetches the value of the lt parameter used on the CalNet login
	form."""

	with urlopen(url) as res:
		html = res.read().decode("utf-8")
		return re.findall(CALNET_HIDDENFIELD_REGEX, html)[0]

class LoginError(Exception):
	pass
