import json
import os

from .abstract_base import AbstractStorageAdapter
from .version import __version__


class AbstractFileAdapter(AbstractStorageAdapter):
    """
    File adapters are for single-user cases, where we can assume that there's a
    simple file-per-user and users are only ever attempting to read their own
    files.
    """

    def file_exists(self):
        """
        Check if the file used by this file storage adapter exists.
        """
        return os.path.exists(self.filename)

    def read_as_dict(self):
        raise NotImplementedError


class SimpleJSONFileAdapter(AbstractFileAdapter):
    """
    :param filename: the name of the file to write to and read from
    :param resource_server: the resource server name for tokens to look up
                            in a token response object
    :param scopes: a list of scope names for tokens to look up in a token
                   response object

    A storage adapter for storing tokens in JSON files.
    Callers must provide exactly one of ``resource_server`` and ``scopes``
    """

    def __init__(self, filename, resource_server=None, scopes=None):
        if resource_server and scopes:
            raise ValueError("cannot take both resource_server and scopes")
        elif not resource_server and not scopes:
            raise ValueError("you must pass resource_server or scopes")

        self.filename = filename
        self.resource_server = resource_server
        self.scopes = scopes

    def store(self, token_response):
        """
        By default, ``self.on_refresh`` is just an alias for this function.

        Given a token response, extract the token data for the configured
        scopes or resource servers of this file adapter and write it to
        ``self.filename`` as JSON data.
        Additionally will write the version of ``globus_sdk_tokenstorage``
        which was in use.

        Under the assumption that this may be running on a system with multiple
        local users, this sets the umask such that only the owner of the
        resulting file can read or write it.
        """
        # extract desired data and copy as a new dict
        if self.resource_server:
            to_write = dict(token_response.by_resource_server[self.resource_server])
        elif self.scopes:
            # NOTE: this can fail if `self.scopes` isn't for exactly one
            # resource server, but then the failure will simply propagate up
            to_write = dict(token_response.by_scopes[self.scopes])
        else:
            raise NotImplementedError("neither resource_server nor scopes are set")

        # deny rwx to Group and World, exec to User
        old_umask = os.umask(0o177)
        try:
            # add the version as an attribute at the top level of the JSON
            # structure
            to_write["globus-sdk-tokenstorage.version"] = __version__
            with open(self.filename, "w") as f:
                json.dump(to_write, f)
        finally:
            # reset umask
            os.umask(old_umask)

    def read_as_dict(self):
        """
        Load the config file contents as JSON and return the resulting dict
        object.

        Although the whole token response is passed in for ``self.store``, this
        will only return the token data for the particular scopes or resource
        server for which this File Adapter is configured.
        """
        with open(self.filename, "r") as f:
            return json.load(f)
