# -*- coding: utf-8 -*-


class ValidateBeneficiaryBankAccountResponse(object):

    """Implementation of the 'Validate Beneficiary Bank AccountResponse' model.

    This is the response to the Validate Beneficiary Bank Account API.

    Attributes:
        is_bank_account_valid (bool): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "is_bank_account_valid":'isBankAccountValid'
    }

    def __init__(self,
                 is_bank_account_valid=None):
        """Constructor for the ValidateBeneficiaryBankAccountResponse class"""

        # Initialize members of the class
        self.is_bank_account_valid = is_bank_account_valid


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

        # Return an object of this model
        return cls(is_bank_account_valid)


