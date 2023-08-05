# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.user
import earthport-rest-api-client.models.bank_account
import earthport-rest-api-client.models.payment

class CreatePaymentRequest(object):

    """Implementation of the 'CreatePaymentRequest' model.

    TODO: type model description here.

    Attributes:
        user (User): A user Object.
        bank_account (BankAccount): The beneficiary bank account Object.
        payment (Payment): Beneficiary Bank account payment.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "user":'user',
        "bank_account":'bankAccount',
        "payment":'payment'
    }

    def __init__(self,
                 user=None,
                 bank_account=None,
                 payment=None):
        """Constructor for the CreatePaymentRequest class"""

        # Initialize members of the class
        self.user = user
        self.bank_account = bank_account
        self.payment = payment


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
        user = earthport-rest-api-client.models.user.User.from_dictionary(dictionary.get('user')) if dictionary.get('user') else None
        bank_account = earthport-rest-api-client.models.bank_account.BankAccount.from_dictionary(dictionary.get('bankAccount')) if dictionary.get('bankAccount') else None
        payment = earthport-rest-api-client.models.payment.Payment.from_dictionary(dictionary.get('payment')) if dictionary.get('payment') else None

        # Return an object of this model
        return cls(user,
                   bank_account,
                   payment)


