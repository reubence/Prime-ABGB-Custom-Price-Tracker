from bs4 import BeautifulSoup
import requests
import smtplib
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import flask
import pandas as pd
import dash_bootstrap_components as dbc
import dash_table as dt

data = pd.read_csv("dataset/Links.csv")

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'}

stylesheets = 'https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/united/bootstrap.min.css'
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, stylesheets],
                suppress_callback_exceptions=True)

app.layout = html.Div(children=[
    dbc.Row(dbc.Col(html.H1("Price Tracker",style={"color":"primary"}))),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                placeholder="Select Component",
                # style={"margin-top": 50},
                id="dd",
                options=[{"label": "CPU", "value": "cpu"},
                         {"label": "GPU", "value": "gpu"},
                         {"label": "RAM", "value": "ram"}
                         ]
            )
        ,width = 2),
        dbc.Col(
            html.Div(id="jumbo-1"),
            width=10
        )])
]
)


@app.callback(Output("jumbo-1", "children"),
              [Input("dd", "value")])
def check_prices(value):
    data = pd.read_csv("dataset/Links.csv")
    if value == "ram":
        y = data['ram']
    elif value == "gpu":
        y = data['gpu']
    else:
        y = data['cpu']

    children = []
    for x in y:
        url = x
        page = requests.get(url, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find("h1", {"class": "product_title entry-title"}).get_text()

        price_divTags = soup.findAll("p", {"class": "price"})

        price_actual = None

        for tag in price_divTags:
            price_div_final = tag.find_all("ins")
            for tag in price_div_final:
                try:
                    price_str = tag.text
                    price_float = price_str[1:7]
                    # price_actual = []
                    price_actual = float(price_float.replace(",", ""))
                except:
                    price_actual = "idk price"
            children.append(html.H3(title, style={"textColor": "primary"}))
            children.append(html.H6(price_actual,style={"textColor":"primary"}))
            children.append(dbc.Badge("Go to Site", href=url, color="info", className="mr-1"))
            children.append(html.Hr())
    return dbc.Jumbotron(children=children)


if __name__ == '__main__':
    app.run_server(debug=True)
