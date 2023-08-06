""" Models for account views """

from decimal import Decimal
from gnucash_portfolio.lib import datetimeutils


class AccountTransactionsViewModel:
    """ View model for account transactions """
    def __init__(self):
        self.start_balance = Decimal(0)
        self.splits = []
        self.end_balance = Decimal(0)


class AccountTransactionsInputModel:
    """ User input """
    def __init__(self):
        from pydatum import Datum

        # Account id
        self.account_id: str = None

        # Date range. The default is the last week.
        # date_to = datetimeutils.today_date()
        date_to = Datum()
        date_to.today()

        date_from = date_to.clone()
        date_from.subtract_days(7)
        # date_from = date_to - timedelta(days=7)
        period = datetimeutils.get_period(date_from.value, date_to.value)
        self.period: str = period


class AccountTransactionsRefModel:
    """ Reference model for search """
    def __init__(self):
        # Dictionary of account id/fullnames.
        self.accounts = {}


class AccountDetailsViewModel:
    """ View model for account details """
    def __init__(self):
        self.account = None
        self.balance = None
        self.security_details_url = None
