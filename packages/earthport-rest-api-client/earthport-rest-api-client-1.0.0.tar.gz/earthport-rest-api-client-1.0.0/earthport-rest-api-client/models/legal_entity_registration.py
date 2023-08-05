# -*- coding: utf-8 -*-


class LegalEntityRegistration(object):

    """Implementation of the 'LegalEntityRegistration' model.

    This group consists of a legal entity registration number type and the
    country that the legal entity is registered in. Legal Entity Registration
    Number is mandatory Legal Entity Registration Country is mandatory Legal
    Entity Registration Province is optional.

    Attributes:
        legal_entity_registration_country (string): Valid supported ISO 3166
            2-character country code.
        legal_entity_registration_number (string): The registration number
            component of the legal entity. The length of this field is limited
            to 254 bytes. 254 bytes can hold 254 normal English characters.
            This value will be truncated if it is too long.
        legal_entity_registration_province (string): Optional province of the
            legal entity's address.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "legal_entity_registration_country":'legalEntityRegistrationCountry',
        "legal_entity_registration_number":'legalEntityRegistrationNumber',
        "legal_entity_registration_province":'legalEntityRegistrationProvince'
    }

    def __init__(self,
                 legal_entity_registration_country=None,
                 legal_entity_registration_number=None,
                 legal_entity_registration_province=None):
        """Constructor for the LegalEntityRegistration class"""

        # Initialize members of the class
        self.legal_entity_registration_country = legal_entity_registration_country
        self.legal_entity_registration_number = legal_entity_registration_number
        self.legal_entity_registration_province = legal_entity_registration_province


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
        legal_entity_registration_country = dictionary.get('legalEntityRegistrationCountry')
        legal_entity_registration_number = dictionary.get('legalEntityRegistrationNumber')
        legal_entity_registration_province = dictionary.get('legalEntityRegistrationProvince')

        # Return an object of this model
        return cls(legal_entity_registration_country,
                   legal_entity_registration_number,
                   legal_entity_registration_province)


