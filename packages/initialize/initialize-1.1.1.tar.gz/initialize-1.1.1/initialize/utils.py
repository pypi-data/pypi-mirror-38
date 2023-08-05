#! /usr/bin/python3


# Predefined Errors
import os

class InvalidTrigger(ValueError):
	"""
	This is raised when trigger of invalid type is raised
	"""
	def __init__(self, msg):
		super(InvalidTrigger,self).__init__(msg)


def printusage():
	print("\n"
			"usage: initialize [options] category\n\n"
			"options:\n"
			"	q : for quite \n"
			"\n"
			"category:\n"
			"	javascript: for javascript standard libray structure\n"
			"	python: for python standard libray structure\n"
			"	html: for html standard libray structure\n"
			"	ws_theme: for standard ws_theme structure\n")


def printmessage(message, customizations):
	"""
	Used to print Message to console
	"""
	if '-q' in customizations['customizations']:
		pass
	else:
		print(message)


def create_badges_table():
	"""
	This Function is used to create Badges Table inside
	Readme
	"""
	pass


def _input(message, allow_none = True, default = None):
	"""
	This is used to take input
	"""
	message = _prepare_input(message, default)
	while True:
		value = input(message)
		if allow_none and value == '' and default is not None:
			return default
		elif not allow_none and value == '':
			print("Value Required")
			pass
		else:
			return value


def _prepare_input(message, default = None):
	"""
	Used to prepare input string
	"""
	if default is not None:
		message = message + ' [' + str(default) + ']: '
		return message
	return message + ' : '


def write_to_file(working_path, file, environment ,content):
    """
    Summary
    """
    path = os.path.join(working_path,file)
    if os.path.exists(path):
    	with open(path, 'w') as f:
    		f.write(content)

def get_github_link(owner, repo):
	"""
	This will be used to get gitub link
	"""
	return 'https://github.com/{owner}/{repo}'.format(owner = owner,repo = repo)

