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

import argparse
import functools
import json
import logging
import os
import sys
import time

import requests


LOG_FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT)
LOG = logging.getLogger(__name__)

ENDPOINT = 'https://pasted.tech/api/pastes'


class Error(Exception):
    pass


class MaxLengthExceeded(Error):
    pass


class UnexpectedError(Error):
    pass


class UrlNotFound(Error):
    pass


def retry(ExceptionToCheck, tries=5, delay=1, backoff=2):
    """Retry calling the decorated function using an exponential backoff.

    :param ExceptionToCheck: the exception to check. may be a tuple of
                             exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the
                    delay each retry
    :type backoff: int
    """
    def deco_retry(f):
        @functools.wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck:
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry
    return deco_retry


class Client(object):
    """A client library for pasteraw.

    To use pasteraw.com:

    >>> c = pasted.Client()
    >>> url = c.create_paste('Lorem ipsum.')
    >>> print(url)
    http://cdn.pasteraw.com/9lvwkwgrgji5gbhjygxgaqcfx3hefpb

    If you're using your own pasteraw deployment, pass your own API endpoint to
    the client:

    >>> c = pasteraw.Client('http://pasted.example.com/api/pastes')

    """

    def __init__(self, endpoint=None):
        """Initialize a pasteraw client for the given endpoint (optional)."""
        self.endpoint = endpoint or ENDPOINT
        LOG.debug('Endpoint: %s', ENDPOINT)

    @retry(UrlNotFound)
    def _validate_paste(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            print('Its likely the server is busy or the object store backend'
                  ' is not responding as quick as we would like. Rest assured'
                  ' your pasted content has been written given the POST'
                  ' returned a URL. Please wait a couple of minutes for the'
                  ' content to be rendered by the site.')
            print('URL: {}'.format(url))
            raise UrlNotFound(url)
        else:
            return url

    def create_paste(self, content):
        """Create a raw paste of the given content.

        Returns a URL to the paste, or raises a ``pasteraw.Error`` if something
        tragic happens instead.

        """
        content_length = len(content)
        LOG.debug('Content-Length: %d', content_length)

        r = requests.post(
            self.endpoint,
            data=json.dumps({'content': content}),
            headers={'content-type': 'application/json'}
        )

        if r.status_code == 201:
            return self._validate_paste(r.text)
        elif r.status_code == 302:
            return r.headers['Location']
        elif r.status_code == 413:
            raise MaxLengthExceeded('%d bytes' % len(content))
        else:
            print(r.text)
            raise UnexpectedError(r.headers)


def main(args):
    LOG.debug('File-Count: %d', len(args.files))

    client = Client(args.endpoint)
    if args.files:
        for arg_file in args.files:
            if os.path.isfile(arg_file):
                LOG.debug('Content-Length: %s', arg_file)
                with open(arg_file) as f:
                    url = client.create_paste(f.read())
                    print(url)
    else:
        url = client.create_paste(''.join(sys.stdin.readlines()))
        print(url)


def cli():
    parser = argparse.ArgumentParser(
        prog='pasted-client',
        description='Pipe `STDIN` or upload files to a raw paste. Get a URL back.'
                    ' Go be productive.')
    parser.add_argument(
        'files', metavar='file', nargs='*',
        help='one or more file names')
    parser.add_argument(
        '--endpoint', default=ENDPOINT,
        help=argparse.SUPPRESS)
    parser.add_argument(
        '--debug', action='store_true',
        help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.debug:
        LOG.setLevel(logging.DEBUG)
    else:
        LOG.setLevel(logging.WARN)

    main(args)


if __name__ == '__main__':
    cli()
