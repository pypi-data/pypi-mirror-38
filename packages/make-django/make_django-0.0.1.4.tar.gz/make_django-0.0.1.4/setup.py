import setuptools
from distutils.core import setup
from make_django import main

setup(
	name=main.__name__,
	version=main.__version__,
	py_modules=['make_django'],
	install_requires=['virtualenv', 'redbaron'],
	author=main.__author__,
	author_email='filantus@mail.ru',
	description=main.__doc__,
	packages=setuptools.find_packages(),
	include_package_data=True,
    license='GPL',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
)
