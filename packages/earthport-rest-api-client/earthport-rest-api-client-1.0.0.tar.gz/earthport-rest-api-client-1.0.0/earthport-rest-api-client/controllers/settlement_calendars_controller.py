# -*- coding: utf-8 -*-

from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.custom_header_auth import CustomHeaderAuth
from ..models.get_settlement_calendar_response import GetSettlementCalendarResponse
from ..exceptions.api_exception import APIException

class SettlementCalendarsController(BaseController):

    """A Controller to access Endpoints in the earthport-rest-api-client API."""


    def get_settlement_calendar(self,
                                service_level=None,
                                beneficiary_country=None,
                                beneficiary_currency=None,
                                payout_request_currency=None,
                                number_of_calendar_days=None):
        """Does a GET request to /settlement-calendars.

        Retrieves the Settlement Calendar for payout.

        Args:
            service_level (string, optional): Service Level. Allowed values
                are standard and express.
            beneficiary_country (string, optional): Beneficiary Country.
            beneficiary_currency (string, optional): Beneficiary Currency.
            payout_request_currency (string, optional): Payout Request
                Currency.
            number_of_calendar_days (int, optional): Number of Calendar Days.

        Returns:
            GetSettlementCalendarResponse: Response from the API. Settlement
                Calendar retrieved.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _query_builder = Configuration.get_base_uri()
        _query_builder += '/settlement-calendars'
        _query_parameters = {
            'serviceLevel': service_level,
            'beneficiaryCountry': beneficiary_country,
            'beneficiaryCurrency': beneficiary_currency,
            'payoutRequestCurrency': payout_request_currency,
            'numberOfCalendarDays': number_of_calendar_days
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
        return APIHelper.json_deserialize(_context.response.raw_body, GetSettlementCalendarResponse.from_dictionary)
