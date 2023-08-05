# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.transaction_id_merchant
import earthport-rest-api-client.models.monetary_value
import earthport-rest-api-client.models.beneficiary_amount_information
import earthport-rest-api-client.models.payout_details
import earthport-rest-api-client.models.transaction_hold

class PaymentRegisteredBeneficiaryRequest(object):

    """Implementation of the 'PaymentRegisteredBeneficiaryRequest' model.

    Beneficiary Bank account payment

    Attributes:
        transaction_id (TransactionIDMerchant): This group consists of
            merchant transaction reference only.
        payout_request_amount (MonetaryValue): Represents a monetary value
            containing a decimal amount value along with a currency code. The
            currency code is a three letter ISO 4217 code. E.g. GBP for
            British sterling pounds.
        beneficiary_amount_information (BeneficiaryAmountInformation): Used to
            specify the beneficiary amount and the payout currency.
        service_level (ServiceLevelEnum): Supported service levels for a
            payout request (standard or express).
        beneficiary_statement_narrative (string): Generic description field.
        fx_ticket_id (int): Generic entity identity.
        requested_fx (RequestedFXEnum): Method of FX that is requested by the
            merchant and for which EPS2 will attempt to use in order to settle
            the payout request. FF (Fixed to Fixed) is where no FX will be
            performed as payout and beneficiary currencies are the same. FV
            (Fixed to Variable) uses the supplied payout request amount in
            order to determine the beneficiary amount. VF (Variable to Fixed)
            uses the supplied beneficiary amount in order to determine the
            payout amount.
        payer_type (PayerTypeEnum): The type of Payer making the payment. This
            detrmines which identity details are used as the payer identity.
        payout_type (string): Reserved for future use. Will be used to state
            the Payout type.
        payout_details (list of PayoutDetails): TODO: type description here.
        transaction_hold (TransactionHold): Parameter to prevent transactions
            from being processed until the desired time has been reached Note
            releaseDateTime must be in UTC format.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "transaction_id":'transactionID',
        "payout_details":'payoutDetails',
        "payout_request_amount":'payoutRequestAmount',
        "beneficiary_amount_information":'beneficiaryAmountInformation',
        "service_level":'serviceLevel',
        "beneficiary_statement_narrative":'beneficiaryStatementNarrative',
        "fx_ticket_id":'fxTicketID',
        "requested_fx":'requestedFX',
        "payer_type":'payerType',
        "payout_type":'payoutType',
        "transaction_hold":'transactionHold'
    }

    def __init__(self,
                 transaction_id=None,
                 payout_details=None,
                 payout_request_amount=None,
                 beneficiary_amount_information=None,
                 service_level=None,
                 beneficiary_statement_narrative=None,
                 fx_ticket_id=None,
                 requested_fx=None,
                 payer_type=None,
                 payout_type=None,
                 transaction_hold=None):
        """Constructor for the PaymentRegisteredBeneficiaryRequest class"""

        # Initialize members of the class
        self.transaction_id = transaction_id
        self.payout_request_amount = payout_request_amount
        self.beneficiary_amount_information = beneficiary_amount_information
        self.service_level = service_level
        self.beneficiary_statement_narrative = beneficiary_statement_narrative
        self.fx_ticket_id = fx_ticket_id
        self.requested_fx = requested_fx
        self.payer_type = payer_type
        self.payout_type = payout_type
        self.payout_details = payout_details
        self.transaction_hold = transaction_hold


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
        transaction_id = earthport-rest-api-client.models.transaction_id_merchant.TransactionIDMerchant.from_dictionary(dictionary.get('transactionID')) if dictionary.get('transactionID') else None
        payout_details = None
        if dictionary.get('payoutDetails') != None:
            payout_details = list()
            for structure in dictionary.get('payoutDetails'):
                payout_details.append(earthport-rest-api-client.models.payout_details.PayoutDetails.from_dictionary(structure))
        payout_request_amount = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('payoutRequestAmount')) if dictionary.get('payoutRequestAmount') else None
        beneficiary_amount_information = earthport-rest-api-client.models.beneficiary_amount_information.BeneficiaryAmountInformation.from_dictionary(dictionary.get('beneficiaryAmountInformation')) if dictionary.get('beneficiaryAmountInformation') else None
        service_level = dictionary.get('serviceLevel')
        beneficiary_statement_narrative = dictionary.get('beneficiaryStatementNarrative')
        fx_ticket_id = dictionary.get('fxTicketID')
        requested_fx = dictionary.get('requestedFX')
        payer_type = dictionary.get('payerType')
        payout_type = dictionary.get('payoutType')
        transaction_hold = earthport-rest-api-client.models.transaction_hold.TransactionHold.from_dictionary(dictionary.get('transactionHold')) if dictionary.get('transactionHold') else None

        # Return an object of this model
        return cls(transaction_id,
                   payout_details,
                   payout_request_amount,
                   beneficiary_amount_information,
                   service_level,
                   beneficiary_statement_narrative,
                   fx_ticket_id,
                   requested_fx,
                   payer_type,
                   payout_type,
                   transaction_hold)


