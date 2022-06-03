import plotly.graph_objects as go
import plotly.io as pio
from alpha_vantage.timeseries import TimeSeries
from constants import Constants
import plotly.express as px

ts = TimeSeries(key=Constants.ARTEMS_ALPHA_KEY, output_format='pandas')
pio.kaleido.scope.default_format = 'png'


def time_series_data(option, symbol):
    """
    Обработка диапазона времени для создания графика

    :param option: Диапазон даты
    :type option: String
    :param symbol: Тикер компании
    :type symbol: String
    :return: Датафрейм для постройки графика
    :rtype: pandas.DataFrame
    """
    if option == 'Daily':
        data = ts.get_daily(symbol)[0]
    elif option == 'Weekly':
        data = ts.get_weekly(symbol)[0]
    elif option == 'Monthly':
        data = ts.get_monthly(symbol)[0]

    return data


def make_candlestick_chart(option: str, symbol):
    """
    Создание .png для графика свеч

    :param option: Диапазон даты
    :type option: String
    :param symbol: Тикер компании
    :type symbol: String
    """
    option = option.strip()
    data = time_series_data(option, symbol)

    figure = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data['1. open'],
                high=data['2. high'],
                low=data['3. low'],
                close=data['4. close'],
                increasing_line_color='green',
                decreasing_line_color='red',
            )
        ]
    )
    figure.update_layout(xaxis_rangeslider_visible=False, width=1600, height=1000,
                         xaxis=dict(tickfont=dict(family="Arial", size=18), title="Date"),
                         yaxis=dict(tickfont=dict(family="Arial", size=18), title="Numbers"),
                         )

    figure.write_image("../images/fig1.png", format='png')


def make_chart(option, ticker1, ticker2):
    """
    Создание .png для графика сравнения

    :param option: Диапазон даты
    :type option: String
    :param ticker1: Тикер первой компании
    :type ticker1: String
    :param ticker2: Тикер второй компании
    :type ticker2: String
    """
    tikcer1_data = time_series_data(option, ticker1)
    tikcer2_data = time_series_data(option, ticker2)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tikcer1_data.index, y=tikcer1_data["4. close"], mode="lines+markers", name=ticker1,
                             line=dict(color="black", width=2)))
    fig.add_trace(go.Scatter(x=tikcer2_data.index, y=tikcer2_data["4. close"], mode="lines+markers", name=ticker2,
                             line=dict(color="red", width=2)))
    fig.update_layout(title=ticker1 + " vs " + ticker2, width=1600, height=1000,
                      xaxis=dict(tickfont=dict(family="Arial", size=18), title="Date"),
                      yaxis=dict(tickfont=dict(family="Arial", size=18), title="Close price"),
                      legend=dict(font=dict(family="Arial", size=28, color="black")),
                      )

    fig.for_each_xaxis(lambda axis: axis.title.update(font=dict(color='black', size=30)))
    fig.for_each_yaxis(lambda axis: axis.title.update(font=dict(color='black', size=30)))

    fig.write_image("../images/fig1.png", format='png')
