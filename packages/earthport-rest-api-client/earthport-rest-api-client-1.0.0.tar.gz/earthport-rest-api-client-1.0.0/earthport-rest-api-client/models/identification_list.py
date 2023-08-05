# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.identification

class IdentificationList(object):

    """Implementation of the 'IdentificationList' model.

    Represents a list of Identityfication objects.

    Attributes:
        identification (list of Identification): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "identification":'identification'
    }

    def __init__(self,
                 identification=None):
        """Constructor for the IdentificationList class"""

        # Initialize members of the class
        self.identification = identification


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
        identification = None
        if dictionary.get('identification') != None:
            identification = list()
            for structure in dictionary.get('identification'):
                identification.append(earthport-rest-api-client.models.identification.Identification.from_dictionary(structure))

        # Return an object of this model
        return cls(identification)


