# -*- coding: utf-8 -*-


class GetPayoutRequiredDataForCountryCurrency(object):

    """Implementation of the 'getPayoutRequiredDataForCountryCurrency' model.

    TODO: type model description here.

    Attributes:
        beneficiary_identity_entity (IdentityEntityEnum): Supported identity
            entity types.
        country_code (string): Valid supported ISO 3166 2-character country
            code.
        currency_code (string): Valid supported ISO 4217 3-character currency
            code.
        locale (string): Supports a comma separated list of locales. for
            example en_GB, en_US in order of preferred locale.
        service_level (ServiceLevelEnum): Supported service levels for a
            payout request (standard or express).

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "country_code":'countryCode',
        "currency_code":'currencyCode',
        "beneficiary_identity_entity":'beneficiaryIdentityEntity',
        "locale":'locale',
        "service_level":'serviceLevel'
    }

    def __init__(self,
                 country_code=None,
                 currency_code=None,
                 beneficiary_identity_entity=None,
                 locale=None,
                 service_level=None):
        """Constructor for the GetPayoutRequiredDataForCountryCurrency class"""

        # Initialize members of the class
        self.beneficiary_identity_entity = beneficiary_identity_entity
        self.country_code = country_code
        self.currency_code = currency_code
        self.locale = locale
        self.service_level = service_level


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
        country_code = dictionary.get('countryCode')
        currency_code = dictionary.get('currencyCode')
        beneficiary_identity_entity = dictionary.get('beneficiaryIdentityEntity')
        locale = dictionary.get('locale')
        service_level = dictionary.get('serviceLevel')

        # Return an object of this model
        return cls(country_code,
                   currency_code,
                   beneficiary_identity_entity,
                   locale,
                   service_level)


