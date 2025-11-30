# -*- coding: utf-8 -*-
from dash import html, dcc, callback, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
from db import db, logger
import pandas as pd
from datetime import datetime, timedelta


def build_layout():
    """Constrói o layout do dashboard principal"""
    if not db.ensure_connected():
        return dbc.Container([
            dbc.Alert([
                html.H4("⚠️ Sem conexão com o banco de dados", className="alert-heading"),
                html.P("Não foi possível conectar. Verifique as configurações em .env"),
            ], color="danger")
        ], fluid=True)

    # KPIs principais
    stats = {
        'pacientes': db.fetch_one("SELECT COUNT(*) as total FROM tabelapaciente")['total'],
        'medicos': db.fetch_one("SELECT COUNT(*) as total FROM tabelamedico")['total'],
        'clinicas': db.fetch_one("SELECT COUNT(*) as total FROM tabelaclinica")['total'],
        'consultas': db.fetch_one("SELECT COUNT(*) as total FROM tabelaconsulta")['total']
    }

    # Consultas hoje (compatível com SQLite e MySQL)
    hoje = datetime.now().date()
    if db.use_sqlite:
        consultas_hoje = db.fetch_one(
            "SELECT COUNT(*) as total FROM tabelaconsulta WHERE DATE(Data_Hora) = DATE('now')"
        )['total']
    else:
        consultas_hoje = db.fetch_one(
            "SELECT COUNT(*) as total FROM tabelaconsulta WHERE DATE(Data_Hora) = CURDATE()"
        )['total']

    # Próximas 5 consultas (compatível com SQLite e MySQL)
    if db.use_sqlite:
        proximas = db.fetch_all("""
            SELECT 
                c.Data_Hora,
                p.NomePac,
                m.NomeMed,
                m.Especialidade,
                cl.NomeCli
            FROM tabelaconsulta c
            JOIN tabelapaciente p ON c.CpfPaciente = p.CpfPaciente
            JOIN tabelamedico m ON c.CodMed = m.CodMed
            JOIN tabelaclinica cl ON c.CodCli = cl.CodCli
            WHERE c.Data_Hora >= datetime('now')
            ORDER BY c.Data_Hora
            LIMIT 5
        """)
    else:
        proximas = db.fetch_all("""
            SELECT 
                c.Data_Hora,
                p.NomePac,
                m.NomeMed,
                m.Especialidade,
                cl.NomeCli
            FROM tabelaconsulta c
            JOIN tabelapaciente p ON c.CpfPaciente = p.CpfPaciente
            JOIN tabelamedico m ON c.CodMed = m.CodMed
            JOIN tabelaclinica cl ON c.CodCli = cl.CodCli
            WHERE c.Data_Hora >= NOW()
            ORDER BY c.Data_Hora
            LIMIT 5
        """)

    # Top 5 médicos com mais consultas
    top_medicos = db.fetch_all("""
        SELECT 
            m.NomeMed,
            m.Especialidade,
            COUNT(*) as total_consultas
        FROM tabelaconsulta c
        JOIN tabelamedico m ON c.CodMed = m.CodMed
        GROUP BY m.CodMed, m.NomeMed, m.Especialidade
        ORDER BY total_consultas DESC
        LIMIT 5
    """)

    # Consultas por especialidade (para gráfico)
    por_especialidade = db.fetch_all("""
        SELECT 
            m.Especialidade,
            COUNT(*) as total
        FROM tabelaconsulta c
        JOIN tabelamedico m ON c.CodMed = m.CodMed
        GROUP BY m.Especialidade
        ORDER BY total DESC
        LIMIT 10
    """)

    # Consultas nos últimos 30 dias (série temporal)
    # Query compatível com SQLite e MySQL
    if db.use_sqlite:
        ultimos_30_dias = db.fetch_all("""
            SELECT 
                DATE(Data_Hora) as data,
                COUNT(*) as total
            FROM tabelaconsulta
            WHERE Data_Hora >= datetime('now', '-30 days')
            GROUP BY DATE(Data_Hora)
            ORDER BY data
        """)
    else:
        ultimos_30_dias = db.fetch_all("""
            SELECT 
                DATE(Data_Hora) as data,
                COUNT(*) as total
            FROM tabelaconsulta
            WHERE Data_Hora >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            GROUP BY DATE(Data_Hora)
            ORDER BY data
        """)

    # Gráfico de especialidades
    fig_especialidades = go.Figure()
    if por_especialidade:
        fig_especialidades = px.bar(
            pd.DataFrame(por_especialidade),
            x='Especialidade',
            y='total',
            title='Consultas por Especialidade',
            color='total',
            color_continuous_scale='Blues'
        )
        fig_especialidades.update_layout(
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )

    # Gráfico temporal
    fig_timeline = go.Figure()
    if ultimos_30_dias:
        df_timeline = pd.DataFrame(ultimos_30_dias)
        fig_timeline = px.area(
            df_timeline,
            x='data',
            y='total',
            title='Consultas nos Últimos 30 Dias',
            color_discrete_sequence=['#0d6efd']
        )
        fig_timeline.update_layout(
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )

    layout = dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2("📊 Dashboard - Consultório Médico", className="mb-0"),
                html.P(f"Bem-vindo! Hoje é {datetime.now().strftime('%d/%m/%Y')}", 
                       className="text-muted mb-0")
            ], md=8),
            dbc.Col([
                html.Div([
                    dbc.Badge(f"🕐 {consultas_hoje} consultas hoje", 
                             color="success", className="fs-6 px-3 py-2")
                ], className="text-end")
            ], md=4)
        ], className="mb-4 align-items-center"),

        # KPI Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Div("👥", className="fs-1"),
                            html.Div([
                                html.H3(f"{stats['pacientes']}", className="mb-0"),
                                html.P("Pacientes", className="text-muted mb-0")
                            ])
                        ], className="d-flex justify-content-between align-items-center")
                    ])
                ], className="shadow-sm border-0 h-100", style={"borderLeft": "4px solid #0d6efd"})
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Div("⚕️", className="fs-1"),
                            html.Div([
                                html.H3(f"{stats['medicos']}", className="mb-0"),
                                html.P("Médicos", className="text-muted mb-0")
                            ])
                        ], className="d-flex justify-content-between align-items-center")
                    ])
                ], className="shadow-sm border-0 h-100", style={"borderLeft": "4px solid #198754"})
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Div("🏥", className="fs-1"),
                            html.Div([
                                html.H3(f"{stats['clinicas']}", className="mb-0"),
                                html.P("Clínicas", className="text-muted mb-0")
                            ])
                        ], className="d-flex justify-content-between align-items-center")
                    ])
                ], className="shadow-sm border-0 h-100", style={"borderLeft": "4px solid #0dcaf0"})
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Div("📅", className="fs-1"),
                            html.Div([
                                html.H3(f"{stats['consultas']}", className="mb-0"),
                                html.P("Consultas", className="text-muted mb-0")
                            ])
                        ], className="d-flex justify-content-between align-items-center")
                    ])
                ], className="shadow-sm border-0 h-100", style={"borderLeft": "4px solid #ffc107"})
            ], md=3),
        ], className="mb-4 g-3"),

        # Seção de Ações Rápidas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("⚡ Ações Rápidas", className="mb-0")
                    ]),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Button([
                                    html.I(className="bi bi-person-plus me-2"),
                                    "Novo Paciente"
                                ], href="/pacientes", color="primary", className="w-100")
                            ], md=3),
                            dbc.Col([
                                dbc.Button([
                                    html.I(className="bi bi-calendar-plus me-2"),
                                    "Nova Consulta"
                                ], href="/consultas", color="success", className="w-100")
                            ], md=3),
                            dbc.Col([
                                dbc.Button([
                                    html.I(className="bi bi-hospital me-2"),
                                    "Nova Clínica"
                                ], href="/clinicas", color="info", className="w-100")
                            ], md=3),
                            dbc.Col([
                                dbc.Button([
                                    html.I(className="bi bi-graph-up me-2"),
                                    "Ver Analytics"
                                ], href="/analytics", color="warning", className="w-100")
                            ], md=3),
                        ], className="g-2")
                    ])
                ], className="shadow-sm border-0")
            ])
        ], className="mb-4"),

        # Gráficos e Informações
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📈 Consultas nos Últimos 30 Dias", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(figure=fig_timeline, config={'displayModeBar': False})
                    ])
                ], className="shadow-sm border-0")
            ], md=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🏆 Top 5 Médicos", className="mb-0")),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Strong(f"{i+1}. {m['NomeMed']}", className="d-block"),
                                    html.Small(f"{m['Especialidade']} • {m['total_consultas']} consultas", 
                                             className="text-muted")
                                ], className="mb-3") for i, m in enumerate(top_medicos)
                            ]) if top_medicos else html.P("Nenhum dado disponível", className="text-muted")
                        ])
                    ])
                ], className="shadow-sm border-0")
            ], md=4),
        ], className="mb-4 g-3"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📊 Distribuição por Especialidade", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(figure=fig_especialidades, config={'displayModeBar': False})
                    ])
                ], className="shadow-sm border-0")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🕐 Próximas Consultas", className="mb-0")),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                dbc.ListGroupItem([
                                    html.Div([
                                        html.Strong(c['NomePac']),
                                        html.Span(" • ", className="text-muted"),
                                        html.Span(c['NomeMed'], className="text-primary"),
                                    ]),
                                    html.Small([
                                        html.Span(c['Especialidade'], className="badge bg-secondary me-2"),
                                        html.Span(f"📍 {c['NomeCli']}", className="text-muted me-2"),
                                        html.Span(
                                            datetime.strptime(str(c['Data_Hora']), '%Y-%m-%d %H:%M:%S').strftime('%d/%m às %H:%M') 
                                            if isinstance(c['Data_Hora'], str) 
                                            else c['Data_Hora'].strftime('%d/%m às %H:%M'),
                                            className="text-info"
                                        )
                                    ], className="d-block mt-1")
                                ], className="border-0 px-0 py-2") for c in proximas
                            ]) if proximas else html.P("Nenhuma consulta agendada", className="text-muted")
                        ], style={"maxHeight": "300px", "overflowY": "auto"})
                    ])
                ], className="shadow-sm border-0")
            ], md=6),
        ], className="mb-4 g-3"),

    ], fluid=True)

    return layout


def register_callbacks(app):
    """Registra callbacks se necessário"""
    pass
