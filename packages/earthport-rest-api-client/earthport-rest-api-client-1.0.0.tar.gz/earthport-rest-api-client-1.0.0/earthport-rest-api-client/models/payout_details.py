# -*- coding: utf-8 -*-


class PayoutDetails(object):

    """Implementation of the 'PayoutDetails' model.

    Allows additional data to be supplied with a payout Refer to documentation
    for valid keys.

    Attributes:
        key (string): Type which defines the allowable data which may be
            passed to the "key" element of the PayoutDetails.
        value (string): Type which defines the allowable data which may be
            passed to the "value" element of the PayoutDetails.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "key":'key',
        "value":'value'
    }

    def __init__(self,
                 key=None,
                 value=None):
        """Constructor for the PayoutDetails class"""

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


