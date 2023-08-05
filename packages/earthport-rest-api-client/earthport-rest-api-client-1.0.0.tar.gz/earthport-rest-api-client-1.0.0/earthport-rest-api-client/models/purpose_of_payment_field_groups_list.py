# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.purpose_of_payment_code

class PurposeOfPaymentFieldGroupsList(object):

    """Implementation of the 'purposeOfPaymentFieldGroupsList' model.

    This group contains all configuration information for Purpose of Payment
    options. The 'mandatory' attribute indicates whether provision of Purpose
    of Payment data is required for the Payout to be accepted.

    Attributes:
        mandatory (bool): TODO: type description here.
        purpose_of_payment_code (list of PurposeOfPaymentCode): TODO: type
            description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "mandatory":'mandatory',
        "purpose_of_payment_code":'purposeOfPaymentCode'
    }

    def __init__(self,
                 mandatory=None,
                 purpose_of_payment_code=None):
        """Constructor for the PurposeOfPaymentFieldGroupsList class"""

        # Initialize members of the class
        self.mandatory = mandatory
        self.purpose_of_payment_code = purpose_of_payment_code


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
        mandatory = dictionary.get('mandatory')
        purpose_of_payment_code = None
        if dictionary.get('purposeOfPaymentCode') != None:
            purpose_of_payment_code = list()
            for structure in dictionary.get('purposeOfPaymentCode'):
                purpose_of_payment_code.append(earthport-rest-api-client.models.purpose_of_payment_code.PurposeOfPaymentCode.from_dictionary(structure))

        # Return an object of this model
        return cls(mandatory,
                   purpose_of_payment_code)


