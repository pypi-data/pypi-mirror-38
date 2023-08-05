# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.fx_detail

class CreateFXQuoteResponse(object):

    """Implementation of the 'Create FX QuoteResponse' model.

    TODO: type model description here.

    Attributes:
        fx_ticket_id (int): Generic entity identity.
        fx_detail (FXDetail): Represents the details of an FX transaction,
            encapsulating the sellAmount, buyAmount and fxRate into a single
            type.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "fx_ticket_id":'fxTicketID',
        "fx_detail":'fxDetail'
    }

    def __init__(self,
                 fx_ticket_id=None,
                 fx_detail=None):
        """Constructor for the CreateFXQuoteResponse class"""

        # Initialize members of the class
        self.fx_ticket_id = fx_ticket_id
        self.fx_detail = fx_detail


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
        fx_ticket_id = dictionary.get('fxTicketID')
        fx_detail = earthport-rest-api-client.models.fx_detail.FXDetail.from_dictionary(dictionary.get('fxDetail')) if dictionary.get('fxDetail') else None

        # Return an object of this model
        return cls(fx_ticket_id,
                   fx_detail)


