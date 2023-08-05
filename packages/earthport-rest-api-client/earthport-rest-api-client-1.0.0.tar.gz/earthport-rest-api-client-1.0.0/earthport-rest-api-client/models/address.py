# -*- coding: utf-8 -*-


class Address(object):

    """Implementation of the 'Address' model.

    Represents an address. Mandatory attributes are 'addressLine1', 'city' and
    'country'. All other attributes are optional.

    Attributes:
        address_line_1 (string): A line of address information. The length of
            this field is limited to 254 bytes. This value will be truncated
            if it is too long.
        address_line_2 (string): A line of address information. The length of
            this field is limited to 254 bytes. This value will be truncated
            if it is too long.
        address_line_3 (string): A line of address information. The length of
            this field is limited to 254 bytes. This value will be truncated
            if it is too long.
        city (string): A line of address information. The length of this field
            is limited to 254 bytes. This value will be truncated if it is too
            long.
        country (string): Valid supported ISO 3166 2-character country code.
        postcode (string): A line of address information. The length of this
            field is limited to 10 bytes. 10 bytes can hold 10 normal English
            characters. This value will be truncated if it is too long.
        province (string): A line of address information. The length of this
            field is limited to 254 bytes. This value will be truncated if it
            is too long.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address_line1":'addressLine1',
        "city":'city',
        "country":'country',
        "address_line2":'addressLine2',
        "address_line3":'addressLine3',
        "postcode":'postcode',
        "province":'province'
    }

    def __init__(self,
                 address_line1=None,
                 city=None,
                 country=None,
                 address_line2=None,
                 address_line3=None,
                 postcode=None,
                 province=None):
        """Constructor for the Address class"""

        # Initialize members of the class
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_line3 = address_line3
        self.city = city
        self.country = country
        self.postcode = postcode
        self.province = province


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
        address_line1 = dictionary.get('addressLine1')
        city = dictionary.get('city')
        country = dictionary.get('country')
        address_line2 = dictionary.get('addressLine2')
        address_line3 = dictionary.get('addressLine3')
        postcode = dictionary.get('postcode')
        province = dictionary.get('province')

        # Return an object of this model
        return cls(address_line1,
                   city,
                   country,
                   address_line2,
                   address_line3,
                   postcode,
                   province)


