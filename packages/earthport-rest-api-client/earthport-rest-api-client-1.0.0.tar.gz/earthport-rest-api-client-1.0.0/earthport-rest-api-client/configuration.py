# -*- coding: utf-8 -*-

from .api_helper import APIHelper


class Configuration(object):

    """A class used for configuring the SDK by a user.

    This class need not be instantiated and all properties and methods
    are accessible without instance creation.

    """

    # Set the array parameter serialization method
    # (allowed: indexed, unindexed, plain, csv, tsv, psv)
    array_serialization = "indexed"

    # An enum for SDK environments
    class Environment(object):
        # Production server.
        PRODUCTION = 0
        # Sandbox is used for both sandbox testing and customer UAT.
        SANDBOX = 1
        # Customer integration is used by existing clients who need to test new functionality before it is released onto sandbox and production.
        CUSTOMER_INTEGRATION = 2

    # An enum for API servers
    class Server(object):
        DEFAULT = 0
        AUTH = 1

    # The environment in which the SDK is running
    environment = Environment.SANDBOX

    # TODO: Set an appropriate value
    authorization = None


    # All the environments the SDK can run in
    environments = {
        Environment.PRODUCTION: {
            Server.DEFAULT: 'https://api.earthport.com/v1',
            Server.AUTH: 'https://api.earthport.com',
        },
        Environment.SANDBOX: {
            Server.DEFAULT: 'https://api-sandbox.earthport.com/v1',
            Server.AUTH: 'https://api-sandbox.earthport.com',
        },
        Environment.CUSTOMER_INTEGRATION: {
            Server.DEFAULT: 'https://api-integration.earthport.com/v1',
            Server.AUTH: 'https://api-integration.earthport.com',
        },
    }

    @classmethod
    def get_base_uri(cls, server=Server.DEFAULT):
        """Generates the appropriate base URI for the environment and the server.

        Args:
            server (Configuration.Server): The server enum for which the base URI is required.

        Returns:
            String: The base URI.

        """
        return cls.environments[cls.environment][server]
