import setuptools

setuptools.setup(
    name = "zb-common",
    version = "0.1.1",
    author = "Manjunath Somashekar",
    author_email = "ujnamss@gmail.com",
    packages = ["zb_common"],
    description = "A package containing all the common utilities for the Zerobugz project",
    url = "http://pypi.python.org/pypi/zb-common/",
    keywords = ["synthetic", "data", "generation"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
A package containing all the common utilities for the Zerobugz project
-----------------------------------------------------

This version requires Python 2.7 or later
""",
    install_requires=[
        "requests",
        "slackclient",
        "future>=0.16.0"
    ],
)
