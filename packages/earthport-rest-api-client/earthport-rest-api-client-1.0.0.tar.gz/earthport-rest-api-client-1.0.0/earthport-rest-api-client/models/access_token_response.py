# -*- coding: utf-8 -*-


class AccessTokenResponse(object):

    """Implementation of the 'AccessTokenResponse' model.

    The OAuth 2.0 access token to be used in each subsequent API call.

    Attributes:
        token_type (string): Type of token.
        issued_at (string): Time the token was issued. This is milliseconds
            since epoch.
        access_token (string): The actual token which needs to be used to
            authorize each subsequent API request.
        expires_in (string): When this token expires in seconds.
        status (string): The status of the token.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "access_token":'access_token',
        "token_type":'token_type',
        "issued_at":'issued_at',
        "expires_in":'expires_in',
        "status":'status'
    }

    def __init__(self,
                 access_token=None,
                 token_type=None,
                 issued_at=None,
                 expires_in=None,
                 status=None):
        """Constructor for the AccessTokenResponse class"""

        # Initialize members of the class
        self.token_type = token_type
        self.issued_at = issued_at
        self.access_token = access_token
        self.expires_in = expires_in
        self.status = status


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        access_token = dictionary.get('access_token')
        token_type = dictionary.get('token_type')
        issued_at = dictionary.get('issued_at')
        expires_in = dictionary.get('expires_in')
        status = dictionary.get('status')

        # Return an object of this model
        return cls(access_token,
                   token_type,
                   issued_at,
                   expires_in,
                   status)


