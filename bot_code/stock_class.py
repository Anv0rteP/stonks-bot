class CurrentStock:
    def __init__(self, symbol, name, stock_type, region, timezone, currency):
        """
        Хранение основной информации об обрабатываемой компании

        :param symbol: Тикер
        :type symbol: String
        :param name: Название компании
        :type name: String
        :param stock_type: Тип биржевого инструмента
        :type stock_type: String
        :param region: Регион биржевого инструмента
        :type region: String
        :param timezone: Таймзона биржевого инструмента
        :type timezone: String
        :param timezone: Валюта торговли биржевого инструмента
        :type timezone: String
        """
        self.symbol = symbol
        self.name = name
        self.stock_type = stock_type
        self.region = region
        self.timezone = timezone
        self.currency = currency

        self.volume = None
        self.price = None
        self.open_price = None
        self.high_price = None
        self.low_price = None
        self.prev_close = None
        self.change = None
        self.change_percent = None

    def __str__(self):
        return f"""{self.symbol} | {self.name}
{self.stock_type} trading in {self.currency}
{self.region}, timezone is {self.timezone}

Current price is {self.price}, with volume of {self.volume}
Borders are {self.low_price} and {self.high_price} {self.currency}
Previous day close was {self.prev_close} {self.currency}
Change since previous day is {self.change} {self.currency} or {self.change_percent}"""

    def add(self, price, open_price, high_price, low_price, prev_close, change, change_percent, volume):
        """
        Добавление дополнительных параметров компании

        :param price: Текущая цена
        :type price: Float
        :param open_price: Цена открытия
        :type open_price: Float
        :param high_price: Высшая точка цены
        :type high_price: Float
        :param low_price: Низшая точка цены
        :type low_price: Float
        :param prev_close: Цена закрытия предыдущего дня торгов
        :type prev_close: Float
        :param change: Изменение цены
        :type change: Float
        :param change_percent: Изменение цены в процентах
        :type change_percent: Float
        :param volume: Объем продаж акции
        :type volume: Integer
        """
        self.price = price
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.prev_close = prev_close
        self.change = change
        self.change_percent = change_percent
        self.volume = volume

