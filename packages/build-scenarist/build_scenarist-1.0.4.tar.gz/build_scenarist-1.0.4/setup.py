# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io
import os
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(*names, **kwargs):
      with io.open(os.path.join(os.path.dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fp:
            return fp.read()

def find_version(*file_paths):
      version_file = read(*file_paths)
      version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
      if version_match:
            return version_match.group(1)
      raise RuntimeError("Unable to find version string.")

setup(name='build_scenarist',
      version=find_version("build_scenarist", "__init__.py"),
      description="Make-like utility to execute platform-dependent scripts (scenarios) written in Python 2.7. Format of scenario-name consist information about platform it written. Scenarios consist of targets",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/sogimu/scenarist',
      author='Aleksandr Lizin',
      author_email='sogimu@nxt.ru',
      license='MIT',
      packages=find_packages(),
      scripts=['scenarist.py'],
      package_data={'build_scenarist': ['src/*']},
      zip_safe=True,
      classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      )
