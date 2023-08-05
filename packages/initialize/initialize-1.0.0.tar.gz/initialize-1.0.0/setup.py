from setuptools import setup

setup(
    name='initialize',
    version='1.0.0',
    packages=['initialize'],
    url='',
    license='MIT',
    author='Akash Chaudhari',
    author_email='devilscyanide@gmail.com',
    description='Automating Automation by creating automatic project structure',
    entry_points={
        'console_scripts': ['initialize=initialize:createworkingenviornment']
    }
)
