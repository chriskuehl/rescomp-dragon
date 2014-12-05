import re
from urllib.parse import urlencode
import requests

CALNET_LOGIN_URL = "https://cas-p1.calnet.berkeley.edu/cas/login"
CALNET_HIDDENFIELD_REGEX = r'<input type="hidden" name="lt" value="(.*?)" />'

def login(return_url, username, password):
	session = requests.session()
	url = get_login_url(return_url)
	token = get_token(session, url)

	post_data = {
		"username": username,
		"password": password,
		"_eventId": "submit",
		"execution": "e1s1",
		"lt": token
	}

	req = session.post(url, post_data)
	new_url = req.url

	if new_url.lower() != return_url:
		raise LoginError("Redirected to unexpected URL <{}>, expected URL <{}>".format(new_url, return_url))

	return new_url

def get_login_url(return_url):
	params = {"renew": True, "service": return_url}
	return CALNET_LOGIN_URL + "?" + urlencode(params)

def get_token(session, url):
	"""Fetches the value of the lt parameter used on the CalNet login
	form."""
	html = session.get(url).text
	return re.findall(CALNET_HIDDENFIELD_REGEX, html)[0]

class LoginError(Exception):
	pass
