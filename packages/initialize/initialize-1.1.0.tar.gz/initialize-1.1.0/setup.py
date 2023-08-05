from setuptools import setup

def readme():
	with open('Readme.rst') as f:
		return f.read()

setup(
    name='initialize',
    version='1.1.0',
    packages=['initialize'],
    long_description=readme(),
    keywords='standard project structure template',
    url='https://github.com/AngrySoilder/initialize',
    license='MIT',
    author='Akash Chaudhari',
    author_email='chaudhari041@outlook.com',
    description='Automating Automation by creating automatic project structure',
    entry_points={
        'console_scripts': ['initialize=initialize:createworkingenviornment']
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
      ],
    include_package_data=True,
    zip_safe=False
)
