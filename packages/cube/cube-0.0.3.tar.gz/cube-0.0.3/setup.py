from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

setup(
    name='cube',
    version="0.0.3",
    description="Python bindings for interfacing with Cube.",
    long_description="", #TODO: write
    url="https://docs.cube.ai/",
    author_email="matkallada@gmail.com",
    license="", #TODO,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
        #"License :: ??", #TODO
    ],
    keywords="cube api",
    packages=['cube']
)
