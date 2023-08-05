import sys
from os import path
from io import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
src_dir = path.join(here, "src")

# When executing the setup.py, we need to be able to import ourselves, this
# means that we need to add the src/ directory to the sys.path.
sys.path.insert(0, src_dir)

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pyarcanist',
    version='0.0.1',
    description='Pure python cli for Phabricator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Software Heritage developers',
    author_email='swh-devel@inria.fr',
    url="https://forge.softwareheritage.org/source/pyarcanist/",
    install_requires=[
        'beaker',
        'click',
        'gitpython',
        'humanize',
        'phabricator',
    ],
    package_dir={"": "src"},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'pyarc=pyarcanist.cli:pyarc']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    )
