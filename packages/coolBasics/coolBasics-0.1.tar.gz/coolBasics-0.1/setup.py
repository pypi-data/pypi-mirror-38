from setuptools import setup

__project__ = "coolBasics"
__version__ = "0.1"
__description__ = "A Python module for having fun!"
__packages__ = ["basics"]
__author__ = "Arca Ege Cengiz"
__author_email__ = "arcaegecengiz@gmail.com"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]
__keywords__ = ["fun","python","basics","learning","motivation"]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    keywords = __keywords__,
)
