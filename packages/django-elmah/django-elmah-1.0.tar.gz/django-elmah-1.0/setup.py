import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-elmah',
    version='1.0',
    packages=find_packages(exclude=['djelmah-server']),
    include_package_data=True,
    license='GNU Affero General Public License v3',
    description='Django Error Logging Modules and Handlers',
    long_description=README,
    url='https://github.com/rickjordan/django-elmah',
    author='Rick Jordan',
    author_email='jordan.rick.d@gmail.com',
    install_requires=[
        'django-tastypie',
        'requests',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
