import setuptools
from distutils.core import setup

setup(
    name='bxmsdk',
    version='0.12.0',
    license='GNU GPL 3',
    author='Sagar Rao',	
    packages=['bxmsdk','bxmsdk.doe2','bxmsdk.energyplus','bxmsdk.energyplus.simEngine'],
	author_email='sagarurao@gmail.com',
    description='software development kit to develope models for building simulation',
    include_package_data=True,
    long_description=open('README.txt').read(),
)