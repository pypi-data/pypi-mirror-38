# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.individual_name
import earthport-rest-api-client.models.address
import earthport-rest-api-client.models.birth_information
import earthport-rest-api-client.models.identification

class IndividualIdentity(object):

    """Implementation of the 'IndividualIdentity' model.

    The identity of an individual. The 'name' attribute is mandatory for an
    individual. You must supply at least identification entry or one birth
    information entry or one address entry.

    Attributes:
        name (IndividualName): The 'givenNames' attribute is mandatory. This
            is a space separated list of names (not including the family
            name).   You should supply names and not initials (wherever
            possible). See examples below.   The 'familyName' attribute is
            mandatory. This contains the single family name. See examples
            below.    *Example1 - a western citizen from a country which uses
            the common western naming convention(such as US, GB, FR, CA, DE
            etc...)*        Name = "John Michael Smith",        
            givenNames="John Michael" and familyName="Smith"   *Example2 - a
            citizen from a country which uses the eastern name order where the
            family name comes first, followed by their given names (such as
            Hungary, China, Japan, Korea, Singapore, Taiwan, Vietnam etc...)* 
            Name = "Máo Zédÿng",         giveNames="Zédÿng" and
            familyName="Máo"        Name = "Hidetoshi Nakata",        
            givenNames="Nakata" and familyName="Hidetoshi"       Name =
            "Ferenc Puskás",         giveNames="Puskás" and
            familyName="Ferenc"   *Example3 - middle east names*         Name=
            "Mohammed bin Rashid bin Saeed Al-Maktoum",        
            givenNames="Mohammed bin Rashid bin Saeed" and
            familName="Al-Maktoum"   *Example4 - single names, such as in
            Indonesia*         Name="Suharto",         givenNames="Suharto"
            and familyName="Suharto".
        address (Address): Represents an address. Mandatory attributes are
            'addressLine1', 'city' and 'country'. All other attributes are
            optional.
        birth_information (BirthInformation): The group consists of elements
            that define birth information for an individual.
        identification (list of Identification): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "name":'name',
        "address":'address',
        "birth_information":'birthInformation',
        "identification":'identification'
    }

    def __init__(self,
                 name=None,
                 address=None,
                 birth_information=None,
                 identification=None):
        """Constructor for the IndividualIdentity class"""

        # Initialize members of the class
        self.name = name
        self.address = address
        self.birth_information = birth_information
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
        name = earthport-rest-api-client.models.individual_name.IndividualName.from_dictionary(dictionary.get('name')) if dictionary.get('name') else None
        address = earthport-rest-api-client.models.address.Address.from_dictionary(dictionary.get('address')) if dictionary.get('address') else None
        birth_information = earthport-rest-api-client.models.birth_information.BirthInformation.from_dictionary(dictionary.get('birthInformation')) if dictionary.get('birthInformation') else None
        identification = None
        if dictionary.get('identification') != None:
            identification = list()
            for structure in dictionary.get('identification'):
                identification.append(earthport-rest-api-client.models.identification.Identification.from_dictionary(structure))

        # Return an object of this model
        return cls(name,
                   address,
                   birth_information,
                   identification)


