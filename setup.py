import os
from setuptools import setup, find_packages


here = os.path.dirname(__file__)

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyresolver",
    description="Cool IoC container",
    long_description=long_description,
    url="https://github.com/zaryanezrya/pyresolver",
    license="MIT",
    author="Ivan Sharun",
    author_email="ivan@sha.run",
    keywords=["IoC", "Inversion of control", "resolve"],
    project_urls={
        "Source": "https://github.com/zaryanezrya/pyresolver",
    },
    version="0.0.3",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
