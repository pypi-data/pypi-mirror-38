# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.monetary_value

class BeneficiaryAmountInformation(object):

    """Implementation of the 'BeneficiaryAmountInformation' model.

    Used to specify the beneficiary amount and the payout currency.

    Attributes:
        beneficiary_amount (MonetaryValue): Represents a monetary value
            containing a decimal amount value along with a currency code. The
            currency code is a three letter ISO 4217 code. E.g. GBP for
            British sterling pounds.
        payout_currency (string): Valid supported ISO 4217 3-character
            currency code.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "beneficiary_amount":'beneficiaryAmount',
        "payout_currency":'payoutCurrency'
    }

    def __init__(self,
                 beneficiary_amount=None,
                 payout_currency=None):
        """Constructor for the BeneficiaryAmountInformation class"""

        # Initialize members of the class
        self.beneficiary_amount = beneficiary_amount
        self.payout_currency = payout_currency


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
        beneficiary_amount = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('beneficiaryAmount')) if dictionary.get('beneficiaryAmount') else None
        payout_currency = dictionary.get('payoutCurrency')

        # Return an object of this model
        return cls(beneficiary_amount,
                   payout_currency)


