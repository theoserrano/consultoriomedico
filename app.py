# -*- coding: utf-8 -*-
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import home, pacientes, medicos, clinicas, consultas, analytics
from dash import html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)

# Registra callbacks das páginas
try:
    home.register_callbacks(app)
except Exception:
    pass

try:
    analytics.register_callbacks(app)
except Exception:
    pass

navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.NavbarBrand([
                    html.I(className="bi bi-hospital-fill me-2"),
                    "Sistema Consultório Médico"
                ], href="/", className="fs-4")
            ]),
        ], className="flex-grow-1 align-items-center"),
        dbc.Row([
            dbc.Col([
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink([html.I(className="bi bi-house-fill me-1"), "Início"], href="/", className="px-3")),
                    dbc.NavItem(dbc.NavLink([html.I(className="bi bi-people-fill me-1"), "Pacientes"], href="/pacientes", className="px-3")),
                    dbc.NavItem(dbc.NavLink([html.I(className="bi bi-person-badge-fill me-1"), "Médicos"], href="/medicos", className="px-3")),
                    dbc.NavItem(dbc.NavLink([html.I(className="bi bi-building-fill me-1"), "Clínicas"], href="/clinicas", className="px-3")),
                    dbc.NavItem(dbc.NavLink([html.I(className="bi bi-calendar-check-fill me-1"), "Consultas"], href="/consultas", className="px-3")),
                    dbc.NavItem(dbc.NavLink([html.I(className="bi bi-bar-chart-fill me-1"), "Analytics"], href="/analytics", className="px-3")),
                ], navbar=True, className="ms-auto")
            ])
        ], className="flex-grow-1")
    ], fluid=True),
    color="primary",
    dark=True,
    className="mb-4 shadow-sm",
    style={"minHeight": "70px"}
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content', fluid=True)
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/pacientes':
        return pacientes.layout
    elif pathname == '/medicos':
        return medicos.layout
    elif pathname == '/clinicas':
        return clinicas.layout
    elif pathname == '/consultas':
        return consultas.layout
    elif pathname == '/analytics':
        return analytics.layout
    else:
        # home provides a build_layout() function which checks DB connectivity
        try:
            return home.build_layout()
        except Exception:
            # fallback: minimal message
            return html.Div([html.H3("Erro ao montar a página inicial")])

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8050)