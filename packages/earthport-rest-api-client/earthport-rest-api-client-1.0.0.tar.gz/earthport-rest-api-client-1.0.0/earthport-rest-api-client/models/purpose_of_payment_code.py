# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.purpose_of_payment_usage_restrictions

class PurposeOfPaymentCode(object):

    """Implementation of the 'purposeOfPaymentCode' model.

    This contains a specific Purpose of Payment option, consisting of a code
    and a human readable description.

    Attributes:
        code (string): TODO: type description here.
        description (string): TODO: type description here.
        purpose_of_payment_usage_restrictions
            (PurposeOfPaymentUsageRestrictions): Usage restrictions apply
            where a specified code is only acceptable for a given type of
            payer or beneficiary. This attribute indicates whether the code
            can be used for Individuals and/or Legal Entities, for both payer
            and beneficiary parties. Additional field specifications identify
            further data that is required, given the chosen Purpose of
            Payment.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "code":'code',
        "description":'description',
        "purpose_of_payment_usage_restrictions":'purposeOfPaymentUsageRestrictions'
    }

    def __init__(self,
                 code=None,
                 description=None,
                 purpose_of_payment_usage_restrictions=None):
        """Constructor for the PurposeOfPaymentCode class"""

        # Initialize members of the class
        self.code = code
        self.description = description
        self.purpose_of_payment_usage_restrictions = purpose_of_payment_usage_restrictions


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
        code = dictionary.get('code')
        description = dictionary.get('description')
        purpose_of_payment_usage_restrictions = earthport-rest-api-client.models.purpose_of_payment_usage_restrictions.PurposeOfPaymentUsageRestrictions.from_dictionary(dictionary.get('purposeOfPaymentUsageRestrictions')) if dictionary.get('purposeOfPaymentUsageRestrictions') else None

        # Return an object of this model
        return cls(code,
                   description,
                   purpose_of_payment_usage_restrictions)


