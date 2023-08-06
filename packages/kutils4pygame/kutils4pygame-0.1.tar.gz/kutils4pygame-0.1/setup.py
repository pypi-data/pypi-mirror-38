#!/usr/bin/env python3
"""Setup module for kutils4pygame pkg."""
from setuptools import setup, find_packages
import os
import sys
import shutil
import stat
from setuptools.command.develop import develop
from setuptools.command.install import install
from abstract_requires import requires

pkg_name = "kutils4pygame"
parent_dir = os.path.dirname(os.path.realpath(__file__))
data_src_dir = pkg_name + "_data"
config_src_dir = pkg_name + "_config"
defaults_location = os.path.join(pkg_name, "defaults")

# Create scripts list
script_dir = os.path.join(parent_dir, "bin")
scripts = []
try:
    for f in os.listdir(script_dir):
        scripts.append(os.path.join(script_dir, str(f)))

except FileNotFoundError:
    pass

def reset():
    """Remove build dirs."""
    dirnames_to_remove = [pkg_name + ".egg-info", "dist", "build"]
    for d in dirnames_to_remove:
        shutil.rmtree(d, ignore_errors=True)

with open("README.md", "r") as fh:
    long_description = fh.read()

def setuptools_setup():
    """Setup provisioner."""
    setup(
        name="kutils4pygame",
        version="0.1",
        description="Thin wrapper on pygame for the creation of simple animations and games.",
        url="https://github.com/ku-wolf/kutils4pygame",
        author="Kevin Wolf",
        author_email="kevinuwolf@gmail.com",
        license="gplv3.txt",
        packages=find_packages(),
        scripts=scripts,
        install_requires=requires,
        setup_requires=requires,
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ],
    )


def main():
    """Main method."""
    os.chdir(parent_dir)

    if sys.argv[1] == "reset":
        reset()
    else:
        setuptools_setup()

if __name__ == "__main__":
    main()
