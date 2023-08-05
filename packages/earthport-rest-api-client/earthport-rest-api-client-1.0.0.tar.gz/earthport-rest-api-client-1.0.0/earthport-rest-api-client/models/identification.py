# -*- coding: utf-8 -*-


class Identification(object):

    """Implementation of the 'Identification' model.

    This group consists of an individual identification type unique number and
    the country of origin of the identification. The idType will be a String
    value saying what the identification number relates to. This might be
    Passport. national ID card, driving licence or any other value. The idType
    will be validated against an enumeration to ensure it is of a valid type.
    Please refer to the "API Solution Guide" for further details. The
    identification number will normally be the equivalent of a passport
    number, but other types of identification can be used. The identification
    country will be the country that issued the identification number, so in
    the example that a passport number is provided as the identification
    number, the identification country will be the passport country origin.

    Attributes:
        id_type (string): Enumeration of ID Types such as 'Passport', 'Driving
            License', 'National ID Card'. Please refer to the Earthport "API
            Solution Guide".
        identification_country (string): Valid supported ISO 3166 2-character
            country code.
        identification_number (string): An identification number for an
            individual. For example, a passport number can be an
            identification number type. The length of this field is limited to
            50 bytes. 50 bytes can hold 50 normal English characters. This
            value will be truncated if it is too long.
        valid_from_date (string): Valid ISO 8601 date format YYYY-MM-DD.
        valid_to_date (string): Valid ISO 8601 date format YYYY-MM-DD.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "id_type":'idType',
        "identification_country":'identificationCountry',
        "identification_number":'identificationNumber',
        "valid_from_date":'validFromDate',
        "valid_to_date":'validToDate'
    }

    def __init__(self,
                 id_type=None,
                 identification_country=None,
                 identification_number=None,
                 valid_from_date=None,
                 valid_to_date=None):
        """Constructor for the Identification class"""

        # Initialize members of the class
        self.id_type = id_type
        self.identification_country = identification_country
        self.identification_number = identification_number
        self.valid_from_date = valid_from_date
        self.valid_to_date = valid_to_date


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
        id_type = dictionary.get('idType')
        identification_country = dictionary.get('identificationCountry')
        identification_number = dictionary.get('identificationNumber')
        valid_from_date = dictionary.get('validFromDate')
        valid_to_date = dictionary.get('validToDate')

        # Return an object of this model
        return cls(id_type,
                   identification_country,
                   identification_number,
                   valid_from_date,
                   valid_to_date)


