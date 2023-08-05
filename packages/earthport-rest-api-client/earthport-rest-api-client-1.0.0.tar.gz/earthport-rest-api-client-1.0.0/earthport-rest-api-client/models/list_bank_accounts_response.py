# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_bank_account_summary
import earthport-rest-api-client.models.user_id
import earthport-rest-api-client.models.pagination_result

class ListBankAccountsResponse(object):

    """Implementation of the 'List Bank AccountsResponse' model.

    This type gives a summary of the Beneficiary Bank Account.

    Attributes:
        beneficiary_bank_account_summary (list of
            BeneficiaryBankAccountSummary): TODO: type description here.
        user_id (UserID): This group consists of all possible user identifier
            types. The 'epUserID' field is a unique identifier for a merchant
            and is the equivalent of a Virtual Account Number (VAN). The
            'merchantUserID' is a merchant specified identifier for an
            individual or company that an account was set up for. The
            'epUserID', 'merchantUserID' or both 'epUserID' and
            'merchantUserID' can be supplied. A mapping will be performed to
            retrieve the merchant user ID from the supplied EP user ID and
            vice versa. If both the 'epUserID' and 'merchantUserID' are
            supplied, a check will be performed to ensure that the two are
            mapped. If the two provided fields are not mapped, then a
            validation error code will be returned. At least one of the fields
            must be populated.
        pagination_result (PaginationResult): This returns a paged set of
            results rather than the full result set.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "beneficiary_bank_account_summary":'beneficiaryBankAccountSummary',
        "user_id":'userID',
        "pagination_result":'paginationResult'
    }

    def __init__(self,
                 beneficiary_bank_account_summary=None,
                 user_id=None,
                 pagination_result=None):
        """Constructor for the ListBankAccountsResponse class"""

        # Initialize members of the class
        self.beneficiary_bank_account_summary = beneficiary_bank_account_summary
        self.user_id = user_id
        self.pagination_result = pagination_result


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
        beneficiary_bank_account_summary = None
        if dictionary.get('beneficiaryBankAccountSummary') != None:
            beneficiary_bank_account_summary = list()
            for structure in dictionary.get('beneficiaryBankAccountSummary'):
                beneficiary_bank_account_summary.append(earthport-rest-api-client.models.beneficiary_bank_account_summary.BeneficiaryBankAccountSummary.from_dictionary(structure))
        user_id = earthport-rest-api-client.models.user_id.UserID.from_dictionary(dictionary.get('userID')) if dictionary.get('userID') else None
        pagination_result = earthport-rest-api-client.models.pagination_result.PaginationResult.from_dictionary(dictionary.get('paginationResult')) if dictionary.get('paginationResult') else None

        # Return an object of this model
        return cls(beneficiary_bank_account_summary,
                   user_id,
                   pagination_result)


