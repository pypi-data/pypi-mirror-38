# -*- coding: utf-8 -*-


class SettlementCalendar(object):

    """Implementation of the 'SettlementCalendar' model.

    TODO: type model description here.

    Attributes:
        submit_by (string): TODO: type description here.
        for_value_on (string): Valid ISO 8601 date format YYYY-MM-DD.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "submit_by":'submitBy',
        "for_value_on":'forValueOn'
    }

    def __init__(self,
                 submit_by=None,
                 for_value_on=None):
        """Constructor for the SettlementCalendar class"""

        # Initialize members of the class
        self.submit_by = submit_by
        self.for_value_on = for_value_on


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
        submit_by = dictionary.get('submitBy')
        for_value_on = dictionary.get('forValueOn')

        # Return an object of this model
        return cls(submit_by,
                   for_value_on)


