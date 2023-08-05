# -*- coding: utf-8 -*-


class BenBankID(object):

    """Implementation of the 'BenBankID' model.

    This group consists of all possible beneficiary bank identifier types. The
    'epBankID' field is a unique identifier for a beneficiary bank account.
    The 'merchantBankID' is an optional merchant specified identifier for the
    beneficiary bank account. The 'epBankID', 'merchantBankID' or both
    'epBankID' and 'merchantBankID' can be supplied. A mapping will be
    performed to retrieve the merchant bank ID from the supplied EP bank ID
    and vice versa. If both the 'epBankID' and 'merchantBankID' are supplied,
    a check will be performed to ensure that the two are mapped. If the two
    provided fields are not mapped, then a validation error code will be
    returned. At least one of the fields must be populated.

    Attributes:
        ep_bank_id (int): The unique ID of a beneficiary bank account.
        merchant_bank_id (string): The merchant specified ID for a beneficiary
            bank account.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "ep_bank_id":'epBankID',
        "merchant_bank_id":'merchantBankID'
    }

    def __init__(self,
                 ep_bank_id=None,
                 merchant_bank_id=None):
        """Constructor for the BenBankID class"""

        # Initialize members of the class
        self.ep_bank_id = ep_bank_id
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
        ep_bank_id = dictionary.get('epBankID')
        merchant_bank_id = dictionary.get('merchantBankID')

        # Return an object of this model
        return cls(ep_bank_id,
                   merchant_bank_id)


