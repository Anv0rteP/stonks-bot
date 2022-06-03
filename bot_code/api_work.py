# -*- coding: utf-8 -*-

from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
from constants import Constants

ts = TimeSeries(key=Constants.ARTEMS_ALPHA_KEY, output_format='pandas', indexing_type='integer')
fd = FundamentalData(key=Constants.ARTEMS_ALPHA_KEY)
fx = ForeignExchange(key=Constants.ARTEMS_ALPHA_KEY)


def search(ticker):
    """
    Обработка api-запроса для получения таблицы биржевых инструментов

    :param ticker: Тикер биржевого инструмента
    :type ticker: String
    :return: Датафрейм с основными данными по тикеру
    :rtype: pandas.DataFrame
    """
    return ts.get_symbol_search(ticker)[0].rename(columns={
        '1. symbol': 'symbol', '2. name': 'name', '3. type': 'type', '4. region': 'region', '7. timezone': 'timezone',
        '8. currency': 'currency'})


def quote_endpoint(ticker):
    """
    Обработка api-запроса для получения дополнительных значений акции, необходимых для построения графиков

    :param ticker: Тикер биржевого инструмента
    :type ticker: String
    :return: Датафрейм с нужными для построения графиков данными
    :rtype: pandas.DataFrame
    """
    return ts.get_quote_endpoint(ticker)[0].rename(columns={
        '01. symbol': 'symbol', '02. open': 'open', '03. high': 'high', '04. low': 'low', '05. price': 'price',
        '06. volume': 'volume', "07. latest trading day": "latest trading day", "08. previous close": "previous close",
        "09. change": "change", "10. change percent": "change percent"})


def cur_exchange_rate(from_cur, to_cur):
    """
    Обработка api-запроса для получения курсов обмена

    :param from_cur: Конвертируемая валюта
    :type from_cur: String
    :param to_cur: Итоговая валюта
    :type to_cur: String
    :return: Цена итоговой валюты
    :rtype: Float
    """
    return round(float(fx.get_currency_exchange_rate(from_cur, to_cur)[0]["5. Exchange Rate"]), 3)


