# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_additional_data

class BeneficiaryAdditionalDataList(object):

    """Implementation of the 'BeneficiaryAdditionalDataList' model.

    Represents a list of Additional Data for Beneficiary Identity.

    Attributes:
        additional_data (list of BeneficiaryAdditionalData): TODO: type
            description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "additional_data":'additionalData'
    }

    def __init__(self,
                 additional_data=None):
        """Constructor for the BeneficiaryAdditionalDataList class"""

        # Initialize members of the class
        self.additional_data = additional_data


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
        additional_data = None
        if dictionary.get('additionalData') != None:
            additional_data = list()
            for structure in dictionary.get('additionalData'):
                additional_data.append(earthport-rest-api-client.models.beneficiary_additional_data.BeneficiaryAdditionalData.from_dictionary(structure))

        # Return an object of this model
        return cls(additional_data)


