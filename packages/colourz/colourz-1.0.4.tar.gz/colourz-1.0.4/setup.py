"""This is a template setup file, hopefully you'll only need to change
the meta-data"""
import codecs
import os
import sys

from setuptools import setup, Command
from shutil import rmtree


# Package meta-data
NAME = 'colourz'
DESCRIPTION = ('Colourz adds coloured text output and spinners to a Windows '
               'shell  (Powershell / CMD)')
URL = 'https://github.com/alexmacniven/colourz.git'
EMAIL = 'apmacniven@outlook.com'
AUTHOR = 'Alex Macniven'

# What packages are required for this module to be executed?
REQUIRED = [
    'colorama'
]

# Import the README and use it as the long-description
# Note: README.md needs to be in the MANIFEST
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

# Load the package's __version__.py module as a dictionary
# Note: A seperate __version__.py is used so you can add imports to the
# __init__.py file
about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

class UploadCommand(Command):

    """Support setup.py publish."""
    description = "Build and publish the package."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            print("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except FileNotFoundError:
            pass

        print("Building Source distribution…")
        os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))
        print("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")
        print("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")
        sys.exit()

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=['colourz'],
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    cmdclass={
        'upload': UploadCommand
    }
)
