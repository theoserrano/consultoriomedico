# -*- coding: utf-8 -*-
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
from db import db
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("consultorio.analytics")

# Cache simples para dados
_cache = {
    'data': None,
    'timestamp': None,
    'ttl': 300  # 5 minutos
}


def build_layout():
    """Constrói o layout da página de Analytics"""
    if not db.ensure_connected():
        return dbc.Container([
            dbc.Alert([
                html.H4("⚠️ Sem conexão com o banco de dados", className="alert-heading"),
                html.P("Não foi possível conectar. Verifique as configurações em .env"),
            ], color="danger")
        ], fluid=True)

    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2("📊 Analytics & Relatórios Avançados", className="mb-0"),
                html.P("Visualizações detalhadas e análises de dados", className="text-muted")
            ])
        ], className="mb-4"),

        # Filtros interativos
        dbc.Card([
            dbc.CardHeader([
                html.H5("🔍 Filtros", className="mb-0")
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Clínica"),
                        dcc.Dropdown(
                            id='analytics-filter-clinica',
                            options=[{'label': 'Todas', 'value': ''}],
                            value='',
                            clearable=False,
                            className='analytics-dropdown',
                            style={'zIndex': 'auto'}
                        )
                    ], md=3, style={'zIndex': 1050, 'position': 'relative'}),
                    dbc.Col([
                        dbc.Label("Médico"),
                        dcc.Dropdown(
                            id='analytics-filter-medico',
                            options=[{'label': 'Todos', 'value': ''}],
                            value='',
                            clearable=False,
                            className='analytics-dropdown',
                            style={'zIndex': 'auto'}
                        )
                    ], md=3, style={'zIndex': 1050, 'position': 'relative'}),
                    dbc.Col([
                        dbc.Label("Período"),
                        dcc.DatePickerRange(
                            id='analytics-filter-periodo',
                            start_date=None,
                            end_date=None,
                            display_format='DD/MM/YYYY',
                            className="w-100",
                            style={'zIndex': 10000}
                        )
                    ], md=4, style={'zIndex': 1050, 'position': 'relative'}),
                    dbc.Col([
                        dbc.Label("⠀"),
                        dbc.Button("Aplicar Filtros", id="analytics-btn-apply", color="primary", className="w-100")
                    ], md=2),
                ], className="g-2")
            ])
        ], className="mb-4 shadow-sm border-0", style={'zIndex': 1050, 'position': 'relative'}),

        # Loading indicator
        dcc.Loading(
            id="analytics-loading",
            type="default",
            children=[
                html.Div(id="analytics-content", children=[
        # Gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📈 Série Temporal - Consultas por Dia", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            id='analytics-graph-timeseries',
                            figure=go.Figure().update_layout(
                                title="Clique em 'Aplicar Filtros' para carregar os dados",
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False),
                                annotations=[dict(text="Aguardando filtros...", showarrow=False, font=dict(size=16))]
                            ),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm border-0", style={'zIndex': 1, 'position': 'relative'})
            ], md=12),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("👨‍⚕️ Consultas por Médico", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            id='analytics-graph-by-medico',
                            figure=go.Figure().update_layout(
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False)
                            ),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm border-0", style={'zIndex': 1, 'position': 'relative'})
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🏥 Consultas por Clínica", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            id='analytics-graph-by-clinica',
                            figure=go.Figure().update_layout(
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False)
                            ),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm border-0", style={'zIndex': 1, 'position': 'relative'})
            ], md=6),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("👤 Distribuição por Gênero", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            id='analytics-graph-gender',
                            figure=go.Figure().update_layout(
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False)
                            ),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm border-0", style={'zIndex': 1, 'position': 'relative'})
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📊 Distribuição de Idades", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            id='analytics-graph-age-hist',
                            figure=go.Figure().update_layout(
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False)
                            ),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm border-0", style={'zIndex': 1, 'position': 'relative'})
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🔢 Boxplot: Idades por Médico", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            id='analytics-graph-box-age',
                            figure=go.Figure().update_layout(
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False)
                            ),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm border-0", style={'zIndex': 1, 'position': 'relative'})
            ], md=4),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🔥 Heatmap: Hora do Dia x Dia da Semana", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            id='analytics-graph-heatmap',
                            figure=go.Figure().update_layout(
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False)
                            ),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm border-0", style={'zIndex': 1, 'position': 'relative'})
            ], md=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("⭐ Scatter: Consultas por Médico", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            id='analytics-graph-scatter',
                            figure=go.Figure().update_layout(
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False)
                            ),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm border-0", style={'zIndex': 1, 'position': 'relative'})
            ], md=4),
        ], className="mb-3"),
                ])
            ]
        ),

    ], fluid=True)


# Callback será o mesmo que o antigo, mas agora separado nesta página
def register_callbacks(app):
    @app.callback(
        Output('analytics-graph-timeseries', 'figure'),
        Output('analytics-graph-by-medico', 'figure'),
        Output('analytics-graph-gender', 'figure'),
        Output('analytics-graph-by-clinica', 'figure'),
        Output('analytics-graph-heatmap', 'figure'),
        Output('analytics-graph-age-hist', 'figure'),
        Output('analytics-graph-box-age', 'figure'),
        Output('analytics-graph-scatter', 'figure'),
        Input('analytics-btn-apply', 'n_clicks'),
        State('analytics-filter-clinica', 'value'),
        State('analytics-filter-medico', 'value'),
        State('analytics-filter-periodo', 'start_date'),
        State('analytics-filter-periodo', 'end_date'),
        prevent_initial_call=True
    )
    def update_all(n_clicks, clinica, medico, start_date, end_date):
        # Verifica cache
        cache_key = f"{clinica}_{medico}_{start_date}_{end_date}"
        now = datetime.now()
        
        if (_cache['data'] is not None and 
            _cache['timestamp'] and 
            (now - _cache['timestamp']).seconds < _cache['ttl'] and
            _cache.get('key') == cache_key):
            logger.info("Usando dados em cache")
            df = _cache['data']
        else:
            # Monta query otimizada com filtros
            # Se não houver filtros de data, limita aos últimos 90 dias por padrão
            if not start_date and not end_date:
                default_start = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
                start_date = default_start
                logger.info(f"Aplicando filtro padrão: últimos 90 dias desde {start_date}")
            
            # Query otimizada: seleciona apenas colunas necessárias
            sql = ("SELECT c.CodCli, c.CodMed, c.CpfPaciente, c.Data_Hora, "
                   "cl.NomeCli, m.NomeMed, p.DataNascimento, p.Genero as GeneroPac "
                   "FROM tabelaconsulta c "
                   "INNER JOIN tabelaclinica cl ON c.CodCli=cl.CodCli "
                   "INNER JOIN tabelamedico m ON c.CodMed=m.CodMed "
                   "INNER JOIN tabelapaciente p ON c.CpfPaciente=p.CpfPaciente "
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

            # Busca dados com limite
            logger.info(f"Buscando dados com filtros: clinica={clinica}, medico={medico}, período={start_date} a {end_date}")
            rows = db.fetch_all_paginated(sql + ' ORDER BY c.Data_Hora DESC', params, limit=5000)
            df = pd.DataFrame(rows) if rows else pd.DataFrame()
            
            # Atualiza cache
            _cache['data'] = df
            _cache['timestamp'] = now
            _cache['key'] = cache_key
            logger.info(f"Cache atualizado com {len(df)} registros")

        # Figuras vazias por padrão
        empty_fig = go.Figure().update_layout(
            title="Sem dados para exibir",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(text="Nenhum dado disponível", showarrow=False, font=dict(size=20))]
        )
        
        fig_timeseries = empty_fig
        fig_by_medico = empty_fig
        fig_gender = empty_fig
        fig_by_clinica = empty_fig
        fig_heatmap = empty_fig
        fig_age_hist = empty_fig
        fig_box = empty_fig
        fig_scatter = empty_fig

        if not df.empty:
            try:
                df['Data_Hora'] = pd.to_datetime(df['Data_Hora'])
            except Exception:
                df['Data_Hora'] = pd.to_datetime(df['Data_Hora'], errors='coerce')
            
            df['date'] = df['Data_Hora'].dt.date
            df['hour'] = df['Data_Hora'].dt.hour
            df['weekday'] = df['Data_Hora'].dt.day_name()

            # Idade
            def compute_age(dob):
                try:
                    d = pd.to_datetime(dob)
                    today = pd.Timestamp.now()
                    return int((today - d).days / 365.25)
                except Exception:
                    return None

            if 'DataNascimento' in df.columns:
                df['age'] = df['DataNascimento'].apply(compute_age)

            # Série temporal
            ts = df.groupby('date').size().reset_index(name='count')
            fig_timeseries = px.line(
                ts, x='date', y='count',
                title='Evolução Temporal de Consultas',
                labels={'date': 'Data', 'count': 'Número de Consultas'}
            )
            fig_timeseries.update_traces(line_color='#0d6efd', line_width=3)

            # Por médico
            by_med = df.groupby('NomeMed').size().reset_index(name='count').sort_values('count', ascending=False).head(15)
            fig_by_medico = px.bar(
                by_med, x='NomeMed', y='count',
                title='Top 15 Médicos com Mais Consultas',
                labels={'NomeMed': 'Médico', 'count': 'Consultas'},
                color='count',
                color_continuous_scale='Blues'
            )

            # Gênero
            if 'GeneroPac' in df.columns:
                gender = df['GeneroPac'].fillna('Desconhecido').value_counts().reset_index()
                gender.columns = ['Genero', 'count']
                fig_gender = px.pie(
                    gender, names='Genero', values='count',
                    title='Distribuição por Gênero',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )

            # Por clínica
            by_cli = df.groupby('NomeCli').size().reset_index(name='count').sort_values('count', ascending=False)
            fig_by_clinica = px.bar(
                by_cli, x='NomeCli', y='count',
                title='Consultas por Clínica',
                labels={'NomeCli': 'Clínica', 'count': 'Consultas'},
                color='count',
                color_continuous_scale='Greens'
            )

            # Heatmap
            heat = df.groupby(['weekday', 'hour']).size().reset_index(name='count')
            heat_pivot = heat.pivot(index='hour', columns='weekday', values='count').fillna(0)
            weekdays_pt = {'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
                          'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
            weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            cols = [c for c in weekdays if c in heat_pivot.columns]
            if not heat_pivot.empty and cols:
                fig_heatmap = go.Figure(data=go.Heatmap(
                    z=heat_pivot[cols].values,
                    x=[weekdays_pt.get(c, c) for c in cols],
                    y=heat_pivot.index,
                    colorscale='Viridis',
                    colorbar=dict(title="Consultas")
                ))
                fig_heatmap.update_layout(
                    title='Padrão de Horários: Dia da Semana vs Hora',
                    xaxis_title='Dia da Semana',
                    yaxis_title='Hora do Dia'
                )

            # Idades
            if 'age' in df.columns and df['age'].notnull().any():
                fig_age_hist = px.histogram(
                    df, x='age', nbins=20,
                    title='Distribuição de Idades dos Pacientes',
                    labels={'age': 'Idade'},
                    color_discrete_sequence=['#17a2b8']
                )
                
                # Boxplot por médico (top 10)
                top_10_med = by_med.head(10)['NomeMed'].tolist()
                df_top = df[df['NomeMed'].isin(top_10_med)]
                fig_box = px.box(
                    df_top, x='NomeMed', y='age',
                    title='Distribuição de Idades por Médico (Top 10)',
                    labels={'NomeMed': 'Médico', 'age': 'Idade'},
                    color='NomeMed'
                )
                fig_box.update_layout(showlegend=False)

            # Scatter
            fig_scatter = px.scatter(
                by_med.head(30), x='NomeMed', y='count', size='count',
                title='Dispersão de Consultas por Médico',
                labels={'NomeMed': 'Médico', 'count': 'Consultas'},
                color='count',
                color_continuous_scale='Sunset'
            )

        return fig_timeseries, fig_by_medico, fig_gender, fig_by_clinica, fig_heatmap, fig_age_hist, fig_box, fig_scatter

    @app.callback(
        Output('analytics-filter-clinica', 'options'),
        Output('analytics-filter-medico', 'options'),
        Input('url', 'pathname'),
        prevent_initial_call=False
    )
    def populate_filters(_pathname):
        clinicas = db.get_clinicas() or []
        medicos = db.get_medicos() or []
        cli_opts = [{'label': 'Todas', 'value': ''}] + [
            {'label': c.get('NomeCli') or str(c.get('CodCli')), 'value': c.get('CodCli')} for c in clinicas
        ]
        med_opts = [{'label': 'Todos', 'value': ''}] + [
            {'label': m.get('NomeMed'), 'value': m.get('CodMed')} for m in medicos
        ]
        return cli_opts, med_opts


layout = build_layout()
