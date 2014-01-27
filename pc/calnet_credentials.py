import getpass, json, os.path

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
