# -*- coding: utf-8 -*-


class AdditionalData(object):

    """Implementation of the 'AdditionalData' model.

    Represents a set of name value pairs that can be supplied with the
    Identity information. The keys will be validated on the server side
    against a list of valid types that are accepted. See the "API Solution
    Guide" for further details. Both the key and the value are required if
    adding additional data. The length of the additionalDataKey field is
    currently restricted to 50 bytes and will be truncated if the value is too
    long. The length of the additionalDataValue field is currently restricted
    to 254 bytes and will be truncated if the value is too long.

    Attributes:
        key (string): TODO: type description here.
        value (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "key":'Key',
        "value":'Value'
    }

    def __init__(self,
                 key=None,
                 value=None):
        """Constructor for the AdditionalData class"""

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
        key = dictionary.get('Key')
        value = dictionary.get('Value')

        # Return an object of this model
        return cls(key,
                   value)


