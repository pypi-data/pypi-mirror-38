# -*- coding: utf-8 -*-

from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.custom_header_auth import CustomHeaderAuth
from ..models.financial_transaction import FinancialTransaction
from ..models.cancel_transaction_response import CancelTransactionResponse
from ..models.search_transactions_response import SearchTransactionsResponse
from ..exceptions.api_exception import APIException

class TransactionsController(BaseController):

    """A Controller to access Endpoints in the earthport-rest-api-client API."""


    def get_transaction(self,
                        transaction_id,
                        id_type=None):
        """Does a GET request to /transactions/{transactionID}.

        Retrieves a Transaction.

        Args:
            transaction_id (string): A unique transaction ID. You can use
                earthport transaction id or merchant transaction reference.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            FinancialTransaction: Response from the API. Transaction
                succesfully retrieved.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/transactions/{transactionID}'
        _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
            'transactionID': transaction_id
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
        return APIHelper.json_deserialize(_context.response.raw_body, FinancialTransaction.from_dictionary)

    def delete_cancel_transaction(self,
                                  transaction_id,
                                  id_type=None):
        """Does a DELETE request to /transactions/{transactionID}.

        Cancels a Transaction.

        Args:
            transaction_id (string): A unique transaction ID. You can use
                earthport transaction id or merchant transaction reference.
            id_type (IdTypeEnum, optional): idType for the path parameters.
                This allows you to specify either your own UIDs or Earthport
                generated UIDs. The Earthport generated UIDs will be used by
                default.

        Returns:
            CancelTransactionResponse: Response from the API. Transaction
                succesfully Cancelled.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/transactions/{transactionID}'
        _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
            'transactionID': transaction_id
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
        _request = self.http_client.delete(_query_url, headers=_headers)
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
        return APIHelper.json_deserialize(_context.response.raw_body, CancelTransactionResponse.from_dictionary)

    def search_transactions(self,
                            managed_merchant_name=None,
                            currency=None,
                            start_date_time=None,
                            end_date_time=None,
                            amount_from=None,
                            amount_to=None,
                            sort_order=None,
                            sort_fields=None,
                            merchant_transaction_id=None,
                            transaction_type=None,
                            transaction_status_code=None,
                            offset=None,
                            page_size=None):
        """Does a GET request to /transactions.

        Search Transactions.

        Args:
            managed_merchant_name (string, optional): Managed Merchant Name.
            currency (string, optional): currency.
            start_date_time (string, optional): Start Date Time.
            end_date_time (string, optional): End Date Time.
            amount_from (float, optional): Amount From.
            amount_to (float, optional): Amount To.
            sort_order (SortOrderEnum, optional): Sort Order.
            sort_fields (list of string, optional): Sort Fields.
            merchant_transaction_id (string, optional):
                merchantTransactionID.
            transaction_type (TransactionTypeEnum, optional): Transaction
                Type.
            transaction_status_code (int, optional): Transaction Status Code.
            offset (int, optional): This is used for pagination of resultsets.
                0-based starting offset of the page with respect to the entire
                resultset.
            page_size (int, optional): This is used for pagination of
                resultsets. Number of items per page to return. If empty the
                maximum allowable (25) number of records will be returned.

        Returns:
            SearchTransactionsResponse: Response from the API. Transaction
                succesfully retrieved.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/transactions'
        _query_parameters = {
            'managedMerchantName': managed_merchant_name,
            'currency': currency,
            'startDateTime': start_date_time,
            'endDateTime': end_date_time,
            'amountFrom': amount_from,
            'amountTo': amount_to,
            'sortOrder': sort_order,
            'sortFields': sort_fields,
            'merchantTransactionID': merchant_transaction_id,
            'transactionType': transaction_type,
            'transactionStatusCode': transaction_status_code,
            'offset': offset,
            'pageSize': page_size
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
        return APIHelper.json_deserialize(_context.response.raw_body, SearchTransactionsResponse.from_dictionary)
