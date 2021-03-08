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

portfolio_account_name = config.get('General', 'portfolio_account_name')
portfolio_account_type = config.get('General', 'portfolio_account_type')

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


def treemap_df():
    df = sql.get_treemap_df(portfolio_account_type, portfolio_account_name)

    # Set group value to 0 for correct treemap appearance
    idx = df.index[df['account_name']
                            == portfolio_account_name].tolist()
    df.at[idx, 'value'] = 0

    return df


app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Data', children=[
            html.H5("Expense"),
            dcc.Graph(figure=plot.expense_category_bar(df_expense_category)),
            html.H5("Subscriptions"),
            dcc.Graph(figure=plot.subscription_bar(df_subscriptions)),
            html.P(net_worth_value),
            dcc.Graph(figure=plot.account_values_stacked_bar(
                df_account_values.sort_values('proportion',
                                              ascending=False))),

            dcc.Graph(figure=plot.total_treemap(treemap_df())),

            html.Hr(),
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
