import configparser
from sqlalchemy import create_engine
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

host = config.get('Postgres', 'host')
port = config.get('Postgres', 'port')
dbname = config.get('Postgres', 'dbname')
user = config.get('Postgres', 'dbuser')
password = config.get('Postgres', 'dbpassword')

engine = create_engine(
    f'postgresql://{user}:{password}@{host}:{port}/{dbname}')


def get_expense_table():
    """ Return expoense df
    """
    q_table = "SELECT expense.expense_id, expense.date, \
                      account.account_name, expense.amount, \
                      expense_category.category_name, expense.note \
               FROM expense \
               LEFT JOIN expense_category \
               ON expense.category_id = expense_category.category_id \
               LEFT JOIN account \
               ON expense.account_id = account.account_id \
               ORDER BY date"

    return pd.read_sql_query(q_table, con=engine)


def get_subscription_table():
    """ Return subscription df
    """
    q_table = "SELECT subscription_name as name, \
                      subscription_price as price \
               FROM subscription \
               ORDER BY price"

    return pd.read_sql_query(q_table, con=engine)


def get_net_worth():
    """ Return net worth value
    """
    q_value = "SELECT to_char(round(SUM(account_value), 2), \
                              'fm999,999,999,999.99') \
               FROM account_value"

    return pd.read_sql_query(q_value, con=engine).iloc[0]


def get_account_values():
    """ Return accounts df
    """
    q_values = "SELECT '' as tmp, account_type.account_type, \
                       account.account_name, account_value.account_value, \
                       100 * account_value.account_value / \
                       sum(account_value.account_value) over () as proportion \
                FROM account_value \
                LEFT JOIN account \
                ON account_value.account_id = account.account_id \
                LEFT JOIN account_type \
                ON account_type.account_type_id = account.account_type_id \
                ORDER BY proportion"

    return pd.read_sql_query(q_values, con=engine)
