import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='concierge_freshdesk_plugin',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)',
    description='The Government of Canada freshdesk for Concierge',
    url='https://github.com/gctools-outilsgc/concierge-freshdesk-plugin',
    maintainer='GCTools Team',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)