# -*- coding: utf-8 -*-


class IdentityRestriction(object):

    """Implementation of the 'identityRestriction' model.

    TODO: type model description here.

    Attributes:
        individual (bool): TODO: type description here.
        legal_entity (bool): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "individual":'individual',
        "legal_entity":'legalEntity'
    }

    def __init__(self,
                 individual=None,
                 legal_entity=None):
        """Constructor for the IdentityRestriction class"""

        # Initialize members of the class
        self.individual = individual
        self.legal_entity = legal_entity


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
        individual = dictionary.get('individual')
        legal_entity = dictionary.get('legalEntity')

        # Return an object of this model
        return cls(individual,
                   legal_entity)


