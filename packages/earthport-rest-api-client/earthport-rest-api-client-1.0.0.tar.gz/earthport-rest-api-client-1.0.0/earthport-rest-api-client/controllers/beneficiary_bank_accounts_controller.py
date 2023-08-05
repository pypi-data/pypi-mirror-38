# -*- coding: utf-8 -*-

from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.custom_header_auth import CustomHeaderAuth
from ..models.get_expected_settlement_date_response import GetExpectedSettlementDateResponse
from ..models.validate_beneficiary_bank_account_response import ValidateBeneficiaryBankAccountResponse
from ..models.users_bank_id import UsersBankID
from ..models.list_bank_accounts_response import ListBankAccountsResponse
from ..models.get_beneficiary_bank_account_response import GetBeneficiaryBankAccountResponse
from ..exceptions.api_exception import APIException

class BeneficiaryBankAccountsController(BaseController):

    """A Controller to access Endpoints in the earthport-rest-api-client API."""


    def create_get_expected_settlement_date(self,
                                            get_expected_settlement_date_request):
        """Does a POST request to /bank-accounts/expected-settlement.

        Vaidates a new beneficiary bank account and get expected settlement
        date.

        Args:
            get_expected_settlement_date_request
                (GetExpectedSettlementDateRequest): The beneficiary bank
                account.

        Returns:
            GetExpectedSettlementDateResponse: Response from the API. Bank
                Account Valid.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/bank-accounts/expected-settlement'
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json',
            'content-type': 'application/json; charset=utf-8'
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(get_expected_settlement_date_request))
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
        return APIHelper.json_deserialize(_context.response.raw_body, GetExpectedSettlementDateResponse.from_dictionary)

    def create_validate_beneficiary_bank_account(self,
                                                 validate_beneficiary_bank_account_request):
        """Does a POST request to /bank-accounts.

        Vaidates a new beneficiary bank account against a User.

        Args:
            validate_beneficiary_bank_account_request
                (ValidateBeneficiaryBankAccountRequest): The beneficiary bank
                account.

        Returns:
            ValidateBeneficiaryBankAccountResponse: Response from the API.
                Bank Account Valid.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/bank-accounts'
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json',
            'content-type': 'application/json; charset=utf-8'
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(validate_beneficiary_bank_account_request))
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
        return APIHelper.json_deserialize(_context.response.raw_body, ValidateBeneficiaryBankAccountResponse.from_dictionary)

    def create_beneficiary_bank_account(self,
                                        create_beneficiary_bank_account_request,
                                        user_id,
                                        id_type=None):
        """Does a POST request to /users/{userID}/bank-accounts.

        Registers a new beneficiary bank account against a User.

        Args:
            create_beneficiary_bank_account_request
                (CreateBeneficiaryBankAccountRequest): The beneficiary bank
                account.
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            UsersBankID: Response from the API. Bank Account succesfully
                created.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}/bank-accounts'
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
            'accept': 'application/json',
            'content-type': 'application/json; charset=utf-8'
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(create_beneficiary_bank_account_request))
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
        return APIHelper.json_deserialize(_context.response.raw_body, UsersBankID.from_dictionary)

    def list_bank_accounts(self,
                           user_id,
                           offset=None,
                           page_size=None,
                           id_type=None):
        """Does a GET request to /users/{userID}/bank-accounts.

        Gets all Beneficiary Bank Accounts registered by this User.

        Args:
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            offset (int, optional): This is used for pagination of resultsets.
                0-based starting offset of the page with respect to the entire
                resultset.
            page_size (int, optional): This is used for pagination of
                resultsets. Number of items per page to return. If empty the
                maximum allowable (25) number of records will be returned.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            ListBankAccountsResponse: Response from the API. Bank Accounts
                succesfully returned.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}/bank-accounts'
        _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
            'userID': user_id
        })
        _query_parameters = {
            'offset': offset,
            'pageSize': page_size,
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
        return APIHelper.json_deserialize(_context.response.raw_body, ListBankAccountsResponse.from_dictionary)

    def get_beneficiary_bank_account(self,
                                     user_id,
                                     bank_id,
                                     id_type=None):
        """Does a GET request to /users/{userID}/bank-accounts/{bankID}.

        Gets a Beneficiary Bank Account.

        Args:
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            bank_id (string): Unique ID for the beneficiary bank account. It
                can be either earthport id or merchant id.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            GetBeneficiaryBankAccountResponse: Response from the API. Bank
                Accounts succesfully returned.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}/bank-accounts/{bankID}'
        _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
            'userID': user_id,
            'bankID': bank_id
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
        return APIHelper.json_deserialize(_context.response.raw_body, GetBeneficiaryBankAccountResponse.from_dictionary)

    def delete_deactivate_beneficiary_bank_account(self,
                                                   user_id,
                                                   bank_id,
                                                   id_type=None):
        """Does a DELETE request to /users/{userID}/bank-accounts/{bankID}.

        Deactivates a Beneficiary Bank Account. You will not be able to send a
        payment to a deactivated bank account.

        Args:
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            bank_id (string): Unique ID for the beneficiary bank account. It
                can be either earthport id or merchant id.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            void: Response from the API. Bank Accounts succesfully
                deactivated.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}/bank-accounts/{bankID}'
        _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
            'userID': user_id,
            'bankID': bank_id
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
