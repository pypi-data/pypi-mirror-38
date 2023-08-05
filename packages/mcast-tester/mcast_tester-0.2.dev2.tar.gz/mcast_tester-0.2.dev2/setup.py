

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mcast_tester',


    version='0.2dev2',

    description='An IP multicast traffic generator.',
    long_description='This is a multicast traffic generator with sender and reciever functions along with loss and I/O measurement.'
,

    url='https://github.com/kriswans/ipMCAST_Lab_Tools/tree/master/mcast_tester',


    author='Kris Swanson',
    author_email='kriswans@cisco.com',


    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',


        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',


        'License :: OSI Approved :: MIT License',



        'Programming Language :: Python :: 3.6',
    ],


    keywords=['Multicast','traffic-generator','IP-Multicast'],

	packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    python_requires='>=2.7',

    install_requires=[],

	package_data={
        'mcast_tester': ['helpfile.txt'],
    },


    data_files=['helpfile.txt'],



)
