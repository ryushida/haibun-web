import base64
import configparser
import datetime
import io
import warnings

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import flask
import pandas as pd
from dash.dependencies import Input, Output, State

import plot
import sql

warnings.filterwarnings('error')

config = configparser.ConfigParser()
config.read('config.ini')

value_column = config.get('csv', 'value_column')
item_column = config.get('csv', 'item_column')
skipped_item = config.get('csv', 'skip_item')
portfolio_account_name = config.get('General', 'portfolio_account_name')

external_stylesheets = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']


external_scripts = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

# Server definition

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)
app.title = 'haibun'

df_expense = sql.get_expense_table()
df_expense_category = sql.expense_by_category()
df_subscriptions = sql.get_subscription_table()
df_account_values = sql.get_account_values()
net_worth_value = sql.get_net_worth()


def account_sums(df, df_portfolio):
    portfolio_sum = df_portfolio['account_value'].sum()
    other_sum = df[df['account_name'] !=
                   portfolio_account_name]['account_value'].sum()
    return portfolio_sum + other_sum


def get_treemap_df(df_portfolio, df_accounts):
    df_accounts = df_accounts.assign(account_type='')

    df_portfolio = df_portfolio.copy()
    df_portfolio.rename(
        columns={item_column: 'account_name', value_column: 'account_value'},
        inplace=True)
    df_portfolio = df_portfolio.assign(account_type=portfolio_account_name)
    df_portfolio.loc[:, 'proportion'] = df_portfolio['account_value'] / \
        (account_sums(df_accounts, df_portfolio)) * 100

    df_combined = pd.concat(
        [df_portfolio, df_accounts], axis=0, ignore_index=True)

    # Set group value to 0 for correct treemap appearance
    idx = df_combined.index[df_combined['account_name']
                            == portfolio_account_name].tolist()
    df_combined.at[idx, 'account_value'] = 0

    # Format proportion column
    df_combined = df_combined.round({'proportion': 1})
    df_combined['proportion'] = df_combined['proportion'].astype(str) + '%'

    return df_combined


def value_to_float(df):
    """ Convert column to float
    """
    df = df.copy()
    df[value_column] = df[value_column].astype(float)
    return df


def remove_currency_symbol(df):
    """ Remove currency symbol from column
    """
    currency_symbol = config.get('csv', 'currency_symbol')
    df = df.copy()
    df[value_column] = df[value_column].str.replace(currency_symbol, '')
    return df


def remove_items(df):
    """ Remove skipped item in dataframe
    """
    return df[df[item_column] != skipped_item]


def csv_output(df, filename, date):
    """ Return div of csv output
    """
    df = remove_items(df)
    df = remove_currency_symbol(df)
    df = value_to_float(df)

    df_treemap = get_treemap_df(df, df_account_values)

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dcc.Graph(figure=plot.total_treemap(df_treemap)),
        html.Hr(),
        dcc.Graph(figure=plot.portfolio_bar(df)),
        html.Hr(),

        # Display CSV in Table
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_table={'overflowX': 'auto'},
            sort_action='native'
        ),

        html.Hr(),

    ])


def parse_contents(contents, filename, date):
    """ Read csv and return output
    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename.lower():
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), skiprows=2)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return csv_output(df, filename, date)


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Expenses', children=[
            dcc.Graph(figure=plot.expense_category_bar(df_expense_category)),
            dash_table.DataTable(
                id='expense_table',
                columns=[{"name": i, "id": i} for i in df_expense.columns],
                data=df_expense.to_dict('records'),
                sort_action='native'
            )
        ]),
        dcc.Tab(label='Subscriptions', children=[
            dcc.Graph(figure=plot.subscription_bar(df_subscriptions)),
            dash_table.DataTable(
                id='subscription_table',
                columns=[{"name": i, "id": i}
                         for i in df_subscriptions.columns],
                data=df_subscriptions.to_dict('records'),
                sort_action='native'
            )
        ]),
        dcc.Tab(label='Net Worth', children=[
            html.P(net_worth_value),
            dcc.Graph(figure=plot.account_values_stacked_bar(
                df_account_values.sort_values('proportion',
                                              ascending=False))),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=True
            ),
            html.Div(id='output-data-upload'),
        ]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
