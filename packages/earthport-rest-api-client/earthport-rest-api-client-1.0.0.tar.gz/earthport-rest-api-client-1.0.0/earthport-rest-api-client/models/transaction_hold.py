# -*- coding: utf-8 -*-


class TransactionHold(object):

    """Implementation of the 'TransactionHold' model.

    Parameter to prevent transactions from being processed until the desired
    time has been reached Note releaseDateTime must be in UTC format.

    Attributes:
        offset_minutes (int): TODO: type description here.
        release_date_time (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "offset_minutes":'offsetMinutes',
        "release_date_time":'releaseDateTime'
    }

    def __init__(self,
                 offset_minutes=None,
                 release_date_time=None):
        """Constructor for the TransactionHold class"""

        # Initialize members of the class
        self.offset_minutes = offset_minutes
        self.release_date_time = release_date_time


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
        offset_minutes = dictionary.get('offsetMinutes')
        release_date_time = dictionary.get('releaseDateTime')

        # Return an object of this model
        return cls(offset_minutes,
                   release_date_time)


