from setuptools import setup, find_packages
import synergine_xyz

setup(
    name='synergine_xyz',
    version='0.0.1.11',
    packages=find_packages(),
    install_requires=['synergine'],
    author='Bastien Sevajol',
    author_email="synergine@bux.fr",
    description='Synergy 2d and 3d library',
    long_description=open('README.md').read(),
    include_package_data=True,
    url='https://github.com/buxx/synergine-xyz',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ]
)