# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.legal_entity_registration
import earthport-rest-api-client.models.address

class LegalEntityIdentity(object):

    """Implementation of the 'LegalEntityIdentity' model.

    The identity of a legal entity. The 'legalEntityName' is mandatory. You
    must supply one of 'legalEntityRegistration' or 'address'.

    Attributes:
        legal_entity_name (string): The name component of the legal entity.
            The length of this field is limited to 1024 bytes. 1024 bytes can
            hold 1024 normal English characters.
        legal_entity_registration (LegalEntityRegistration): This group
            consists of a legal entity registration number type and the
            country that the legal entity is registered in. Legal Entity
            Registration Number is mandatory Legal Entity Registration Country
            is mandatory Legal Entity Registration Province is optional.
        address (Address): Represents an address. Mandatory attributes are
            'addressLine1', 'city' and 'country'. All other attributes are
            optional.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "legal_entity_name":'legalEntityName',
        "legal_entity_registration":'legalEntityRegistration',
        "address":'address'
    }

    def __init__(self,
                 legal_entity_name=None,
                 legal_entity_registration=None,
                 address=None):
        """Constructor for the LegalEntityIdentity class"""

        # Initialize members of the class
        self.legal_entity_name = legal_entity_name
        self.legal_entity_registration = legal_entity_registration
        self.address = address


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
        legal_entity_name = dictionary.get('legalEntityName')
        legal_entity_registration = earthport-rest-api-client.models.legal_entity_registration.LegalEntityRegistration.from_dictionary(dictionary.get('legalEntityRegistration')) if dictionary.get('legalEntityRegistration') else None
        address = earthport-rest-api-client.models.address.Address.from_dictionary(dictionary.get('address')) if dictionary.get('address') else None

        # Return an object of this model
        return cls(legal_entity_name,
                   legal_entity_registration,
                   address)


