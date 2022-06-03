# -*- coding: utf-8 -*-

import telebot
from telebot import types
from constants import Constants, CommandRelatedConsts
from stock_class import CurrentStock
from api_work import search, quote_endpoint, cur_exchange_rate
from charts import make_candlestick_chart, make_chart
import df2img

bot = telebot.TeleBot(Constants.BOT_KEY)
user_tickers = {}
data_frames = {}
user_additional_data = {}


@bot.message_handler(commands=['exchange'])
def show_cur_exchange_rate(message):
    """
    Вывод сообщения с требуемым форматом ввода для exchange

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """
    bot.send_message(message.chat.id, "To convert write in the next format |CUR1 CUR2 AMMOUNT|")
    bot.register_next_step_handler(message, exchange_calculator)


def exchange_calculator(message):
    """
    Обрабатывает пользовательский ввод для exchange

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """
    try:
        from_curr, to_curr, amount = message.text.split()
        convert_price = cur_exchange_rate(from_curr, to_curr)
        bot.send_message(message.chat.id,
                         amount + ' ' + from_curr + ' = ' + str(int(amount) * convert_price) + ' ' + to_curr)
    except ValueError:
        bot.send_message(message.chat.id, "Incorrect input :(")


@bot.message_handler(commands=['criptoexchangerate'])
def cripto_exchange_rate_handler(message):
    """
    Вывод inline-клавиатуры для популярных криптовалют

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """
    cur_array = ["BTC", "ETH", "BNB", "SOL", "ADA", "XRP", "DOT", "TRX", "AVAX", "SHIB", "MATIC", "LEO", "LTC", "CRO",
                 "FTT", "CATGIRL", "LUNA", "CAKE", "DOGE", "SHIB"]
    markup = make_markup(cur_array, mode=2)
    bot.send_message(message.chat.id, "Exchange rate of 20 criptos", reply_markup=markup)


@bot.message_handler(commands=['popularexchange'])
def exchange_rate_handler(message):
    """
    Вывод inline-клавиатуры для курса обмена популярных валют

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """
    cur_array = ["$", "€", "¥", "£", "₽"]
    cur_iso_code_array = ["USD", "EUR", "JPY", "GBP", "RUB"]
    markup = make_markup(cur_array, cur_iso_code_array, 1)
    bot.send_message(message.chat.id, "Exchange rate of 5 most traded currencies", reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: call.data[:call.data.rfind(";")] in Constants.CURRENCY and not is_num(call.data))
def exchange_rate_sender(callback):
    """
    Обрабатывает нажатие кнопок в обменных функциях

    :param callback: Содержит пользовательский выбор c inline-клавиатуре
    :type callback: telebot.types.CallbackQuery
    """

    from_cur = callback.data[:callback.data.rfind(";")]
    to_cur = callback.data[callback.data.rfind(";") + 1:]
    try:
        data = cur_exchange_rate(from_cur=from_cur, to_cur=to_cur)
        bot.send_message(callback.message.chat.id, "1 " + from_cur + " = " + str(data) + ' ' + to_cur)
    except ValueError:
        bot.send_message(callback.message.chat.id,
                         "1 " + from_cur + " = 0.0 " + to_cur + "  (or alpha vanture limit is broken)")


@bot.message_handler(content_types="text")
def text_handler(message):
    """
    Обрабатывает любой введенный текст на проверку существующий команды

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """
    try:
        handlers_dict[message.text.lower()](message)
    except KeyError:
        bot.send_message(message.chat.id, Constants.DEFAULT_TEXT)


def ticker_input(message):
    """Ввод тикера """
    user_tickers[message.chat.id] = message.text
    overview_result(message)


def ticker_input_handler(message):
    """
    Обработка введенного тикера, вывод кнопок для дальнейших операций с тикером

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """

    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Compartment chart", callback_data="compartment_chart"),
               types.InlineKeyboardButton("Candle chart", callback_data="candle_chart"))
    markup.add(types.InlineKeyboardButton("Another ticker", callback_data="another_ticker"),
               types.InlineKeyboardButton("Stop", callback_data="stop"))

    bot.send_message(message.chat.id, "Choose variant", reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: call.data in ["overview", "candle_chart", "another_ticker", "stop", "compartment_chart"])
def data_processing_variant_handler(callback):
    """
    Обработка кнопок операций с тикером

    :param callback: Содержит пользовательский выбор c inline-клавиатуре
    :type callback: telebot.types.CallbackQuery
    """
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)

    if callback.data == 'candle_chart':
        candle_handler(callback.message)
    elif callback.data == 'another_ticker':
        start_handler(callback.message)
    elif callback.data == "compartment_chart":
        bot.send_message(callback.message.chat.id, "Введите Тикер с которым будете сравнивать")
        bot.register_next_step_handler(callback.message, compartment_chart)
    else:
        bot.send_message(callback.message.chat.id, "Hope that you found everything that you needed")


def candle_handler(message):
    """
    Обрабатывает пользовательский ввод для определения периода графика свеч

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(types.InlineKeyboardButton("Daily adjusted - 1", callback_data="Daily1"))
    markup.add(types.InlineKeyboardButton("Weekly adjusted - 2", callback_data="Weekly1"))
    markup.add(types.InlineKeyboardButton("Monthly adjusted - 3", callback_data="Monthly1"))
    bot.send_message(message.chat.id, "Pic will be rendering for some time, pls wait :)")
    bot.send_message(message.chat.id, "Daily adjusted - 1; Weekly adjusted - 2; Monthly adjusted - 3;",
                     reply_markup=markup)


def compartment_chart(message):
    """
    Обрабатывает пользвотельский ввод второго значения тикера для построения графика сравнения, также спрашивает
    период графика

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """
    user_additional_data[message.chat.id] = message.text
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(types.InlineKeyboardButton("Daily adjusted - 1", callback_data="Daily2"))
    markup.add(types.InlineKeyboardButton("Weekly adjusted - 2", callback_data="Weekly2"))
    markup.add(types.InlineKeyboardButton("Monthly adjusted - 3", callback_data="Monthly2"))
    bot.send_message(message.chat.id, "Pic will be rendering for some time, pls wait :)", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data[:-1] in ["Daily", "Weekly", "Monthly"])
def adjusted_num_handler(callback):
    """
    Обработка нажатие кнопки при выборе периодов вывода графика

    :param callback: Содержит пользовательский выбор c inline-клавиатуре
    :type callback: telebot.types.CallbackQuery
    """
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    try:
        if callback.data[-1] == '1':
            make_candlestick_chart(callback.data[:-1], user_tickers[callback.message.chat.id])
        elif callback.data[-1] == '2':
            make_chart(callback.data[:-1], user_tickers[callback.message.chat.id],
                       user_additional_data[callback.message.chat.id])
        picture = open("../images/fig1.png", 'rb')
        bot.send_photo(callback.message.chat.id, picture, caption="Here you are")
        picture.close()
    except ValueError:
        bot.send_message(callback.message.chat.id, "Incorrect token")
    finally:
        callback.message.text = user_tickers[callback.message.chat.id]
        ticker_input_handler(callback.message)


def overview_result(message):
    """
    Вывод оверьвю полученного тикера в .png формате

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """

    ticker = user_tickers[message.chat.id]
    try:
        data = search(ticker)
        data_frames[message.chat.id] = data
        markup = types.InlineKeyboardMarkup()
        if data.shape[0] % 2 == 0:
            for i in range(0, data.shape[0], 2):
                markup.row(types.InlineKeyboardButton(data.iloc[i]["symbol"], callback_data=str(i)),
                           types.InlineKeyboardButton(data.iloc[i + 1]["symbol"], callback_data=str(i + 1)))
        else:
            for i in range(0, data.shape[0]):
                markup.row(types.InlineKeyboardButton(data.iloc[i]["symbol"], callback_data=str(i)))

        markup.add(types.InlineKeyboardButton("Exit overview", callback_data="-1"))
        bot.send_message(message.chat.id, "Here are the search results:\n")
        fig = df2img.plot_dataframe(data[['symbol', 'name', 'type']], title=dict(
            font_color="black",
            font_family="Arial",
            font_size=22,
            text="Search Result",
            y=0.98
        ),
                                    tbl_header=dict(
                                        align="center",
                                        fill_color="darkgray",
                                        font_color="white",
                                        font_family="Arial",
                                        font_size=12,
                                        line_color="darkslategray",
                                    ),
                                    tbl_cells=dict(
                                        align="center",
                                        font_family="Arial",
                                        font_color="#434343",
                                        line_color="darkslategray",
                                        height=30
                                    ),
                                    row_fill_color=("#ffffff", "#efefef"),
                                    col_width=[0.5, 1.3, 3, 1],
                                    fig_size=(500, 55 * data.shape[0]), )

        df2img.save_dataframe(fig=fig, filename="../images/plot1.png")

        picture = open("../plot1.png", 'rb')
        bot.send_photo(message.chat.id, photo=picture, reply_markup=markup)
        bot.send_message(message.chat.id,
                         "Press the ticker of the company you are interested in.")
    except KeyError:
        bot.send_message(message.chat.id, "No data was received")
        overview_result(ticker)


@bot.callback_query_handler(func=lambda call: call.data in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-1'])
def data_processing_variant_handler(callback):
    """
    Обработка нажатия кнопки в /overview

    :param callback: Содержит пользовательский выбор c inline-клавиатуре
    :type callback: telebot.types.CallbackQuery
    """
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id)
    if callback.data == '-1':
        bot.send_message(callback.message.chat.id, "Finished")
        callback.message.text = user_tickers[callback.message.chat.id]
        ticker_input(callback.message)
    else:
        user_index_input(callback)


def user_index_input(message):
    """
    Обработка ввода id тикера из .png таблицы

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """
    data = data_frames[message.message.chat.id]
    try:
        overview_dataframe = data.iloc[int(message.data)]
        tmp_stock = CurrentStock(overview_dataframe['symbol'], overview_dataframe['name'],
                                 overview_dataframe['type'], overview_dataframe['region'],
                                 overview_dataframe['timezone'], overview_dataframe['currency'], )
        overview_dataframe = quote_endpoint(tmp_stock.symbol)
        tmp_stock.add(overview_dataframe.iloc[0]['price'], overview_dataframe.iloc[0]['open'],
                      overview_dataframe.iloc[0]['high'],
                      overview_dataframe.iloc[0]['low'], overview_dataframe.iloc[0]['previous close'],
                      overview_dataframe.iloc[0]['change'],
                      overview_dataframe.iloc[0]['change percent'], overview_dataframe.iloc[0]['volume'])

        bot.send_message(message.message.chat.id, tmp_stock.__str__())
        print(tmp_stock.symbol)
    except ValueError:
        bot.send_message(message.message.chat.id, "No data was received, sorry!")
    finally:
        message.message.text = tmp_stock.symbol
        user_tickers[message.message.chat.id] = tmp_stock.symbol
        ticker_input_handler(message.message)


def help_command_handler(message):
    """
    Вывод сообщения команды /help

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """
    bot.send_message(message.chat.id, CommandRelatedConsts.HELP_TEXT)


def start_handler(message):
    """
    Вывод сообщения команды /start

    :param message: Содержит пользовательский ввод
    :type message: telebot.types.Message
    """
    # message equals to /start
    bot.send_message(message.chat.id, "Введите токен")  # bot sends message
    bot.register_next_step_handler(message, ticker_input)


def make_markup(cur_array, cur_iso_code_array=None, mode=1):
    """
    Создание inline-клавиатуры для валют

    :param cur_array: Массив валют
    :type cur_array: List
    :param cur_iso_code_array: Массив валют в iso формате
    :type cur_iso_code_array: List
    :param mode: Режим работы функции
    :type mode: Integer
    :return: Inline-клавиатура
    :rtype: telebot.types.InlineKeyboardMarkup
    """
    if not cur_iso_code_array:
        cur_iso_code_array = cur_array

    markup = types.InlineKeyboardMarkup()
    if mode == 1:
        #  Мод 1 для перевода из многих валют в многие
        for i in range(len(cur_array)):
            buttons_arr = []
            for j in range(len(cur_array)):
                if i != j:
                    buttons_arr.append(
                        types.InlineKeyboardButton(cur_array[i] + "➔" + cur_array[j],
                                                   callback_data=cur_iso_code_array[i] + ';' + cur_iso_code_array[j]))

            markup.row(*buttons_arr)

    elif mode == 2:
        #  Мод 2 для перевода из многих валют в одну конкретную
        cur_iso_code_array = "USDT"
        for i in range(0, 20, 5):
            markup.row(
                types.InlineKeyboardButton(cur_array[i],
                                           callback_data=cur_array[i] + ';' + cur_iso_code_array),
                types.InlineKeyboardButton(cur_array[i + 1],
                                           callback_data=cur_array[i + 1] + ';' + cur_iso_code_array),
                types.InlineKeyboardButton(cur_array[i + 2],
                                           callback_data=cur_array[i + 2] + ';' + cur_iso_code_array),
                types.InlineKeyboardButton(cur_array[i + 3],
                                           callback_data=cur_array[i + 3] + ';' + cur_iso_code_array),
                types.InlineKeyboardButton(cur_array[i + 4],
                                           callback_data=cur_array[i + 4] + ';' + cur_iso_code_array))

    return markup


def is_num(number: str):
    """
    Проверка String на возможность конвертации в число

    :param number: Строка
    :type number: String
    :return:
    """
    number = number.replace('-', '')
    if number.isnumeric():
        return True
    else:
        return False


handlers_dict = {
    "/help": help_command_handler,
    "/start": start_handler,
}

if __name__ == "__main__":
    bot.polling(none_stop=True)
