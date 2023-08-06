import setuptools
import sys

with open("readme.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name = "7",
    packages = ["7"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "0.0.0",
    description = "Seven",
    author = "Carlos Abraham",
    author_email = "abraham@abranhe.com",
    url = "https://abranhe.com",
    classifiers=(
        "Programming Language :: Python",
        "Natural Language :: English",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ),
    project_urls={
        'Source': 'https://github.com/abranhe/7',
    },
)
