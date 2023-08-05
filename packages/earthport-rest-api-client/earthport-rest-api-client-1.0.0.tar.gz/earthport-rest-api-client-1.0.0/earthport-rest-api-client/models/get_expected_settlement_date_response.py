# -*- coding: utf-8 -*-


class GetExpectedSettlementDateResponse(object):

    """Implementation of the 'Get Expected Settlement DateResponse' model.

    This is the response to the Validate Beneficiary Bank Account API.

    Attributes:
        is_bank_account_valid (bool): TODO: type description here.
        anticipated_payout_request_time (string): TODO: type description
            here.
        service_level (ServiceLevelEnum): Supported service levels for a
            payout request (standard or express).
        expected_settlement_date (string): Valid ISO 8601 date format
            YYYY-MM-DD.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "is_bank_account_valid":'isBankAccountValid',
        "anticipated_payout_request_time":'anticipatedPayoutRequestTime',
        "service_level":'serviceLevel',
        "expected_settlement_date":'expectedSettlementDate'
    }

    def __init__(self,
                 is_bank_account_valid=None,
                 anticipated_payout_request_time=None,
                 service_level=None,
                 expected_settlement_date=None):
        """Constructor for the GetExpectedSettlementDateResponse class"""

        # Initialize members of the class
        self.is_bank_account_valid = is_bank_account_valid
        self.anticipated_payout_request_time = anticipated_payout_request_time
        self.service_level = service_level
        self.expected_settlement_date = expected_settlement_date


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
        is_bank_account_valid = dictionary.get('isBankAccountValid')
        anticipated_payout_request_time = dictionary.get('anticipatedPayoutRequestTime')
        service_level = dictionary.get('serviceLevel')
        expected_settlement_date = dictionary.get('expectedSettlementDate')

        # Return an object of this model
        return cls(is_bank_account_valid,
                   anticipated_payout_request_time,
                   service_level,
                   expected_settlement_date)


