# -*- coding: utf-8 -*-

from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.custom_header_auth import CustomHeaderAuth
from ..models.create_bulk_fx_quote_response import CreateBulkFXQuoteResponse
from ..models.get_indicative_fx_quote_response import GetIndicativeFXQuoteResponse
from ..models.create_fx_quote_response import CreateFXQuoteResponse
from ..exceptions.api_exception import APIException

class QuotesController(BaseController):

    """A Controller to access Endpoints in the earthport-rest-api-client API."""


    def create_bulk_fx_quote(self,
                             create_bulk_fx_quote_request=None):
        """Does a POST request to /quotes/bulk.

        Requests a bulk FX quote and creates a ticket for the quote.

        Args:
            create_bulk_fx_quote_request (list of CreateBulkFXQuoteRequest,
                optional): Bulk FX Quote Request.

        Returns:
            CreateBulkFXQuoteResponse: Response from the API. Quote
                succesfully retrieved.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/quotes/bulk'
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json',
            'content-type': 'application/json; charset=utf-8'
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(create_bulk_fx_quote_request))
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
        return APIHelper.json_deserialize(_context.response.raw_body, CreateBulkFXQuoteResponse.from_dictionary)

    def create_get_indicative_fx_quote(self,
                                       get_indicative_fx_quote_request=None):
        """Does a POST request to /quotes/indicative.

        Requests an  indicative quote

        Args:
            get_indicative_fx_quote_request (GetIndicativeFXQuoteRequest,
                optional): The request details to get an indicative FX quote.

        Returns:
            GetIndicativeFXQuoteResponse: Response from the API. Quote
                succesfully retrieved.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/quotes/indicative'
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json',
            'content-type': 'application/json; charset=utf-8'
        }

        # Prepare and execute request
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(get_indicative_fx_quote_request))
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
        return APIHelper.json_deserialize(_context.response.raw_body, GetIndicativeFXQuoteResponse.from_dictionary)

    def create_fx_quote(self,
                        user_id,
                        bank_id,
                        create_fx_quote_request=None,
                        id_type=None):
        """Does a POST request to /users/{userID}/bank-accounts/{bankID}/quotes.

        Requests a quote and creates a ticket for the quote.

        Args:
            user_id (string): The payer's unique id. It can be either VAN or
                merchant id.
            bank_id (string): Unique ID for the beneficiary bank account. It
                can be either earthport id or merchant id.
            create_fx_quote_request (CreateFXQuoteRequest, optional): The
                request details to get an FX quote and receive a unique Ticket
                ID with a time to live.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            CreateFXQuoteResponse: Response from the API. Quote succesfully
                retrieved.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/users/{userID}/bank-accounts/{bankID}/quotes'
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
        _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(create_fx_quote_request))
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
        return APIHelper.json_deserialize(_context.response.raw_body, CreateFXQuoteResponse.from_dictionary)
