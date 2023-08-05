# -*- coding: utf-8 -*-

from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.custom_header_auth import CustomHeaderAuth
from ..models.statement import Statement
from ..exceptions.api_exception import APIException

class StatementsController(BaseController):

    """A Controller to access Endpoints in the earthport-rest-api-client API."""


    def get_statement(self,
                      managed_merchant_name=None,
                      currency=None,
                      start_date_time=None,
                      end_date_time=None,
                      sort_order=None,
                      offset=None,
                      page_size=None):
        """Does a GET request to /statements.

        Retrieves the statement of a merchant account.

        Args:
            managed_merchant_name (string, optional): The name of managed
                merchant registered on EarthPort
            currency (string, optional): currency
            start_date_time (string, optional): startDateTime in
                yyyyy-MM-ddTHH:mm:ssZ
            end_date_time (string, optional): endDateTime in
                yyyyy-MM-ddTHH:mm:ssZ
            sort_order (SortOrderEnum, optional): Sort in either ascending or
                descending order
            offset (int, optional): This is used for pagination of resultsets.
                0-based starting offset of the page with respect to the entire
                resultset.
            page_size (int, optional): This is used for pagination of
                resultsets. Number of items per page to return. If empty the
                maximum allowable (25) number of records will be returned.

        Returns:
            Statement: Response from the API. Statement succesfully
                retrieved.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/statements'
        _query_parameters = {
            'managedMerchantName': managed_merchant_name,
            'currency': currency,
            'startDateTime': start_date_time,
            'endDateTime': end_date_time,
            'sortOrder': sort_order,
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
        return APIHelper.json_deserialize(_context.response.raw_body, Statement.from_dictionary)
