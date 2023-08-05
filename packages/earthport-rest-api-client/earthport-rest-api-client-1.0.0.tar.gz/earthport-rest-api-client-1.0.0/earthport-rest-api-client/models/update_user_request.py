# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.identity

class UpdateUserRequest(object):

    """Implementation of the 'UpdateUserRequest' model.

    A user Object.

    Attributes:
        payer_identity (Identity): Represents the identity of an individual or
            legal entity. You must specify one of either an individual
            identity or legal entity identity or unstructured identity.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "payer_identity":'payerIdentity'
    }

    def __init__(self,
                 payer_identity=None):
        """Constructor for the UpdateUserRequest class"""

        # Initialize members of the class
        self.payer_identity = payer_identity


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
        payer_identity = earthport-rest-api-client.models.identity.Identity.from_dictionary(dictionary.get('payerIdentity')) if dictionary.get('payerIdentity') else None

        # Return an object of this model
        return cls(payer_identity)


