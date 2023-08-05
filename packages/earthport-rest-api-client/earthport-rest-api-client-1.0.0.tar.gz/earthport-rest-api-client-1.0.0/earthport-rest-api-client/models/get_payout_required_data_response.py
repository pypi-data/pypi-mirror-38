# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_bank_account_groups_list
import earthport-rest-api-client.models.beneficiary_identity_groups_list
import earthport-rest-api-client.models.purpose_of_payment_field_groups_list

class GetPayoutRequiredDataResponse(object):

    """Implementation of the 'GetPayoutRequiredDataResponse' model.

    All the data required to settle a payment with a given currency into a
    given country.

    Attributes:
        beneficiary_bank_account_field_groups_list
            (BeneficiaryBankAccountGroupsList): This type defines a list of
            bank account data groups. Each group is normally represented as a
            row on the UI.
        beneficiary_identity_field_groups_list
            (BeneficiaryIdentityGroupsList): This type defines a list of
            identity data groups. Each group is normally represented as a
            section of fields on the UI.
        purpose_of_payment_field_groups_list
            (PurposeOfPaymentFieldGroupsList): This group contains all
            configuration information for Purpose of Payment options. The
            'mandatory' attribute indicates whether provision of Purpose of
            Payment data is required for the Payout to be accepted.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "beneficiary_bank_account_field_groups_list":'beneficiaryBankAccountFieldGroupsList',
        "beneficiary_identity_field_groups_list":'beneficiaryIdentityFieldGroupsList',
        "purpose_of_payment_field_groups_list":'purposeOfPaymentFieldGroupsList'
    }

    def __init__(self,
                 beneficiary_bank_account_field_groups_list=None,
                 beneficiary_identity_field_groups_list=None,
                 purpose_of_payment_field_groups_list=None):
        """Constructor for the GetPayoutRequiredDataResponse class"""

        # Initialize members of the class
        self.beneficiary_bank_account_field_groups_list = beneficiary_bank_account_field_groups_list
        self.beneficiary_identity_field_groups_list = beneficiary_identity_field_groups_list
        self.purpose_of_payment_field_groups_list = purpose_of_payment_field_groups_list


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
        beneficiary_bank_account_field_groups_list = earthport-rest-api-client.models.beneficiary_bank_account_groups_list.BeneficiaryBankAccountGroupsList.from_dictionary(dictionary.get('beneficiaryBankAccountFieldGroupsList')) if dictionary.get('beneficiaryBankAccountFieldGroupsList') else None
        beneficiary_identity_field_groups_list = earthport-rest-api-client.models.beneficiary_identity_groups_list.BeneficiaryIdentityGroupsList.from_dictionary(dictionary.get('beneficiaryIdentityFieldGroupsList')) if dictionary.get('beneficiaryIdentityFieldGroupsList') else None
        purpose_of_payment_field_groups_list = earthport-rest-api-client.models.purpose_of_payment_field_groups_list.PurposeOfPaymentFieldGroupsList.from_dictionary(dictionary.get('purposeOfPaymentFieldGroupsList')) if dictionary.get('purposeOfPaymentFieldGroupsList') else None

        # Return an object of this model
        return cls(beneficiary_bank_account_field_groups_list,
                   beneficiary_identity_field_groups_list,
                   purpose_of_payment_field_groups_list)


