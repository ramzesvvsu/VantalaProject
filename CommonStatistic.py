import plotly

plotly.offline.init_notebook_mode()
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime
from IPython.display import display
import numpy as np
import pandas as pd
import pprint as pp


def print_statistic(file, div_list, start_price, end_price):
    df = pd.read_csv(file, names=['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL'])
    df.drop(['LOW', 'TIME', 'HIGH', 'VOL'], axis=1, inplace=True)
    df.DATE = pd.to_datetime(df.DATE, dayfirst=True)
    df.OPEN = pd.to_numeric(df.OPEN)
    df.CLOSE = pd.to_numeric(df.CLOSE)
    df['Price'] = (df.OPEN + df.CLOSE) / 2
    df['Price2'] = df.Price.round(2)
    df.Price = df.Price.round(2)
    div_list.Date = pd.to_datetime(div_list.Date)
    div_list.sort_values(by='Date', inplace=True, ascending=False)
    df['Qty'] = 0
    df['QtyNoDiv'] = 0
    df['Amount'] = 0
    df['AmountNoDiv'] = 0
    df['Cash'] = 0
    df.loc[0, 'Cash'] = 100000
    df.loc[0, 'Price'] = start_price
    last_div = None
    prev_row = None
    sum_div = None
    first_qty = 0
    result_list = []

    for index, row in df.iterrows():
        if row.Cash == 0:
            row.Cash = prev_row.Cash
            row.Qty = prev_row.Qty
        found_div = div_list[div_list.Date <= row.DATE - datetime.timedelta(days=1)]
        if len(found_div) > 0 and not found_div.Date.values[0] == last_div:
            sum_div = row.Qty * found_div.Val.values[0]
            row.Cash += sum_div
            last_div = found_div.Date.values[0]

        if row.Cash // row.Price > 0 and (sum_div == None or sum_div > 0):
            #new_qty = row.Cash // row.Price
            new_qty = round(row.Cash / row.Price, 0)
            if sum_div == None:
                result_list.append([row.DATE.to_datetime64(), new_qty, 0, 0, row.Price, new_qty,
                                    row.Cash - new_qty * row.Price, row.Cash])
            else:
                result_list.append(
                    [row.DATE.to_datetime64(), row.Qty, sum_div, found_div.Val.values[0] if sum_div > 0 else 0,
                     row.Price, new_qty, row.Cash - new_qty * row.Price, row.Qty * row.Price + row.Cash])
                sum_div = 0
            row.Qty += new_qty
            #row.Cash = row.Cash - new_qty * row.Price
            row.Cash = 0
            if first_qty == 0:
                first_qty = new_qty

        df.loc[index, 'Amount'] = row.Price * row.Qty
        df.loc[index, 'AmountNoDiv'] = row.Price * first_qty
        df.loc[index, 'Qty'] = row.Qty
        df.loc[index, 'Cash'] = row.Cash
        prev_row = row
    result_list.append(
        [prev_row.DATE.to_datetime64(), prev_row.Qty, 0, 0, end_price, 0, prev_row.Cash,
         prev_row.Cash + prev_row.Qty * end_price])

    result_table = pd.DataFrame(result_list,
                                columns=['Дата', 'Количество акций', 'Общая сумма дивов', 'Дивов на 1 акцию',
                                         'Цена акции',
                                         'Количество акций новых', 'Остаток денег', 'Стоимость актива'])
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', 200)
    display(result_table)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.DATE, y=df.AmountNoDiv, name='Сумма без дивидентов'))
    fig.add_trace(go.Scatter(x=df.DATE, y=df.Amount, name='Сумма'))
    fig.update_layout(
        legend_orientation="h",
        title="График роста стоимости портфеля",
        xaxis_title="Период",
        yaxis_title="Сумма рублей",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    fig.show()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.DATE, y=df.Qty, name='Количество акций'))
    fig.update_layout(
        legend_orientation="h",
        title="График роста количества акций",
        xaxis_title="Период",
        yaxis_title="Количество акций",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        ))
    fig.show()


if __name__ == '__main__':
    start_price = round((1744.3 + 1687.6) / 2, 2)
    end_price = round((6203.5 + 6550.5) / 2, 2)
    print_statistic('LKOH_100101_200101.csv', pd.DataFrame.from_dict({'Date': ['20.12.2019',
                                                                               '09.06.2019',
                                                                               '21.12.2018',
                                                                               '11.06.2018',
                                                                               '22.12.2017',
                                                                               '10.06.2017',
                                                                               '23.12.2016',
                                                                               '12.06.2016',
                                                                               '24.12.2015',
                                                                               '14.06.2015',
                                                                               '26.12.2014',
                                                                               '15.06.2014',
                                                                               '15.08.2013',
                                                                               '13.05.2013',
                                                                               '12.11.2012',
                                                                               '11.05.2012',
                                                                               '6.05.2011',
                                                                               '7.05.2010'], 'Val': [192.00,
                                                                                                     155.00,
                                                                                                     95.00,
                                                                                                     130.00,
                                                                                                     85.00,
                                                                                                     120.00,
                                                                                                     75.00,
                                                                                                     112.00,
                                                                                                     65.00,
                                                                                                     94.00,
                                                                                                     60.00,
                                                                                                     60.00,
                                                                                                     50.00,
                                                                                                     50.00,
                                                                                                     40.00,
                                                                                                     75.00,
                                                                                                     59.00,
                                                                                                     52.00]}),
                    start_price, end_price)
