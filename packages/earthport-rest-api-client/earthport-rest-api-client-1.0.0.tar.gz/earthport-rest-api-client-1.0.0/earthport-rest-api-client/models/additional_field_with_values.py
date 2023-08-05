# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.field_value

class AdditionalFieldWithValues(object):

    """Implementation of the 'additionalFieldWithValues' model.

    Key and label pairs indicate the accepted responses for an
    'additionalFieldWithValues' data field. They can be used to create a
    select list within a User Interface.

    Attributes:
        key (string): TODO: type description here.
        label (string): TODO: type description here.
        mandatory (bool): TODO: type description here.
        field_value (list of FieldValue): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "key":'key',
        "label":'label',
        "mandatory":'mandatory',
        "field_value":'fieldValue'
    }

    def __init__(self,
                 key=None,
                 label=None,
                 mandatory=None,
                 field_value=None):
        """Constructor for the AdditionalFieldWithValues class"""

        # Initialize members of the class
        self.key = key
        self.label = label
        self.mandatory = mandatory
        self.field_value = field_value


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
        key = dictionary.get('key')
        label = dictionary.get('label')
        mandatory = dictionary.get('mandatory')
        field_value = None
        if dictionary.get('fieldValue') != None:
            field_value = list()
            for structure in dictionary.get('fieldValue'):
                field_value.append(earthport-rest-api-client.models.field_value.FieldValue.from_dictionary(structure))

        # Return an object of this model
        return cls(key,
                   label,
                   mandatory,
                   field_value)


