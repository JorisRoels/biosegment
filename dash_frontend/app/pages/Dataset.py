import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app.app import app
from app import api

title="Dataset"
path="/dataset"

layout = html.Div([
    html.P(
        children="Dataset",
    ),
    html.Button('Update', id='update-dataset-button'),
    html.Div(
        id="dataset",
    )
])

def get_card_for_dataset(p):
    # print(p)
    card = dbc.Card(
    dbc.CardBody(
        [
            html.H4(p['title'], className="card-title"),
            # html.H6("Card subtitle", className="card-subtitle"),
            html.P(
                p['description'],
                className="card-text",
            ),
            dbc.CardLink("Card link", href="#"),
            dbc.CardLink("External link", href="https://google.com"),
        ]
    ),
    # style={"width": "18rem"},
    )
    return card

@app.callback([
    Output('dataset', 'children'),
], [
    Input('url', 'pathname'),
    Input('update-dataset-button', 'n_clicks'),
    Input('token', 'data')
])
def update_datasets(pathname, clicks, token):
    dataset_id = pathname.split('/')[-1]
    token = api.base.get_tokens()
    dataset = api.dataset.get(id=dataset_id, token=token)
    return [get_card_for_dataset(dataset)]

if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)