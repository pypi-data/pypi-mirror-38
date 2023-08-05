# -*- coding: utf-8 -*-


class AddDepositReferenceRequest(object):

    """Implementation of the 'AddDepositReferenceRequest' model.

    Deposit Reference.

    Attributes:
        deposit_reference (string): A Merchant User Deposit Reference.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "deposit_reference":'depositReference'
    }

    def __init__(self,
                 deposit_reference=None):
        """Constructor for the AddDepositReferenceRequest class"""

        # Initialize members of the class
        self.deposit_reference = deposit_reference


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
        deposit_reference = dictionary.get('depositReference')

        # Return an object of this model
        return cls(deposit_reference)


