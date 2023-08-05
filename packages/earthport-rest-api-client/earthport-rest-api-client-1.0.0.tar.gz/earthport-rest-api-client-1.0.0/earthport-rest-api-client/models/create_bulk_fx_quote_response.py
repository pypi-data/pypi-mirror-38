# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.bulk_fx_detail

class CreateBulkFXQuoteResponse(object):

    """Implementation of the 'Create Bulk FX QuoteResponse' model.

    Bulk FX Quote Response.

    Attributes:
        fx_ticket_id (int): Generic entity identity.
        expiry_timestamp (string): TODO: type description here.
        bulk_fx_detail (list of BulkFXDetail): Represents the list of fxRates
            and their details.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "fx_ticket_id":'fxTicketID',
        "expiry_timestamp":'expiryTimestamp',
        "bulk_fx_detail":'bulkFXDetail'
    }

    def __init__(self,
                 fx_ticket_id=None,
                 expiry_timestamp=None,
                 bulk_fx_detail=None):
        """Constructor for the CreateBulkFXQuoteResponse class"""

        # Initialize members of the class
        self.fx_ticket_id = fx_ticket_id
        self.expiry_timestamp = expiry_timestamp
        self.bulk_fx_detail = bulk_fx_detail


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
        expiry_timestamp = dictionary.get('expiryTimestamp')
        bulk_fx_detail = None
        if dictionary.get('bulkFXDetail') != None:
            bulk_fx_detail = list()
            for structure in dictionary.get('bulkFXDetail'):
                bulk_fx_detail.append(earthport-rest-api-client.models.bulk_fx_detail.BulkFXDetail.from_dictionary(structure))

        # Return an object of this model
        return cls(fx_ticket_id,
                   expiry_timestamp,
                   bulk_fx_detail)


