# Creating Custom Functions to to Add it To Hook
# Python Specific

import os
from initialize.utils import write_to_file, get_github_link
from initialize._templates import (PYTHON_INSTALLATION, Contributing,
	GITIGNORE_PY, INDEX_HTML, EditorConfig, SETUP_PY, Wp_Theme_Header,
	Readme_Header, Wp_Plugin_Header, Wp_license)
from initialize._license_template import license_arr, license_dct


def readme_py(working_path, file, environment, storage = ''):
	"""
	Hook For Readme
	"""
	_storage = storage
	github_link = environment['github_link']
	package_name = environment['github_repo']
	_storage = _storage + PYTHON_INSTALLATION.format(package_name = environment['project_name'],
													github_link = environment['github_link'],
													git_folder = environment['project_name'])
	readme(working_path, file, environment, _storage)


def setup_py(working_path, file, environment):
	"""
	Creating Custom Triggers For Setup.py file python
	"""
	try:
		license_int = int(environment['license'])
	except ValueError:
		license_int = 0

	content = SETUP_PY.format(project_name=environment['project_name'],
							  version=environment['version'] ,
							  package_name=environment['project_name'],
							  project_url=environment['github_link'],
							  license=license_arr[license_int],
							  author=environment['author'],
							  author_email='',
							  description=environment['desc'])

	write_to_file(working_path, file, environment, content)



def gitignore_py(working_path, file, environment):
	"""
	Hook for gitignore File
	"""
	write_to_file(working_path, file, environment, GITIGNORE_PY)


# Html Css Javascript Configurations
def _index_html(working_path, file, environment):
	"""
	Index.html
	"""
	write_to_file(working_path, file, environment, INDEX_HTML)

# Wordpress Format
def _style_css(working_path, file, environment):
	"""
	Used to create style.css
	"""
	try:
		license_int = int(environment['license'])
	except ValueError:
		license_int = 0
	license = license_arr[license_int]
	content = Wp_Theme_Header.format(theme_name=environment['theme_name'],
									 theme_uri=environment['github_link'] ,
									 author=environment['author'],
									 author_uri=environment['github_link'],
									 description=environment['desc'] ,
									 version=environment['version'] ,
									 license= license ,
									 text_domain=environment['text_domain'] ,
									 tags= environment['tags'])
	write_to_file(working_path, file, environment, content)

def plugin_php(working_path, file ,environment):
	"""
	Works With Traditional Plugin
	"""
	"""
	Used to create style.css
	"""
	try:
		license_int = int(environment['license'])
	except ValueError:
		license_int = 0
	license = license_arr[license_int]
	content = Wp_Plugin_Header.format(theme_name=environment['plugin_name'],
									 theme_uri=environment['plugin_uri'] ,
									 author=environment['author'],
									 author_uri=environment['github_link'],
									 description=environment['desc'] ,
									 version=environment['version'] ,
									 license= license ,
									 text_domain=environment['text_domain']
									 )
	lic_content = license_dct[license].format(year = environment['year'],
											  author = environment['author'])

	lic_content = Wp_license.format(lic_content)
	content = content + lic_content
	write_to_file(working_path, file, environment, content)


# General Formatting Hooks
def readme(working_path, file, environment, storage = ''):
	"""
	This is used to create simple readme file
	"""
	_storage = ''
	prev_content = storage
	header = Readme_Header.format(readme_header=environment['project_name'],
								  readme_text=environment['readme_text'])
	Contrib = Contributing.format(github_link = environment['github_link'])
	_storage = _storage + header + prev_content + Contrib
	write_to_file(working_path, file, environment ,_storage)


def license(working_path, file, environment):
	"""
	Hook for license
	"""
	try:
		license_int = int(environment['license'])
	except ValueError:
		license_int = 0

	content = license_dct[license_arr[license_int]].format(year = environment['year'],author= environment['author'])
	write_to_file(working_path, file, environment, content)

def project_format(file, environment):
	"""
	Project Naming Formatter
	"""
	file = file.format(environment['project_name'])
	return file


def authors(working_path, file, environment):
	"""
	Hook For authors
	"""
	write_to_file(working_path, file, environment, environment['author'])


def editor_config(working_path, file, environment):
	"""
	For Editor Config Hook
	"""
	write_to_file(working_path, file, environment, EditorConfig)
