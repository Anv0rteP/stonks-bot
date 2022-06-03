# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Constants:
    """
    Константы типа string
    """
    BOT_KEY = '5270429686:AAG22bIypSCISOGaI8yoNkOwhRCyAmEPH4k'
    DEFAULT_TEXT = '''Bot by Kontora P'''
    ARTEMS_ALPHA_KEY = "0AZ8CZ5S4PTD6TYI"
    ARTEMS_12_API_KEY = "9a9121f2c73b453e8a1cdc175b84cef4"
    CURRENCY = "USD;EUR;JPY;GBP;RUB;USDT;USDC;BUSD;DAI;TUSD;BTC;ETH;BNB;SOL;XRP;ADA;DOT;TRX;AVAX;SHIB;MATIC;LEO;LTC;CRO;FTT;CATGIRL;LUNA;CAKE;DOGE;SHIB"


# TXC7MQ7SEGPIWKV3
# 0AZ8CZ5S4PTD6TYI
@dataclass
class CommandRelatedConsts:
    """
    Текст различных выводов бота
    """
    HELP_TEXT = """Для выполнения базовых операция с тикером введите /start
    
Данная команда включает в себя:

Overview - Таблица подошедших/похожих тикеров и основные данные по ним;
Compartment chart - Сравнивает графики закрытия цены акции за определенный период
Candle chart - Отправляет вам график японской свечи введённого тикера за день/неделю/месяц;
Another ticker - Ввод другого тикера;
Stop - Остановка работы функции start. 
-------------------------------------
/exchange - возвращает обменный курс в реальном времени для пары валют
(например, биткойн) и физической валюты (например, доллар США).
-------------------------------------
/popularexchange - Отправляет сообщение с 5 самыми обмениваемыми валютами и по нажатию выводит их курсы
-------------------------------------
/criptoexchangerate - Отправляет сообщение с 20 криптами и по нажатию возвращает их цену в USDT

"""
