# -*- coding: utf-8 -*-


class IndividualName(object):

    """Implementation of the 'IndividualName' model.

    The 'givenNames' attribute is mandatory. This is a space separated list of
    names (not including the family name). 
    You should supply names and not initials (wherever possible). See examples
    below. 
    The 'familyName' attribute is mandatory. This contains the single family
    name. See examples below. 
    *Example1 - a western citizen from a country which uses the common western
    naming convention(such as US, GB, FR, CA, DE etc...)*
      
        Name = "John Michael Smith", 
      
        givenNames="John Michael" and familyName="Smith"
    *Example2 - a citizen from a country which uses the eastern name order
    where the family name comes first, followed by their given names (such as
    Hungary, China, Japan, Korea, Singapore, Taiwan, Vietnam etc...)* 
        Name = "Máo Zédÿng", 
      
        giveNames="Zédÿng" and familyName="Máo" 
        Name = "Hidetoshi Nakata", 
      
        givenNames="Nakata" and familyName="Hidetoshi"
        Name = "Ferenc Puskás", 
      
        giveNames="Puskás" and familyName="Ferenc"
    *Example3 - middle east names* 
      
        Name= "Mohammed bin Rashid bin Saeed Al-Maktoum", 
      
        givenNames="Mohammed bin Rashid bin Saeed" and familName="Al-Maktoum"
    *Example4 - single names, such as in Indonesia* 
      
        Name="Suharto", 
      
        givenNames="Suharto" and familyName="Suharto".

    Attributes:
        family_name (string): The family name component of an individual's
            identity. The length of this field is limited to 1024 bytes. 1024
            bytes can hold 1024 normal English characters.
        given_names (string): The given names component of an individual's
            identity. For detailed examples see documentation for type
            IndividualName. The length of this field is limited to 1024 bytes.
            1024 bytes can hold 1024 normal English characters.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "family_name":'familyName',
        "given_names":'givenNames'
    }

    def __init__(self,
                 family_name=None,
                 given_names=None):
        """Constructor for the IndividualName class"""

        # Initialize members of the class
        self.family_name = family_name
        self.given_names = given_names


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
        family_name = dictionary.get('familyName')
        given_names = dictionary.get('givenNames')

        # Return an object of this model
        return cls(family_name,
                   given_names)


