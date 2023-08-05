# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.user_id
import earthport-rest-api-client.models.ben_bank_id

class UsersBankID(object):

    """Implementation of the 'UsersBankID' model.

    This group consists of a collection of both the user ID group and
    beneficiary bank ID group. The 'userID' is a collection of user identifier
    types. The 'benBankID' is a collection of account identifier types. Both
    the 'userID' and 'benBankID' fields are mandatory.

    Attributes:
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
        ben_bank_id (BenBankID): This group consists of all possible
            beneficiary bank identifier types. The 'epBankID' field is a
            unique identifier for a beneficiary bank account. The
            'merchantBankID' is an optional merchant specified identifier for
            the beneficiary bank account. The 'epBankID', 'merchantBankID' or
            both 'epBankID' and 'merchantBankID' can be supplied. A mapping
            will be performed to retrieve the merchant bank ID from the
            supplied EP bank ID and vice versa. If both the 'epBankID' and
            'merchantBankID' are supplied, a check will be performed to ensure
            that the two are mapped. If the two provided fields are not
            mapped, then a validation error code will be returned. At least
            one of the fields must be populated.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "user_id":'userID',
        "ben_bank_id":'benBankID'
    }

    def __init__(self,
                 user_id=None,
                 ben_bank_id=None):
        """Constructor for the UsersBankID class"""

        # Initialize members of the class
        self.user_id = user_id
        self.ben_bank_id = ben_bank_id


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
        user_id = earthport-rest-api-client.models.user_id.UserID.from_dictionary(dictionary.get('userID')) if dictionary.get('userID') else None
        ben_bank_id = earthport-rest-api-client.models.ben_bank_id.BenBankID.from_dictionary(dictionary.get('benBankID')) if dictionary.get('benBankID') else None

        # Return an object of this model
        return cls(user_id,
                   ben_bank_id)


