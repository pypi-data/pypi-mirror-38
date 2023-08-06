=============
pasted-client
=============

Pipe `STDIN` or upload files to a raw paste. Get a URL back. Go be productive.

By default, `pasted` uses a hosted paste service, `pasted.tech
<http://pasted.tech/>`_. You can also deploy `your own instance
<https://github.com/cloudnull/pasted>`_ of the service and use it instead.

Installation
------------

.. image:: https://img.shields.io/badge/pasted-stable-brightgreen.svg
   :target: https://pypi.python.org/pypi/pasted-client

From PyPi::

    $ pip install pasted-client

Command line usage
------------------

Given a file::

    $ cat somefile
    Lorem ipsum.


Pipe the file to `pasted` and get back a URL to a raw paste of that file::

    $ cat somefile | pasted
    http://pasted.com/89001a7fbbe57e6921a91b2ba166fa98e1579cd2.raw


Do whatever you want with the URL. Curl it, email it, whatever::

    $ curl http://pasted.tech/89001a7fbbe57e6921a91b2ba166fa98e1579cd2.raw
    Lorem ipsum.


You can also paste multiple files without a pipe::

    $ pasted /path/to/file1 /path/to/file2 /path/to/file3
    https://pasted.tech/pastes/294b43b2cec9919063be1a3b49e8722648424779.raw
    https://pasted.tech/pastes/3c56f1d7f112e09002627d24b82446431df5039a.raw
    https://pasted.tech/pastes/f9372ce11a7370c54135f3c708131de123caf90f.raw


Python library usage
--------------------

To use `pasted.tech <http://pasted.tech/>`_::

    >>> c = pasted.Client()
    >>> url = c.create_paste('Lorem ipsum.')
    >>> print(url)
    http://pasted.tech/89001a7fbbe57e6921a91b2ba166fa98e1579cd2.raw

Alternatively, if you're using your own deployment of `pasteraw
<https://github.com/cloudnull/pasted>`_, pass your own API endpoint to the
client::

    >>> c = pasteraw.Client('http://pasted.example.com/api/pastes')

Usage is otherwise identical to using `pasted.tech <http://pasted.tech/>`_.
