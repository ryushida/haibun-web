import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objs as gobs


def subscription_bar(df):
    """ horizontal bar with price of each subscription
    """
    fig = px.bar(df, y='name', x='price', orientation='h')
    return fig


def account_values_stacked_bar(df):
    """ horizontal stacked bar with proportion of each account
    """
    fig = px.bar(df, y='tmp', x='proportion', color='account_name',
                 text='account_value', orientation='h')
    return fig


def portfolio_bar(df):
    """ horizontal bar with value of each item
    """
    fig = px.bar(df, y='Symbol', x='Market Value', orientation='h')
    fig.update_layout(barmode='stack',
                      yaxis={'categoryorder': 'total ascending'},
                      height=len(df)*30)
    return fig


def total_treemap(df):
    """ treemap with value of each item
    """
    fig = go.Figure(go.Treemap(
        labels=df['account_name'],
        parents=df['account_type'],
        values=df['value'],
        text=df['proportion'],
        hovertemplate='<b>%{label} </b><br>Value: %{value}<br><br>%{text}</br>'
    ))
    return fig

def expense_category_bar(df):
    """ bar graph of expenses by category
    """
    fig = px.bar(df, x='sum', y='category', orientation='h')
    return fig
