# -*- coding: utf-8 -*-


class UserIDMerchant(object):

    """Implementation of the 'UserID_Merchant' model.

    This group consists of merchant user identifier only.

    Attributes:
        merchant_user_id (string): A unique reference for the merchant that
            identifies the person or company on behalf of which this account
            was set up. This needs to be used to reference KYC data held by
            the merchant (amongst other things). This is often a unique
            username or reference allocated by the merchant at user
            registration time.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "merchant_user_id":'merchantUserID'
    }

    def __init__(self,
                 merchant_user_id=None):
        """Constructor for the UserIDMerchant class"""

        # Initialize members of the class
        self.merchant_user_id = merchant_user_id


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
        merchant_user_id = dictionary.get('merchantUserID')

        # Return an object of this model
        return cls(merchant_user_id)


