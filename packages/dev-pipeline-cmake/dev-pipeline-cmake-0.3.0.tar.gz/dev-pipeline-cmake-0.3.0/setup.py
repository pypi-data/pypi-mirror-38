#!/usr/bin/python3

from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="dev-pipeline-cmake",
    version="0.3.0",
    package_dir={
        "": "lib"
    },
    packages=find_packages("lib"),

    install_requires=[
        'dev-pipeline-build >= 0.3.0',
        'dev-pipeline-core >= 0.3.0'
    ],

    entry_points={
        'devpipeline.builders': [
            'cmake = devpipeline_cmake:_CMAKE_TOOL',
        ]
    },

    author="Stephen Newell",
    description="cmake plugin for dev-pipeline",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license="BSD-2",
    url="https://github.com/dev-pipeline/dev-pipeline-cmake",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities"
    ]
)
