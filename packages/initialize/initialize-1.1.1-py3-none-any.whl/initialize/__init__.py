#! /usr/bin/python3

import sys
import os
from sys import argv
from os.path import join
from os import getcwd
from sys import path
from subprocess import call
from initialize.utils import InvalidTrigger, printusage, printmessage, _input
from initialize.triggers import Trigger, HeadshorTriggers
from initialize.mappers import (PYTHON_PROJ, WORDPRESS_THEME, HTCSJS, JSLIB, SHTML,
								WORDPRESS_PLUGIN)
from subprocess import call
# main options
standard_main_options = ['javascript', 'python' , 'html', 'wp_theme', 'shtml', 'wp_plugin']
standard_sub_options = ['-q']

def createworkingenviornment():
	"""
	This function will create workig enviornment for
	other functions to work mainly
	"""
	if len(argv) > 1:
		option = argv[-1]
		customizations = argv[1: -1]

		if option not in standard_main_options:
			printusage()
			return

		for customization in customizations:
			if customization not in standard_sub_options:
				print(customization + " option does not exist")
				printusage()
				return

		project_name = _input('Enter Project Name', allow_none = False)
		readme = _input('Enter Readme Text Please', allow_none = False)

		enviornment = dict(option = option,
						   customizations = customizations,
						   project_name = project_name,
						   readme_text = readme)
		HeadshorTriggers[enviornment['option']].clis(enviornment)
		main(enviornment)

	else:
		printusage()
		return

def main(enviornment):
	# use to take enviornment


	# Main Path is
	main_path = join(getcwd(),enviornment['project_name'])
	option = enviornment['option']
	tasks = {'javascript': JSLIB ,
			 'python': PYTHON_PROJ,
			 'html' : HTCSJS,
			 'wp_theme' : WORDPRESS_THEME ,
			 'shtml': SHTML,
			 'wp_plugin': WORDPRESS_PLUGIN
			 }
	enviornment['main_path'] = main_path
	enviornment['tasks'] = tasks
	_create_files(main_path, tasks[option],enviornment)
	os.chdir(main_path)
	file = open('x.tmp','w')
	call(['git','init'], stdout = file)
	call(['git','add','*'])
	call(['git','commit','-m',"initial commit"], stdout = file)
	call(['git','tag','0.1.0'])
	call(['git','branch','dev'])
	call(['git','branch','docs'])
	file.close()
	os.remove('x.tmp')


def _create_files(working_path, files_to_create,enviornment):
	"""
	directory structrue is structure in form of
	"""
	if not os.path.exists(working_path):
		os.makedirs(working_path)

	for file in files_to_create:
		if isinstance(file, dict):
			_callback(working_path, file, enviornment)
		else:
			# Processing With Filters
			file = HeadshorTriggers[enviornment['option']].process_filter(file, enviornment)
			printmessage("Creating File: " + file, enviornment)
			_createfile(working_path, file)
			HeadshorTriggers[enviornment['option']].process_trigger(working_path, file, enviornment)

def _dct(dictionary):
	for name, value in dictionary.items():
		return (name, value)


def _createfile(file_path,file):
	file_path = join(file_path, file)
	open(file_path, 'w').close()

def _callback(current_path, dictionary, enviornment):
	"""
	Used to callback create_files_in_dict folder
	"""
	working_path, files = _dct(dictionary)
	working_path = HeadshorTriggers[enviornment['option']].process_filter(working_path, enviornment)
	working_path = join(current_path, working_path)
	printmessage("Going Inside Directory: " + working_path.split('/')[-1], enviornment)
	_create_files(working_path, files, enviornment)
