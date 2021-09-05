import os
from distutils.core import setup
from setuptools import setup, find_packages


here = os.path.dirname(__file__)

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pyresolver',
    description='Cool IoC container',
    long_description=long_description,
    url='https://github.com/zaryanezrya/pyresolver',
    license='MIT',
    author='Ivan Sharun',
    author_email='ivan@sha.run',
    keywords=['IoC', 'Inversion on control', 'resolve'],
    project_urls={
        'Source': 'https://github.com/zaryanezrya/pyresolver',
    },
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
