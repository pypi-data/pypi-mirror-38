# -*- coding: utf-8 -*-


class AdditionalFieldWithValidator(object):

    """Implementation of the 'additionalFieldWithValidator' model.

    The 'Validation' attribute may contain a Regular Expression, which should
    be used to validate data before submission.

    Attributes:
        key (string): TODO: type description here.
        label (string): TODO: type description here.
        mandatory (bool): TODO: type description here.
        validation (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "key":'key',
        "label":'label',
        "mandatory":'mandatory',
        "validation":'validation'
    }

    def __init__(self,
                 key=None,
                 label=None,
                 mandatory=None,
                 validation=None):
        """Constructor for the AdditionalFieldWithValidator class"""

        # Initialize members of the class
        self.key = key
        self.label = label
        self.mandatory = mandatory
        self.validation = validation


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
        validation = dictionary.get('validation')

        # Return an object of this model
        return cls(key,
                   label,
                   mandatory,
                   validation)


