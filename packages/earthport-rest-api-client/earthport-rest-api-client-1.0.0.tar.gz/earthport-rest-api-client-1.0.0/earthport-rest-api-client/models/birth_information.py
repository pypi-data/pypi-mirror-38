# -*- coding: utf-8 -*-


class BirthInformation(object):

    """Implementation of the 'BirthInformation' model.

    The group consists of elements that define birth information for an
    individual.

    Attributes:
        city_of_birth (string): A line of address information. The length of
            this field is limited to 254 bytes. This value will be truncated
            if it is too long.
        country_of_birth (string): Valid supported ISO 3166 2-character
            country code.
        date_of_birth (string): Valid ISO 8601 date format YYYY-MM-DD.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "country_of_birth":'countryOfBirth',
        "date_of_birth":'dateOfBirth',
        "city_of_birth":'cityOfBirth'
    }

    def __init__(self,
                 country_of_birth=None,
                 date_of_birth=None,
                 city_of_birth=None):
        """Constructor for the BirthInformation class"""

        # Initialize members of the class
        self.city_of_birth = city_of_birth
        self.country_of_birth = country_of_birth
        self.date_of_birth = date_of_birth


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
        country_of_birth = dictionary.get('countryOfBirth')
        date_of_birth = dictionary.get('dateOfBirth')
        city_of_birth = dictionary.get('cityOfBirth')

        # Return an object of this model
        return cls(country_of_birth,
                   date_of_birth,
                   city_of_birth)


