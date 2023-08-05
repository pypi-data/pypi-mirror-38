# A Template Directory To Keep Track of  Templates


# ------------------License
License = """License
=======
{0}
"""

# -----------------This is Installation Text
# ----------------- package_name, github_link
PYTHON_INSTALLATION = """Installation
============

The `Python Packaging Guide`_ contains general information about how to manage
your project and dependencies.

.. _Python Packaging Guide: https://packaging.python.org/current/

Released version
----------------

Install or upgrade using pip. ::

    pip install -U {package_name}

Development
-----------

The latest code is available from `GitHub`_. Clone the repository then install
using pip. ::

    git clone {github_link}
    pip install -e ./{git_folder}

Or install the latest build from an `archive`_. ::

    pip install -U {github_link}/tarball/master

.. _GitHub: {github_link}
.. _archive: {github_link}/archive/master.tar.gz


"""



Contributing = """Contributing
=============

One Can Contribute to this project by **creating a issue at issue** at `{github_link}` Or **creating a pull request**

Pull Request Process
--------------------

1. Ensure any install or build dependencies are removed before the end of the layer when doing a
   build.
2. Checkout pull requests list at `{github_link}/pulls` to ensure that you are not dublicating anybody's work
3. Update the README.md with details of changes to the interface, this includes new environment
   variables, exposed ports, useful file locations and container parameters.
4. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
5. You may merge the Pull Request in once you have the sign-off of by other developers, or if you
   do not have permission to do that, you may request the one of maintainers of project to merge it for you.

Development Process
-------------------

* Create a local copy of repository in our machiene
* Install dependencies which are currently used by project
* Make Changes To your Project
* Write atleast Basic Test which covers your changes
* Improve docs with your changes
* Create a coverage report
* Pull...

How To issue
------------
While registering a issue it will be beneficial if creator of issue desribe following things about issue

* operating system he used
* steps to generte error or bug
* if not know steps in what function or method bug generated


"""


# Templates For index.html

INDEX_HTML = """<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Hello World</title>
	<link rel="stylesheet" href="css/index.css">
</head>
<body>

	<script src="js/index.js"></script>
</body>
</html>"""


# travis templates


# gitignore templates
# Taken From Github don't know from where but will be updated
# here when found


EditorConfig = """# http://EditorConfig.org

#################
# Common Settings
#################

# This file is the top-most EditorConfig file
root = true

# All Files
[*]
charset = utf-8
end_of_line = crlf
indent_style = space
indent_size = 4
insert_final_newline = false
trim_trailing_whitespace = true

#########################
# File Extension Settings
#########################

# Visual Studio Solution Files
[*.sln]
indent_style = tab

# Visual Studio XML Project Files
[*.{csproj,vbproj,vcxproj,vcxproj.filters,proj,projitems,shproj}]
indent_size = 2

# XML Configuration Files
[*.{xml,config,props,targets,nuspec,resx,ruleset,vsixmanifest,vsct}]
indent_size = 2

# JSON Files
[*.{json,json5}]
indent_size = 2

# YAML Files
[*.{yml,yaml}]
indent_size = 2

# Markdown Files
[*.md]
trim_trailing_whitespace = false

# Web Files
[*.{htm,html,js,ts,tsx,css,sass,scss,less,svg,vue}]
indent_size = 2
insert_final_newline = true

# Batch Files
[*.{cmd,bat}]

# Bash Files
[*.sh]
end_of_line = lf
"""

GITIGNORE_PY = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/"""


SETUP_PY = """from setuptools import setup

setup(
    name='{project_name}',
    version='{version}',
    packages=['{package_name}'],
    url='{project_url}',
    license='{license}',
    author='{author}',
    author_email='{author_email}',
    description='{description}'
)"""


