import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import home, pacientes, medicos, clinicas, consultas
from dash import html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# registra callbacks da home (filtros)
try:
    home.register_callbacks(app)
except Exception:
    pass

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Início", href="/")),
        dbc.NavItem(dbc.NavLink("Pacientes", href="/pacientes")),
        dbc.NavItem(dbc.NavLink("Médicos", href="/medicos")),
        dbc.NavItem(dbc.NavLink("Clínicas", href="/clinicas")),
        dbc.NavItem(dbc.NavLink("Consultas", href="/consultas")),
    ],
    brand=html.Span([html.Img(src='/assets/icons/logo.svg', height='28'), html.Span("Sistema Consultório Médico")]),
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4"
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
    else:
        # home provides a build_layout() function which checks DB connectivity
        try:
            return home.build_layout()
        except Exception:
            # fallback: minimal message
            return html.Div([html.H3("Erro ao montar a página inicial")])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)