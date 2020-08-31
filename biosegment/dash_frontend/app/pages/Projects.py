import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app.app import app
from app import api

title="Projects"
path="/projects"

layout = html.Div([
    html.P(
        children="Projects",
    ),
    html.Button('Update', id='update-button-projects'),
    html.Div(
        id="projects",
    )
])

def get_card_for_project(p):
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
    Output('projects', 'children'),
], [Input('update-button-projects', 'n_clicks')])
def update_projects(clicks):
    projects = api.project.get_multi()
    return [[get_card_for_project(p) for p in projects]]

if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)