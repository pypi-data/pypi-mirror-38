# -*- coding: utf-8 -*-


class BankAccountDetails(object):

    """Implementation of the 'BankAccountDetails' model.

    This group holds all possible account identifier types - listed below in
    alphabetical order. The data which should be supplied in this group
    differs depending on the bank account territory. Please refer to the
    integration guide for territory specific details of what should be
    supplied. The following set of parameter names are valid keys:-
    abaRoutingNumber, accountName, accountNumber, accountNumberPrefix,
    accountNumberSuffix, accountType, bankCode, bankName, branchCode, bic,
    holdingBranchName, iban, miscField1, miscField2, miscField3, sortCode,
    swiftBic.

    Attributes:
        key (string): Type which defines the allowable data which may be
            passed to the "key" element of the BankAccountDetails.
        value (string): Type which defines the allowable data which may be
            passed to the "value" element of the BankAccountDetails.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "key":'key',
        "value":'value'
    }

    def __init__(self,
                 key=None,
                 value=None):
        """Constructor for the BankAccountDetails class"""

        # Initialize members of the class
        self.key = key
        self.value = value


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
        key = dictionary.get('key')
        value = dictionary.get('value')

        # Return an object of this model
        return cls(key,
                   value)


