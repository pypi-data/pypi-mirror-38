class AbstractStorageAdapter(object):
    def store(self, token_response):
        raise NotImplementedError

    def on_refresh(self, token_response):
        """
        By default, the on_refresh handler for a token storage adapter simply
        stores the token response.
        """
        return self.store(token_response)
