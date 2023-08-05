#! /usr/bin/python3
from initialize.utils import InvalidTrigger, _input, get_github_link
from initialize.mappers import (PYTHON_PROJ, WORDPRESS_THEME, HTCSJS, JSLIB, SHTML,
								WORDPRESS_PLUGIN)
from datetime import datetime
from initialize._triggers import (readme_py, setup_py, gitignore_py, _index_html,
								  readme, license, project_format, authors,
								  editor_config, _style_css, plugin_php)
from initialize._license_template import license_dct, license_arr

class Trigger(object):
	"""
	This are functional triggers that can be assigned
	which will invoke when working with file creation
	"""
	def __init__(self, category):
		super(Trigger, self).__init__()
		self.category = category
		self._triggers = {}
		self._filters= {}

		# Adding Custom Triggers Here
		self.add_trigger('License', license)
		self.add_trigger('Authors', authors)
		self.add_trigger('.editorconfig', editor_config)
		self.add_trigger('Readme.md', readme)

		# Adding custom filters
		# A difference between filters they run on data not on enviornment
		self.add_filter('{0}', project_format)

	@staticmethod
	def clis(enviornment):
		"""
		Ads Enviornment Variables
		"""
		for idx, lic in enumerate(license_arr):
			print(idx, lic)
		license = _input("Select License Templates", default = 0)
		year = _input("Enter Year", default=datetime.now().year)
		author = _input("Enter Author Of Repo", allow_none = False)
		quick_description = _input("Small Description")
		version = _input("Enter Version", default = '0.1.0')
		github_repo = _input("Enter Github Repository Name",
							default = enviornment['project_name'])
		github_profile_name = _input("Enter Profile Name",
									  default = author)
		author_url = _input("Author Url", default = get_github_link(github_profile_name, github_repo))




		if enviornment['option'] == 'wp_theme':
			# enviornment related to ws_theme
			pass

		# Adding Enviornment
		enviornment['license'] = license
		enviornment['year'] = year
		enviornment['author'] = author
		enviornment['desc'] = quick_description
		enviornment['version'] = version
		enviornment['author_url'] = author_url
		enviornment['github_repo'] = github_repo
		enviornment['github_link'] = get_github_link(github_profile_name, github_repo)


	def add_trigger(self, name, trigger):
		"""
		This is used to add trigger to cetogery
		"""
		if not callable(trigger):
			raise InvalidTrigger("Improper Trigger Provided"
								 " Trigger Should Be Callable")
		self._triggers[name] = trigger


	def add_filter(self, name, trigger):
		"""
		This is used to add trigger to cetogery
		"""
		if not callable(trigger):
			raise InvalidTrigger("Improper Trigger Provided"
								 " Trigger Should Be Callable")
		self._filters[name] = trigger


	def process_trigger(self, working_path, trigger, enviornment):
		"""
		This is used to
		"""
		if trigger in self._triggers:
			self._triggers[trigger](working_path, trigger, enviornment);


	def process_filter(self, name, enviornment):
		"""
		This is used to
		"""
		if name in self._filters:
			x = self._filters[name](name, enviornment)
			return x
		else:
			return name


	def remove_trigger(self, name):
		"""
		This is used to remove trigger
		"""
		self._triggers.pop(name,None)


class JavascriptTrigger(Trigger):
	"""
	Triggers For javascript
	"""
	def __init__(self, category):
		super(JavascriptTrigger, self).__init__(category)


class Shtml(Trigger):
	"""A Simple Class Representing A shtml Trigger"""
	def __init__(self, category):
		super(Shtml, self).__init__(category)
		self.add_trigger('index.html', _index_html)


class Python(Trigger):
	"""A Python Project Accumulator"""
	def __init__(self, category):
		super(Python, self).__init__(category)

		# Adding A Custom Python Triggers
		self.add_trigger('Readme.rst', readme_py)
		self.add_trigger('setup.py', setup_py)
		self.add_trigger('.gitignore', gitignore_py)

	@staticmethod
	def clis(enviornment):
		""" A cli enviornment Attachment"""
		Trigger.clis(enviornment)
		packages = _input("Enter Packages", default=enviornment['project_name'])
		enviornment['packages'] = [package.strip() for package in packages.split(',')]


class Wp_Theme(Trigger):
	"""A Wordpress Theme Trigger Accumulator"""
	def __init__(self, category):
		super(Wp_Theme, self).__init__(category)
		self.add_trigger('style.css', _style_css)

	@staticmethod
	def clis(enviornment):
		""" A cli enviornment Attachment"""
		Trigger.clis(enviornment)
		theme_name = _input("Enter Theme Name", allow_none=False)
		theme_uri = _input("Enter Theme Url", default=enviornment['github_link'])
		author_url = _input("Enter Author Url", default=enviornment['github_link'])
		tags = _input("Enter Tags Comma Seperated")
		text_domain = _input("Enter Text Domain", allow_none=False)

		# Registering Enviornment
		enviornment['theme_name'] = theme_name
		enviornment['theme_uri'] = theme_uri
		enviornment['author_url'] = author_url
		enviornment['tags'] = tags
		enviornment['text_domain'] = text_domain

class Wp_Plugin(Trigger):
	"""
	Trigger
	"""
	def __init__(self, category):
		super(Wp_Plugin, self).__init__(category)
		self.add_filter('{0}.php', project_format)

	def process_filter(self, name, enviornment):
		"""
		Here Function is Re-implemented
		"""
		if name == '{0}.php':
			trg = name.format(enviornment['project_name'])
			self.add_trigger(trg, plugin_php)

		x = super(Wp_Plugin,self).process_filter(name, enviornment)
		return x

	@staticmethod
	def clis(enviornment):
		Trigger.clis(enviornment)
		plugin_name = _input("Enter Plugin Name", allow_none=False)
		plugin_uri = _input("Enter Plugin Url", default=enviornment['github_link'])
		author_url = _input("Enter Author Url", default=enviornment['github_link'])
		text_domain = _input("Enter Text Domain", allow_none=False)

		# Registering Enviornment
		enviornment['plugin_name'] = plugin_name
		enviornment['plugin_uri'] = plugin_uri
		enviornment['author_url'] = author_url
		enviornment['text_domain'] = text_domain


javascript 	= JavascriptTrigger('javascript')
python 		= Python('python')
html 		= Shtml('html')
shtml 		= Shtml('shtml')
wp_theme 	= Wp_Theme('wp_theme')
wp_plugin 	= Wp_Plugin('wp_plugin')


HeadshorTriggers = {'javascript': javascript ,
			 'python': python ,
			 'html' : html,
			 'wp_theme' : wp_theme ,
			 'shtml': shtml,
			 'wp_plugin': wp_plugin
			 }
