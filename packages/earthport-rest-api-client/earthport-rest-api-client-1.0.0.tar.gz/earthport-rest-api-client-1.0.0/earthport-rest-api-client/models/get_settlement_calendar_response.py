# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.settlement_calendar

class GetSettlementCalendarResponse(object):

    """Implementation of the 'Get Settlement CalendarResponse' model.

    Settlement Calendar.

    Attributes:
        response_time_stamp (string): TODO: type description here.
        settlement_calendar (list of SettlementCalendar): TODO: type
            description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "response_time_stamp":'responseTimeStamp',
        "settlement_calendar":'settlementCalendar'
    }

    def __init__(self,
                 response_time_stamp=None,
                 settlement_calendar=None):
        """Constructor for the GetSettlementCalendarResponse class"""

        # Initialize members of the class
        self.response_time_stamp = response_time_stamp
        self.settlement_calendar = settlement_calendar


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
        response_time_stamp = dictionary.get('responseTimeStamp')
        settlement_calendar = None
        if dictionary.get('settlementCalendar') != None:
            settlement_calendar = list()
            for structure in dictionary.get('settlementCalendar'):
                settlement_calendar.append(earthport-rest-api-client.models.settlement_calendar.SettlementCalendar.from_dictionary(structure))

        # Return an object of this model
        return cls(response_time_stamp,
                   settlement_calendar)


