# -*- coding: utf-8 -*-


class BenBankIDMerchant(object):

    """Implementation of the 'BenBankID_Merchant' model.

    This group consists of merchant beneficiary bank identifier only.

    Attributes:
        merchant_bank_id (string): The merchant specified ID for a beneficiary
            bank account.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "merchant_bank_id":'merchantBankID'
    }

    def __init__(self,
                 merchant_bank_id=None):
        """Constructor for the BenBankIDMerchant class"""

        # Initialize members of the class
        self.merchant_bank_id = merchant_bank_id


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
        merchant_bank_id = dictionary.get('merchantBankID')

        # Return an object of this model
        return cls(merchant_bank_id)


