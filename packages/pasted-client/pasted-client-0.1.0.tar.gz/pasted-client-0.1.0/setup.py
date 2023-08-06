# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import setuptools


with open('README.rst', 'r') as r_file:
    README = r_file.read()


setuptools.setup(
    name = 'pasted-client',
    version = '0.1.0',
    description = 'Pasted client. Paste files or STDIN to a raw object.',
    long_description = README,
    author = 'Kevin Carter',
    author_email = 'kevin@cloudnull.com',
    url = 'http://github.com/cloudnull/pasted-client',
    install_requires = [
        'requests'
    ],
    packages = [
        'pasted_client'
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ],
    entry_points = {
        "console_scripts": [
            "pasted = pasted_client.pasted:cli"
        ]
    }
)
