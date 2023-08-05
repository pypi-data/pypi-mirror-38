from setuptools import setup

with open("README.txt", "r") as readme:
    long_description = readme.read()
    
setup(
   name='PyTech',
   version='0.6',
   description='Emulated computer, Documentation fixed.',
   author='Robert Bassett',
   author_email='bassett.w.robert@gmail.com',
   packages=['PyTech'],  #same as name
   long_description = long_description
)
