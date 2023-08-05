# -*- coding: utf-8 -*-

from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..models.access_token_response import AccessTokenResponse
from ..exceptions.api_exception import APIException

class AuthenticationController(BaseController):

    """A Controller to access Endpoints in the earthport-rest-api-client API."""


    def create_get_access_token(self,
                                client_id,
                                client_secret,
                                grant_type='client_credentials'):
        """Does a POST request to /oauth/token.

        Verify client credentials and returns a bearer token

        Args:
            client_id (string): Client ID
            client_secret (string): Client Secret
            grant_type (GrantTypeEnum, optional): The grant type for OAuth2.0

        Returns:
            AccessTokenResponse: Response from the API. Access token
                generated.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri(Configuration.Server.AUTH)
        _query_builder += '/oauth/token'
        _query_parameters = {
            'grant_type': grant_type
        }
        _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
            _query_parameters, Configuration.array_serialization)
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'client_id': client_id,
            'client_secret': client_secret
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 400:
            raise APIException('The requested operation could not be performed. Input Request is invalid or incorrect.', _context)
        elif _context.response.status_code == 401:
            raise APIException('Unauthorized - Invalid API Key and Token.', _context)
        elif _context.response.status_code == 500:
            raise APIException('An internal error has occurred in the Earthport payment platform.', _context)
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, AccessTokenResponse.from_dictionary)
