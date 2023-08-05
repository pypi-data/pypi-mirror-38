# -*- coding: utf-8 -*-


class TransactionIDMerchant(object):

    """Implementation of the 'TransactionID_Merchant' model.

    This group consists of merchant transaction reference only.

    Attributes:
        merchant_transaction_id (string): The unique reference of a
            transaction provided by the merchant.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "merchant_transaction_id":'merchantTransactionID'
    }

    def __init__(self,
                 merchant_transaction_id=None):
        """Constructor for the TransactionIDMerchant class"""

        # Initialize members of the class
        self.merchant_transaction_id = merchant_transaction_id


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
        merchant_transaction_id = dictionary.get('merchantTransactionID')

        # Return an object of this model
        return cls(merchant_transaction_id)


