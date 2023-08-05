# -*- coding: utf-8 -*-

class RequestedFXEnum(object):

    """Implementation of the 'RequestedFX' enum.

    Method of FX that is requested by the merchant and for which EPS2 will
    attempt to use in order to settle the payout request. FF (Fixed to Fixed)
    is where no FX will be performed as payout and beneficiary currencies are
    the same. FV (Fixed to Variable) uses the supplied payout request amount
    in order to determine the beneficiary amount. VF (Variable to Fixed) uses
    the supplied beneficiary amount in order to determine the payout amount.

    Attributes:
        FF: TODO: type description here.
        FV: TODO: type description here.
        VF: TODO: type description here.

    """

    FF = 'FF'

    FV = 'FV'

    VF = 'VF'

