from setuptools import setup
import os
import re

# Load version from module (without loading the whole module)
with open('whammyjammer/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

here = os.path.abspath(os.path.dirname(__file__))

desc = "An example module that doesn't do anything except have a silly name."


setup(
    name='WhammyJammer',
    version=version,
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description=desc,
    license='BSD',
    long_description=desc,
    packages=['whammyjammer'],
    install_requires=[],
    keywords="example",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)