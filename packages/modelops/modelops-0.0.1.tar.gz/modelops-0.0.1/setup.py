#!/usr/bin/env python

import re
from setuptools import find_packages, setup

# parameter variables
install_requires = []
dependency_links = []
package_data = {}

version = '0.0.1'


if __name__ == '__main__':

    setup(
        name='modelops',
        version=version,
        description='Framework for AI Model and Application Lifecycle Management',
        # author='IBM Research AI',
        # scripts=['bin/modelops'],
        packages=find_packages(exclude=('tests', 'tests.*')),
        package_data=package_data,
        # url='https://github.ibm.com/ModelOps/modelops',
        install_requires=install_requires,
        dependency_links=dependency_links,
        # test_suite='tests',
        license='Apache License 2.0',
        zip_safe=False,
        classifiers=[
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
        ]
    )
