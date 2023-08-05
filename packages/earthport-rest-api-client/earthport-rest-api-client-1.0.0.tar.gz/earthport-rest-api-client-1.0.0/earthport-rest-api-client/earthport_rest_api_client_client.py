# -*- coding: utf-8 -*-

from .decorators import lazy_property
from .configuration import Configuration
from .controllers.quotes_controller import QuotesController
from .controllers.balances_controller import BalancesController
from .controllers.payments_controller import PaymentsController
from .controllers.beneficiary_bank_accounts_controller import BeneficiaryBankAccountsController
from .controllers.authentication_controller import AuthenticationController
from .controllers.users_controller import UsersController
from .controllers.transactions_controller import TransactionsController
from .controllers.statements_controller import StatementsController
from .controllers.settlement_calendars_controller import SettlementCalendarsController

class EarthportRestApiClientClient(object):

    config = Configuration

    @lazy_property
    def quotes(self):
        return QuotesController()

    @lazy_property
    def balances(self):
        return BalancesController()

    @lazy_property
    def payments(self):
        return PaymentsController()

    @lazy_property
    def beneficiary_bank_accounts(self):
        return BeneficiaryBankAccountsController()

    @lazy_property
    def authentication(self):
        return AuthenticationController()

    @lazy_property
    def users(self):
        return UsersController()

    @lazy_property
    def transactions(self):
        return TransactionsController()

    @lazy_property
    def statements(self):
        return StatementsController()

    @lazy_property
    def settlement_calendars(self):
        return SettlementCalendarsController()


    def __init__(self, 
                 authorization = None):
        if authorization != None:
            Configuration.authorization = authorization


