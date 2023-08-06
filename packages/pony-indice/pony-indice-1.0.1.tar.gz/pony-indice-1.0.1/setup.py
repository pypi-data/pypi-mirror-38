import os
from setuptools import find_packages, setup
import pony_indice

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='pony-indice',
    version=pony_indice.__version__,
    py_modules=['pony_indice'],
    packages=find_packages(exclude=[]),
    include_package_data=True,
    license=pony_indice.__license__,
    description=pony_indice.__doc__,
    long_description=README,
    url=pony_indice.__url__,
    author=pony_indice.__author__,
    author_email=pony_indice.__email__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
    ],
)
