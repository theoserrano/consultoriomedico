from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from db import db, logger
import pandas as pd
from datetime import datetime
import json


def build_layout():
    # Mensagem se não há conexão com o banco
    if not db.ensure_connected():
        return dbc.Container([
            dbc.Row(dbc.Col(html.H2("Dashboard - Consultório Médico", className="text-center mb-4"))),
            dbc.Row(dbc.Col(dbc.Alert([
                html.H4("Sem conexão com o banco de dados", className="alert-heading"),
                html.P("A aplicação não conseguiu conectar ao MySQL. Verifique o arquivo `.env` e as credenciais."),
                html.P("Passos rápidos: 1) confirme MySQL rodando; 2) importe o dump; 3) atualize `DB_USER`/`DB_PASSWORD` em `.env`."),
                html.P("Consulte o README para instruções completas.")
            ], color="danger"), width=12)),
        ], fluid=True)

    total_pacientes = db.fetch_one("SELECT COUNT(*) as total FROM tabelapaciente")
    total_medicos = db.fetch_one("SELECT COUNT(*) as total FROM tabelamedico")
    total_clinicas = db.fetch_one("SELECT COUNT(*) as total FROM tabelaclinica")
    total_consultas = db.fetch_one("SELECT COUNT(*) as total FROM tabelaconsulta")

    stats = {
        'pacientes': total_pacientes['total'] if total_pacientes else 0,
        'medicos': total_medicos['total'] if total_medicos else 0,
        'clinicas': total_clinicas['total'] if total_clinicas else 0,
        'consultas': total_consultas['total'] if total_consultas else 0
    }

    proximas = db.fetch_all("""
        SELECT 
            c.Data_Hora,
            p.NomePac,
            m.NomeMed,
            cl.NomeCli
        FROM tabelaconsulta c
        JOIN tabelapaciente p ON c.CpfPaciente = p.CpfPaciente
        JOIN tabelamedico m ON c.CodMed = m.CodMed
        JOIN tabelaclinica cl ON c.CodCli = cl.CodCli
        WHERE c.Data_Hora >= NOW()
        ORDER BY c.Data_Hora
        LIMIT 5
    """)

    especialidades = db.fetch_all("""
        SELECT 
            m.Especialidade,
            COUNT(*) as total
        FROM tabelaconsulta c
        JOIN tabelamedico m ON c.CodMed = m.CodMed
        GROUP BY m.Especialidade
        ORDER BY total DESC
    """)

    consultas_raw = db.fetch_all("SELECT c.CodCli, c.CodMed, c.CpfPaciente, c.Data_Hora, cl.NomeCli, m.NomeMed, p.NomePac, p.DataNascimento, p.Genero as GeneroPac, m.Genero as GeneroMed FROM tabelaconsulta c JOIN tabelaclinica cl ON c.CodCli=cl.CodCli JOIN tabelamedico m ON c.CodMed=m.CodMed JOIN tabelapaciente p ON c.CpfPaciente=p.CpfPaciente")
    df_cons = pd.DataFrame(consultas_raw) if consultas_raw else pd.DataFrame()
    if not df_cons.empty:
        # converte Data_Hora para datetime
        try:
            df_cons['Data_Hora'] = pd.to_datetime(df_cons['Data_Hora'])
        except Exception:
            # em SQLite pode ser texto não compatível
            df_cons['Data_Hora'] = pd.to_datetime(df_cons['Data_Hora'], errors='coerce')
        # extrai dia/hora
        df_cons['date'] = df_cons['Data_Hora'].dt.date
        df_cons['hour'] = df_cons['Data_Hora'].dt.hour
        df_cons['weekday'] = df_cons['Data_Hora'].dt.day_name()
        # calcula idade aproximada a partir da data de nascimento
        def compute_age(dob):
            try:
                d = pd.to_datetime(dob)
                today = pd.Timestamp.now()
                return int((today - d).days / 365.25)
            except Exception:
                return None

        df_cons['age'] = df_cons['DataNascimento'].apply(compute_age) if 'DataNascimento' in df_cons.columns else None

    # figuras (inicializadas vazias)
    fig_timeseries = None
    fig_by_medico = None
    fig_gender = None
    fig_by_clinica = None
    fig_heatmap = None
    fig_age_hist = None
    fig_box_cons_med = None
    fig_scatter_med = None

    if not df_cons.empty:
        # série temporal: consultas por dia
        ts = df_cons.groupby('date').size().reset_index(name='count')
        fig_timeseries = px.line(ts, x='date', y='count', title='Consultas por Dia')
        # consultas por médico (top)
        by_med = df_cons.groupby('NomeMed').size().reset_index(name='count').sort_values('count', ascending=False)
        fig_by_medico = px.bar(by_med.head(12), x='NomeMed', y='count', title='Consultas por Médico')
        # distribuição por gênero (pacientes)
        if 'GeneroPac' in df_cons.columns:
            gender = df_cons['GeneroPac'].fillna('Desconhecido').value_counts().reset_index()
            gender.columns = ['Genero', 'count']
            fig_gender = px.pie(gender, names='Genero', values='count', title='Distribuição por Gênero (Pacientes)')

        # área por clínica
        by_cli = df_cons.groupby('NomeCli').size().reset_index(name='count').sort_values('count', ascending=False)
        fig_by_clinica = px.area(by_cli, x='NomeCli', y='count', title='Consultas por Clínica')
        # heatmap hora x dia
        heat = df_cons.groupby(['weekday', 'hour']).size().reset_index(name='count')
        # pivot da tabela
        heat_pivot = heat.pivot(index='hour', columns='weekday', values='count').fillna(0)
        # ordena dias da semana padrão
        weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        cols = [c for c in weekdays if c in heat_pivot.columns]
        if not heat_pivot.empty:
            fig_heatmap = go.Figure(data=go.Heatmap(z=heat_pivot[cols].values, x=cols, y=heat_pivot.index, colorscale='Viridis'))
            fig_heatmap.update_layout(title='Heatmap: Hora do Dia x Dia da Semana')
        # histograma de idades
        if 'age' in df_cons.columns and df_cons['age'].notnull().any():
            fig_age_hist = px.histogram(df_cons, x='age', nbins=12, title='Distribuição de Idades dos Pacientes')
        # boxplot: idades por médico
        cons_per_med = df_cons.groupby('NomeMed').size().reset_index(name='count')
        fig_box_cons_med = px.box(df_cons, x='NomeMed', y='age', title='Boxplot: Idades por Médico (amostra)') if 'age' in df_cons.columns else None
        # scatter: médicos vs número de consultas
        fig_scatter_med = px.scatter(by_med.head(50), x='NomeMed', y='count', size='count', title='Consultas por Médico (scatter)')

    layout = dbc.Container([
        # filtros interativos: clínica, médico, período
        dbc.Row([
            dbc.Col(dbc.Label("Clínica"), md=1),
            dbc.Col(dcc.Dropdown(id='filter-clinica', options=[{'label': 'Todas', 'value': ''}], value='', clearable=False), md=3),
            dbc.Col(dbc.Label("Médico"), md=1),
            dbc.Col(dcc.Dropdown(id='filter-medico', options=[{'label': 'Todos', 'value': ''}], value='', clearable=False), md=3),
            dbc.Col(dbc.Label("Período"), md=1),
            dbc.Col(dcc.DatePickerRange(id='filter-periodo', start_date=None, end_date=None, display_format='YYYY-MM-DD'), md=3),
        ], className='mb-3'),

        dbc.Row([
            dbc.Col([
                html.H2("Dashboard - Consultório Médico", className="text-center mb-4")
            ])
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(stats['pacientes'], className="text-center"),
                        html.P("Pacientes", className="text-center text-muted")
                    ])
                ], color="primary", outline=True)
            ], md=3),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(stats['medicos'], className="text-center"),
                        html.P("Médicos", className="text-center text-muted")
                    ])
                ], color="success", outline=True)
            ], md=3),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(stats['clinicas'], className="text-center"),
                        html.P("Clínicas", className="text-center text-muted")
                    ])
                ], color="info", outline=True)
            ], md=3),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(stats['consultas'], className="text-center"),
                        html.P("Consultas", className="text-center text-muted")
                    ])
                ], color="warning", outline=True)
            ], md=3),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Próximas Consultas")),
                    dbc.CardBody([
                        html.Div(id='proximas-table', children=(
                            dbc.Table.from_dataframe(
                                pd.DataFrame(proximas),
                                striped=True,
                                bordered=True,
                                hover=True,
                                responsive=True
                            ) if proximas else html.P("Nenhuma consulta agendada", className="text-muted")
                        ))
                    ])
                ])
            ], md=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Consultas por Especialidade")),
                    dbc.CardBody([
                        dcc.Graph(
                            id='graph-especialidades',
                            figure={
                                'data': [go.Bar(
                                    x=[e['Especialidade'] for e in especialidades],
                                    y=[e['total'] for e in especialidades],
                                    marker_color='lightblue'
                                )],
                                'layout': go.Layout(
                                    xaxis={'title': 'Especialidade'},
                                    yaxis={'title': 'Total de Consultas'},
                                    margin={'l': 40, 'b': 100, 't': 10, 'r': 10}
                                )
                            }
                        ) if especialidades else html.P("Sem dados", className="text-muted")
                    ])
                ])
            ], md=6),
        ], className="mb-4"),

        # Gráficos avançados
        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader("Consultas por Dia"), dbc.CardBody(dcc.Graph(id='graph-timeseries', figure=fig_timeseries if fig_timeseries is not None else {}))]), md=6),
            dbc.Col(dbc.Card([dbc.CardHeader("Consultas por Médico"), dbc.CardBody(dcc.Graph(id='graph-by-medico', figure=fig_by_medico if fig_by_medico is not None else {}))]), md=6),
        ], className='mb-3'),

        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader("Distribuição por Gênero (Pacientes)"), dbc.CardBody(dcc.Graph(id='graph-gender', figure=fig_gender if fig_gender is not None else {}))]), md=4),
            dbc.Col(dbc.Card([dbc.CardHeader("Consultas por Clínica"), dbc.CardBody(dcc.Graph(id='graph-by-clinica', figure=fig_by_clinica if fig_by_clinica is not None else {}))]), md=4),
            dbc.Col(dbc.Card([dbc.CardHeader("Distribuição de Idades"), dbc.CardBody(dcc.Graph(id='graph-age-hist', figure=fig_age_hist if fig_age_hist is not None else {}))]), md=4),
        ], className='mb-3'),

        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader("Heatmap: Hora x Dia"), dbc.CardBody(dcc.Graph(id='graph-heatmap', figure=fig_heatmap if fig_heatmap is not None else {}))]), md=6),
            dbc.Col(dbc.Card([dbc.CardHeader("Boxplot: Idades por Médico"), dbc.CardBody(dcc.Graph(id='graph-box-age', figure=fig_box_cons_med if fig_box_cons_med is not None else {}))]), md=6),
        ], className='mb-3'),

        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader("Scatter: Consultas por Médico"), dbc.CardBody(dcc.Graph(id='graph-scatter-med', figure=fig_scatter_med if fig_scatter_med is not None else {}))]), md=12),
        ], className='mb-3'),

        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H5("Consultas Não Triviais Implementadas:", className="alert-heading"),
                    html.Hr(),
                    html.P("1. Total de consultas por especialidade médica (agregação + JOIN)"),
                    html.P("2. Próximas consultas com dados completos (múltiplos JOINs + filtro temporal)"),
                    html.P("3. Vários gráficos: série temporal, barras, pizza, área, heatmap, histogramas, boxplot e scatter."),
                ], color="info")
            ])
        ])
    ], fluid=True)

    return layout


def register_callbacks(app):
    @app.callback(
        Output('graph-timeseries', 'figure'),
        Output('graph-by-medico', 'figure'),
        Output('graph-gender', 'figure'),
        Output('graph-by-clinica', 'figure'),
        Output('graph-heatmap', 'figure'),
        Output('graph-age-hist', 'figure'),
        Output('graph-box-age', 'figure'),
        Output('graph-scatter-med', 'figure'),
        Output('graph-especialidades', 'figure'),
        Output('proximas-table', 'children'),
        Input('filter-clinica', 'value'),
        Input('filter-medico', 'value'),
        Input('filter-periodo', 'start_date'),
        Input('filter-periodo', 'end_date')
    )
    def update_all(clinica, medico, start_date, end_date):
        # monta query com filtros
        sql = ("SELECT c.CodCli, c.CodMed, c.CpfPaciente, c.Data_Hora, cl.NomeCli, m.NomeMed, "
               "p.NomePac, p.DataNascimento, p.Genero as GeneroPac, m.Genero as GeneroMed, m.Especialidade "
               "FROM tabelaconsulta c "
               "JOIN tabelaclinica cl ON c.CodCli=cl.CodCli "
               "JOIN tabelamedico m ON c.CodMed=m.CodMed "
               "JOIN tabelapaciente p ON c.CpfPaciente=p.CpfPaciente "
               "WHERE 1=1 ")
        params = []
        if clinica:
            sql += ' AND c.CodCli = %s'
            params.append(clinica)
        if medico:
            sql += ' AND c.CodMed = %s'
            params.append(medico)
        if start_date:
            sql += ' AND c.Data_Hora >= %s'
            params.append(start_date)
        if end_date:
            sql += ' AND c.Data_Hora <= %s'
            params.append(end_date)

        # limite para evitar grandes cargas (ajustável)
        rows = db.fetch_all_paginated(sql + ' ORDER BY c.Data_Hora', params, limit=5000)
        df = pd.DataFrame(rows) if rows else pd.DataFrame()

        # prepara figuras vazias padrão
        empty_fig = {}
        fig_timeseries = empty_fig
        fig_by_medico = empty_fig
        fig_gender = empty_fig
        fig_by_clinica = empty_fig
        fig_heatmap = empty_fig
        fig_age_hist = empty_fig
        fig_box = empty_fig
        fig_scatter = empty_fig
        fig_especial = empty_fig

        if not df.empty:
            try:
                df['Data_Hora'] = pd.to_datetime(df['Data_Hora'])
            except Exception:
                df['Data_Hora'] = pd.to_datetime(df['Data_Hora'], errors='coerce')
            df['date'] = df['Data_Hora'].dt.date
            df['hour'] = df['Data_Hora'].dt.hour
            df['weekday'] = df['Data_Hora'].dt.day_name()

            # idade
            def compute_age(dob):
                try:
                    d = pd.to_datetime(dob)
                    today = pd.Timestamp.now()
                    return int((today - d).days / 365.25)
                except Exception:
                    return None

            if 'DataNascimento' in df.columns:
                df['age'] = df['DataNascimento'].apply(compute_age)

            # timeseries
            ts = df.groupby('date').size().reset_index(name='count')
            fig_timeseries = px.line(ts, x='date', y='count', title='Consultas por Dia')

            # by medico
            by_med = df.groupby('NomeMed').size().reset_index(name='count').sort_values('count', ascending=False)
            fig_by_medico = px.bar(by_med.head(12), x='NomeMed', y='count', title='Consultas por Médico')

            # genero
            if 'GeneroPac' in df.columns:
                gender = df['GeneroPac'].fillna('Desconhecido').value_counts().reset_index()
                gender.columns = ['Genero', 'count']
                fig_gender = px.pie(gender, names='Genero', values='count', title='Distribuição por Gênero (Pacientes)')

            # by clinica
            by_cli = df.groupby('NomeCli').size().reset_index(name='count').sort_values('count', ascending=False)
            fig_by_clinica = px.area(by_cli, x='NomeCli', y='count', title='Consultas por Clínica')

            # heatmap
            heat = df.groupby(['weekday', 'hour']).size().reset_index(name='count')
            heat_pivot = heat.pivot(index='hour', columns='weekday', values='count').fillna(0)
            weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            cols = [c for c in weekdays if c in heat_pivot.columns]
            if not heat_pivot.empty:
                fig_heatmap = go.Figure(data=go.Heatmap(z=heat_pivot[cols].values, x=cols, y=heat_pivot.index, colorscale='Viridis'))
                fig_heatmap.update_layout(title='Heatmap: Hora do Dia x Dia da Semana')

            # ages
            if 'age' in df.columns and df['age'].notnull().any():
                fig_age_hist = px.histogram(df, x='age', nbins=12, title='Distribuição de Idades dos Pacientes')
                fig_box = px.box(df, x='NomeMed', y='age', title='Boxplot: Idades por Médico')

            # scatter
            fig_scatter = px.scatter(by_med.head(50), x='NomeMed', y='count', size='count', title='Consultas por Médico (scatter)')

            # especialidades
            espec = df.groupby('Especialidade').size().reset_index(name='count').sort_values('count', ascending=False)
            if not espec.empty:
                fig_especial = px.bar(espec, x='Especialidade', y='count', title='Consultas por Especialidade')

        # proximas consultas (aplicar filtros clín/med se fornecidos)
        prox_sql = ("SELECT c.Data_Hora, p.NomePac, m.NomeMed, cl.NomeCli "
                    "FROM tabelaconsulta c "
                    "JOIN tabelapaciente p ON c.CpfPaciente = p.CpfPaciente "
                    "JOIN tabelamedico m ON c.CodMed = m.CodMed "
                    "JOIN tabelaclinica cl ON c.CodCli = cl.CodCli "
                    "WHERE c.Data_Hora >= NOW() ")
        prox_params = []
        if clinica:
            prox_sql += ' AND c.CodCli = %s'
            prox_params.append(clinica)
        if medico:
            prox_sql += ' AND c.CodMed = %s'
            prox_params.append(medico)
        prox_rows = db.fetch_all_paginated(prox_sql + ' ORDER BY c.Data_Hora', prox_params, limit=5)
        proximas_div = None
        if prox_rows:
            proximas_div = dbc.Table.from_dataframe(pd.DataFrame(prox_rows), striped=True, bordered=True, hover=True, responsive=True)
        else:
            proximas_div = html.P('Nenhuma consulta agendada', className='text-muted')

        return fig_timeseries, fig_by_medico, fig_gender, fig_by_clinica, fig_heatmap, fig_age_hist, fig_box, fig_scatter, fig_especial, proximas_div

    @app.callback(
        Output('filter-clinica', 'options'),
        Output('filter-medico', 'options'),
        Input('url', 'pathname')
    )
    def populate_filters(_pathname):
        # busca clinicas e medicos para popular selects
        clinicas = db.get_clinicas() or []
        medicos = db.get_medicos() or []
        cli_opts = [{'label': 'Todas', 'value': ''}] + [{'label': c.get('NomeCli') or str(c.get('CodCli')), 'value': c.get('CodCli')} for c in clinicas]
        med_opts = [{'label': 'Todos', 'value': ''}] + [{'label': m.get('NomeMed'), 'value': m.get('CodMed')} for m in medicos]
        return cli_opts, med_opts
