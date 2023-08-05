# -*- coding: utf-8 -*-

from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.custom_header_auth import CustomHeaderAuth
from ..models.user_id import UserID
from ..models.get_user_response import GetUserResponse
from ..exceptions.api_exception import APIException

class UsersController(BaseController):

    """A Controller to access Endpoints in the earthport-rest-api-client API."""


    def create_or_validate_user(self,
                                action=None,
                                beneficiary_country_code=None,
                                create_validate_user_request=None):
        """Does a POST request to /users.

        Registers a new user for the client. A User is responsible for
        registering the beneficiary bank account to which a payment is sent
        to. This normally means the User is the Payer. You can also use this
        API to validate the payer identity details of the User by supplying
        the optional request parameter action=validate.

        Args:
            action (ActionEnum, optional): action=validate, validates the user
                without storing it. This API currently supports validating the
                user identity only.
            beneficiary_country_code (string, optional): Valid supported ISO
                3166 2-character country code. This is required parameter when
                action=validate
            create_validate_user_request (CreateValidateUserRequest,
                optional): The user details to either be created or
                validated.

        Returns:
            UserID: Response from the API. User succesfully created.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users'
        _query_parameters = {
            'action': action,
            'beneficiaryCountryCode': beneficiary_country_code
        }
        _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
            _query_parameters, Configuration.array_serialization)
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json',
            'content-type': 'application/json; charset=utf-8'
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(create_validate_user_request))
        CustomHeaderAuth.apply(_request)
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
        return APIHelper.json_deserialize(_context.response.raw_body, UserID.from_dictionary)

    def get_user(self,
                 user_id,
                 id_type=None):
        """Does a GET request to /users/{userID}.

        Get a User/Payer. This API only returns the identity details of a
        User/Payer.

        Args:
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            GetUserResponse: Response from the API. User succesfully
                returned.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}'
        _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
            'userID': user_id
        })
        _query_parameters = {
            'idType': id_type
        }
        _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
            _query_parameters, Configuration.array_serialization)
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.http_client.get(_query_url, headers=_headers)
        CustomHeaderAuth.apply(_request)
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
        return APIHelper.json_deserialize(_context.response.raw_body, GetUserResponse.from_dictionary)

    def update_user(self,
                    user_id,
                    update_user_request=None,
                    id_type=None):
        """Does a PUT request to /users/{userID}.

        Updates a User/Payer. This API only supports updating the identity
        details of a User/Payer.

        Args:
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            update_user_request (UpdateUserRequest, optional): The user.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            void: Response from the API. User succesfully updated.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}'
        _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
            'userID': user_id
        })
        _query_parameters = {
            'idType': id_type
        }
        _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
            _query_parameters, Configuration.array_serialization)
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'content-type': 'application/json; charset=utf-8'
        }

        # Prepare and execute request
        _request = self.http_client.put(_query_url, headers=_headers, parameters=APIHelper.json_serialize(update_user_request))
        CustomHeaderAuth.apply(_request)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 400:
            raise APIException('The requested operation could not be performed. Input Request is invalid or incorrect.', _context)
        elif _context.response.status_code == 401:
            raise APIException('Unauthorized - Invalid API Key and Token.', _context)
        elif _context.response.status_code == 500:
            raise APIException('An internal error has occurred in the Earthport payment platform.', _context)
        self.validate_response(_context)

    def delete_disable_user(self,
                            user_id,
                            id_type=None):
        """Does a DELETE request to /users/{userID}.

        Disables a User - you cannot register new bank accounts against a
        disabled User or create payments for a disabled User.

        Args:
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            void: Response from the API. User succesfully disabled.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}'
        _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
            'userID': user_id
        })
        _query_parameters = {
            'idType': id_type
        }
        _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
            _query_parameters, Configuration.array_serialization)
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare and execute request
        _request = self.http_client.delete(_query_url)
        CustomHeaderAuth.apply(_request)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 400:
            raise APIException('The requested operation could not be performed. Input Request is invalid or incorrect.', _context)
        elif _context.response.status_code == 401:
            raise APIException('Unauthorized - Invalid API Key and Token.', _context)
        elif _context.response.status_code == 500:
            raise APIException('An internal error has occurred in the Earthport payment platform.', _context)
        self.validate_response(_context)

    def add_deposit_reference(self,
                              user_id,
                              add_deposit_reference_request,
                              id_type=None):
        """Does a POST request to /users/{userID}/deposit-references.

        Creates a deposit reference for a User. This deposit reference is
        unique and each merchant has their own prefix.

        Args:
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            add_deposit_reference_request (AddDepositReferenceRequest):
                Deposit Reference.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            void: Response from the API. Deposit Reference Created.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}/deposit-references'
        _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
            'userID': user_id
        })
        _query_parameters = {
            'idType': id_type
        }
        _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
            _query_parameters, Configuration.array_serialization)
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'content-type': 'application/json; charset=utf-8'
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(add_deposit_reference_request))
        CustomHeaderAuth.apply(_request)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 400:
            raise APIException('The requested operation could not be performed. Input Request is invalid or incorrect.', _context)
        elif _context.response.status_code == 401:
            raise APIException('Unauthorized - Invalid API Key and Token.', _context)
        elif _context.response.status_code == 500:
            raise APIException('An internal error has occurred in the Earthport payment platform.', _context)
        self.validate_response(_context)
