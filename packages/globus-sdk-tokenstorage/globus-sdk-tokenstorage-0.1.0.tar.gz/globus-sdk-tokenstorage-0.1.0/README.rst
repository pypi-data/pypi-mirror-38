.. image:: https://travis-ci.org/sirosen/globus-sdk-tokenstorage.svg?branch=master
    :alt: build status
    :target: https://travis-ci.org/globus/globus-sdk-tokenstorage

.. image:: https://img.shields.io/pypi/v/globus-sdk-tokenstorage.svg
    :alt: Latest Released Version
    :target: https://pypi.org/project/globus-sdk-tokenstorage/

.. image:: https://img.shields.io/pypi/pyversions/globus-sdk-tokenstorage.svg
    :alt: Supported Python Versions
    :target: https://pypi.org/project/globus-sdk-tokenstorage/

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :alt: License
    :target: https://opensource.org/licenses/Apache-2.0


Globus SDK TokenStorage
=======================

Th Globus SDK provides a convenient Pythonic interface to
`Globus <https://www.globus.org>`_ APIs.

This library provides an interface for handling the storage and management of
tokens acquired through the SDK more easily.

It takes tokens, stores and loads them to and from files, and additionally
provides `on_refresh` callbacks which can be used in
`globus_sdk.RefreshTokenAuthorizer` and
`globus_sdk.ClientCredentialsAuthorizer` to keep those files up-to-date.

Intentional limitation: this library does not generate Authorizers or Clients,
and is limited only to token and file management.

In the future, this may expand to include storage mechanisms which are not
files.

Links
-----

- Full documentation: https://globus-sdk-tokenstorage.readthedocs.io/en/latest/
