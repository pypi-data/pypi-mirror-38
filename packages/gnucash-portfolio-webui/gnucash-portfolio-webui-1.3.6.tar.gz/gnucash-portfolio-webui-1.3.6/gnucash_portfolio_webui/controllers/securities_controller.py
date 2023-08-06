"""
Stocks
- List of all stocks (non-currency commodities)
- price chart for selectable period
- price import from csv
- list of all transactions (buy/sell)
- list of all distributions
- calculation of ROI
"""
from decimal import Decimal
import logging
import flask
from flask import Blueprint, request, render_template

try:
    import simplejson as json
except ImportError:
    import json
from gnucash_portfolio.bookaggregate import BookAggregate
from gnucash_portfolio.securitiesaggregate import SecuritiesAggregate
from gnucash_portfolio_webui.models import security_models

stock_controller = Blueprint(  # pylint: disable=invalid-name
    'stock_controller', __name__, url_prefix='/security')


@stock_controller.route('/')
def index():
    """ Root. Search form. """
    # Check if we have a symbol
    symbol = request.args.get('search.symbol')

    if symbol:
        return flask.redirect(flask.url_for('stock_controller.details', symbol=symbol), code=307)
        # code 307, 302

    # else show the search form.
    with BookAggregate() as svc:
        model = __get_model_for_analysis(svc)
        search = {
            "symbol": None
        }
        return render_template('securities.html', model=model, filter=search)


@stock_controller.route('/list')
def list_securities():
    """ List all securities """
    with BookAggregate() as svc:
        all_sec = svc.securities.get_all()
        model = {
            "securities": all_sec,
            "last_prices": {}
        }
        # get last prices
        for sec in all_sec:
            if not sec.prices.count():
                continue
            agg = svc.securities.get_aggregate(sec)
            # last_price = sec.prices.order_by[-1]
            last_price = agg.get_last_available_price()
            model["last_prices"][sec.mnemonic] = last_price

        result = render_template('security.list.html', model=model)
    return result


@stock_controller.route('/details/<symbol>')
def details(symbol: str):
    """ Displays the details in a separate page. Restful url. """
    with BookAggregate() as svc:
        model = __get_model_for_details(svc, symbol)
        return render_template('security.details.html', model=model)


@stock_controller.route('/transactions/<symbol>')
def transactions():
    """ Lists all transactions for security. Symbol must include namespace. """
    return render_template('incomplete.html')


@stock_controller.route('/distributions/<symbol>')
def distributions():
    """ Distributions for the security """
    return render_template('distributions.html', model=None)


@stock_controller.route('/yield/<symbol>')
def yield_calc(symbol: str):
    """ Display yield calculations for security """
    with BookAggregate() as svc:
        agg = svc.securities.get_aggregate_for_symbol(symbol)
        model = security_models.SecurityYieldModel()

        model.symbol = agg.security.namespace + ":" + agg.security.mnemonic
        model.security = agg.security
        model.quantity = agg.get_quantity()
        model.average_price = agg.get_avg_price()
        model.total_paid = agg.get_total_paid_for_remaining_stock()
        model.price = agg.get_last_available_price()
        model.value = agg.get_value()

        model.profit_loss = Decimal(0)
        model.income = 0
        model.total_return = 0
        model.profit_loss_perc = 0
        model.income_perc = 0
        model.total_return_perc = 0

        result = render_template('security.yield.html', model=model)
    return result


###################
# API

@stock_controller.route('/api/search')
def search_api():
    """ Search for security """
    query = request.args.get('query')
    with BookAggregate() as svc:
        securities = svc.securities.find(query)
        sec_list = [{
            "value": sec.mnemonic + " - " + sec.fullname,
            "data": sec.namespace + ":" + sec.mnemonic} for sec in securities]
        model = {"suggestions": sec_list}
        result = json.dumps(model)
        return result


####################
# Private

def __get_model_for_details(
        svc: BookAggregate, symbol: str) -> security_models.SecurityDetailsViewModel:
    """ Loads the model for security details """
    sec_agg = svc.securities.get_aggregate_for_symbol(symbol)

    model = security_models.SecurityDetailsViewModel()

    model.symbol = sec_agg.security.namespace + ":" + sec_agg.security.mnemonic
    model.security = sec_agg.security

    # Quantity
    model.quantity = sec_agg.get_quantity()
    model.value = sec_agg.get_value()
    currency = sec_agg.get_currency()
    if currency:
        assert isinstance(currency, str)
        model.currency = currency
    model.price = sec_agg.get_last_available_price()

    model.average_price = sec_agg.get_avg_price()
    # Here we take only the amount paid for the remaining stock.
    model.total_paid = sec_agg.get_total_paid_for_remaining_stock()

    # Profit/loss
    model.profit_loss = model.value - model.total_paid
    if model.total_paid:
        model.profit_loss_perc = abs(model.profit_loss) * 100 / model.total_paid
    else:
        model.profit_loss_perc = 0
    if abs(model.value) < abs(model.total_paid):
        model.profit_loss_perc *= -1
    # Income
    model.income = sec_agg.get_income_total()
    if model.total_paid:
        model.income_perc = model.income * 100 / model.total_paid
    else:
        model.income_perc = 0
    # income in the last 12 months
    # income_last_year = sec_agg.get_income_total
    # model.income_perc_last_12m = 0

    # total return
    model.total_return = model.profit_loss + model.income
    if model.total_paid:
        model.total_return_perc = model.total_return * 100 / model.total_paid
    else:
        model.total_return_perc = 0

    # load all accounts
    model.accounts = sec_agg.accounts
    model.income_accounts = sec_agg.get_income_accounts()

    # Load asset classes to which this security belongs.
    # todo load asset allocation, find the parents for this symbol
    # svc.asset_allocation.load_config_only(svc.currencies.default_currency)
    # stocks = svc.asset_allocation.get_stock(model.symbol)
    #
    # for stock in stocks:
    #     model.asset_classes.append(stock.asset_class)
    from asset_allocation import AppAggregate
    aa = AppAggregate()
    aa.open_session()
    aa.get_asset_classes_for_security(None, model.symbol)

    return model


def __get_model_for_analysis(svc: BookAggregate):
    """ Loads model for analysis """
    service = SecuritiesAggregate(svc.book)
    all_securities = service.get_all()

    model = security_models.SecurityAnalysisRefModel()
    model.securities = all_securities

    return model
