# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.user_id
import earthport-rest-api-client.models.identity

class GetUserResponse(object):

    """Implementation of the 'Get UserResponse' model.

    A user Object.

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
        payer_identity (Identity): Represents the identity of an individual or
            legal entity. You must specify one of either an individual
            identity or legal entity identity or unstructured identity.
        created_date (string): Valid ISO 8601 date format YYYY-MM-DD.
        expired_date (string): Valid ISO 8601 date format YYYY-MM-DD.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "user_id":'userID',
        "payer_identity":'payerIdentity',
        "created_date":'createdDate',
        "expired_date":'expiredDate'
    }

    def __init__(self,
                 user_id=None,
                 payer_identity=None,
                 created_date=None,
                 expired_date=None):
        """Constructor for the GetUserResponse class"""

        # Initialize members of the class
        self.user_id = user_id
        self.payer_identity = payer_identity
        self.created_date = created_date
        self.expired_date = expired_date


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
        payer_identity = earthport-rest-api-client.models.identity.Identity.from_dictionary(dictionary.get('payerIdentity')) if dictionary.get('payerIdentity') else None
        created_date = dictionary.get('createdDate')
        expired_date = dictionary.get('expiredDate')

        # Return an object of this model
        return cls(user_id,
                   payer_identity,
                   created_date,
                   expired_date)


