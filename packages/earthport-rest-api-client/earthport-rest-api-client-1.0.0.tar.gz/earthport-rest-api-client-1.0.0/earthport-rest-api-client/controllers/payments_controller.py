# -*- coding: utf-8 -*-

from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.custom_header_auth import CustomHeaderAuth
from ..models.payout_response import PayoutResponse
from ..models.get_payout_required_data_response import GetPayoutRequiredDataResponse
from ..exceptions.api_exception import APIException

class PaymentsController(BaseController):

    """A Controller to access Endpoints in the earthport-rest-api-client API."""


    def create_payment(self,
                       create_payment_request=None):
        """Does a POST request to /payments.

        Creates a User (or updates an existing User), adds a Beneficiary Bank
        Account to this user and creates a new payment.

        Args:
            create_payment_request (CreatePaymentRequest, optional): The
                payment request

        Returns:
            PayoutResponse: Response from the API. Payment succesfully
                created.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/payments'
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json',
            'content-type': 'application/json; charset=utf-8'
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(create_payment_request))
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
        return APIHelper.json_deserialize(_context.response.raw_body, PayoutResponse.from_dictionary)

    def create_payment_registered_beneficiary(self,
                                              user_id,
                                              bank_id,
                                              payment_registered_beneficiary_request=None,
                                              id_type=None):
        """Does a POST request to /users/{userID}/bank-accounts/{bankID}/payments.

        Creates a new payment for a previously registered beneficiary bank
        account (and user).

        Args:
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            bank_id (string): Unique ID for the beneficiary bank account. It
                can be either earthport id or merchant id.
            payment_registered_beneficiary_request
                (PaymentRegisteredBeneficiaryRequest, optional):
                CreatePaymentRegisteredBeneficiaryRequest
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            PayoutResponse: Response from the API. Payment succesfully
                created.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}/bank-accounts/{bankID}/payments'
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
            'accept': 'application/json',
            'content-type': 'application/json; charset=utf-8'
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(payment_registered_beneficiary_request))
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
        return APIHelper.json_deserialize(_context.response.raw_body, PayoutResponse.from_dictionary)

    def get_purpose_of_payment_metadata(self,
                                        user_id,
                                        bank_id,
                                        amount=None,
                                        currency=None,
                                        payer_type=None,
                                        service_level=None,
                                        id_type=None):
        """Does a GET request to /users/{userID}/bank-accounts/{bankID}/payments/meta.

        Returns Purpose of Payment metadata for a payment to a beneficiary
        bank account which has previously been registered.

        Args:
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            bank_id (string): Unique ID for the beneficiary bank account. It
                can be either earthport id or merchant id.
            amount (int, optional): Amount
            currency (string, optional): currency
            payer_type (string, optional): The type of Payer. Allowed values
                are authenticatedCaller, managedMerchant and user.
            service_level (string, optional): Service Level. Allowed values
                are standard and express.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            GetPayoutRequiredDataResponse: Response from the API. Payment
                metadata succesfully returned.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}/bank-accounts/{bankID}/payments/meta'
        _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
            'userID': user_id,
            'bankID': bank_id
        })
        _query_parameters = {
            'amount': amount,
            'currency': currency,
            'payerType': payer_type,
            'serviceLevel': service_level,
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
        return APIHelper.json_deserialize(_context.response.raw_body, GetPayoutRequiredDataResponse.from_dictionary)

    def get_metadata_for_payment_request(self,
                                         country_code,
                                         currency_code,
                                         beneficiary_identity_entity_type=None,
                                         locale=None,
                                         service_level=None):
        """Does a GET request to /payments/meta.

        Returns required field for creating the payment request.

        Args:
            country_code (string): Valid supported ISO 3166 2-character
                country code.
            currency_code (string): Valid supported ISO 4217 3-character
                currency code.
            beneficiary_identity_entity_type
                (BeneficiaryIdentityEntityTypeEnum, optional): Type of
                beneficiary identity
            locale (string, optional): Localization String e.g. en_GB, en_US
            service_level (string, optional): Service Level. Allowed values
                are standard and express.

        Returns:
            GetPayoutRequiredDataResponse: Response from the API. Payment
                metadata succesfully returned.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/payments/meta'
        _query_parameters = {
            'countryCode': country_code,
            'currencyCode': currency_code,
            'beneficiaryIdentityEntityType': beneficiary_identity_entity_type,
            'locale': locale,
            'serviceLevel': service_level
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
        return APIHelper.json_deserialize(_context.response.raw_body, GetPayoutRequiredDataResponse.from_dictionary)
