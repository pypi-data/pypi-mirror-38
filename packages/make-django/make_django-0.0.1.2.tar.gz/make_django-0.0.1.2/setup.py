import setuptools
from distutils.core import setup
import main

setup(
	name=main.__name__,
	version=main.__version__,
	py_modules=['make_django'],
	install_requires=['virtualenv', 'redbaron'],
	license='MIT',
	author=main.__author__,
	author_email='filantus@mail.ru',
	description=main.__doc__,
	packages=setuptools.find_packages(),
	include_package_data=True,
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.7'
	]
)
