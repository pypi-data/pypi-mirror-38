# -*- coding: utf-8 -*-


class FinancialTransactionStatus(object):

    """Implementation of the 'FinancialTransactionStatus' model.

    Additional important status information for specific transaction types.

    Attributes:
        code (int): Numerical code of financial transaction status.
        description (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "code":'code',
        "description":'description'
    }

    def __init__(self,
                 code=None,
                 description=None):
        """Constructor for the FinancialTransactionStatus class"""

        # Initialize members of the class
        self.code = code
        self.description = description


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
        code = dictionary.get('code')
        description = dictionary.get('description')

        # Return an object of this model
        return cls(code,
                   description)


