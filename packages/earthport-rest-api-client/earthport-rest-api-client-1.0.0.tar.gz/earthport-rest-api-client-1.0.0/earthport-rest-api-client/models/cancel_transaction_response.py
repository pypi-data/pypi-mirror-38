# -*- coding: utf-8 -*-


class CancelTransactionResponse(object):

    """Implementation of the 'Cancel TransactionResponse' model.

    Transaction Cancellation Response.

    Attributes:
        status (string): TODO: type description here.
        status_description (string): TODO: type description here.
        timestamp (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "status":'status',
        "status_description":'statusDescription',
        "timestamp":'timestamp'
    }

    def __init__(self,
                 status=None,
                 status_description=None,
                 timestamp=None):
        """Constructor for the CancelTransactionResponse class"""

        # Initialize members of the class
        self.status = status
        self.status_description = status_description
        self.timestamp = timestamp


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
        status = dictionary.get('status')
        status_description = dictionary.get('statusDescription')
        timestamp = dictionary.get('timestamp')

        # Return an object of this model
        return cls(status,
                   status_description,
                   timestamp)


