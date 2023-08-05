# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.individual_identity
import earthport-rest-api-client.models.legal_entity_identity
import earthport-rest-api-client.models.unstructured_identity
import earthport-rest-api-client.models.additional_data

class Identity(object):

    """Implementation of the 'Identity' model.

    Represents the identity of an individual or legal entity. You must specify
    one of either an individual identity or legal entity identity or
    unstructured identity.

    Attributes:
        individual_identity (IndividualIdentity): The identity of an
            individual. The 'name' attribute is mandatory for an individual.
            You must supply at least identification entry or one birth
            information entry or one address entry.
        legal_entity_identity (LegalEntityIdentity): The identity of a legal
            entity. The 'legalEntityName' is mandatory. You must supply one of
            'legalEntityRegistration' or 'address'.
        unstructured_identity (list of UnstructuredIdentity): TODO: type
            description here.
        additional_data (list of AdditionalData): TODO: type description
            here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "individual_identity":'individualIdentity',
        "legal_entity_identity":'legalEntityIdentity',
        "unstructured_identity":'unstructuredIdentity',
        "additional_data":'additionalData'
    }

    def __init__(self,
                 individual_identity=None,
                 legal_entity_identity=None,
                 unstructured_identity=None,
                 additional_data=None):
        """Constructor for the Identity class"""

        # Initialize members of the class
        self.individual_identity = individual_identity
        self.legal_entity_identity = legal_entity_identity
        self.unstructured_identity = unstructured_identity
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
        individual_identity = earthport-rest-api-client.models.individual_identity.IndividualIdentity.from_dictionary(dictionary.get('individualIdentity')) if dictionary.get('individualIdentity') else None
        legal_entity_identity = earthport-rest-api-client.models.legal_entity_identity.LegalEntityIdentity.from_dictionary(dictionary.get('legalEntityIdentity')) if dictionary.get('legalEntityIdentity') else None
        unstructured_identity = None
        if dictionary.get('unstructuredIdentity') != None:
            unstructured_identity = list()
            for structure in dictionary.get('unstructuredIdentity'):
                unstructured_identity.append(earthport-rest-api-client.models.unstructured_identity.UnstructuredIdentity.from_dictionary(structure))
        additional_data = None
        if dictionary.get('additionalData') != None:
            additional_data = list()
            for structure in dictionary.get('additionalData'):
                additional_data.append(earthport-rest-api-client.models.additional_data.AdditionalData.from_dictionary(structure))

        # Return an object of this model
        return cls(individual_identity,
                   legal_entity_identity,
                   unstructured_identity,
                   additional_data)


