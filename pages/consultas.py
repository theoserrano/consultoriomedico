# -*- coding: utf-8 -*-
from dash import html, dcc, callback, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
from db import db
from datetime import datetime
import json

layout = dbc.Container([
    html.H2("Gerenciamento de Consultas", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Button("➕ Nova Consulta", id="btn-nova-consulta", color="warning", className="mb-3")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Label("Filtrar por Data Inicial:"),
            dbc.Input(id="filtro-data-inicio", type="date", className="mb-2")
        ], md=3),
        dbc.Col([
            dbc.Label("Data Final:"),
            dbc.Input(id="filtro-data-fim", type="date", className="mb-2")
        ], md=3),
        dbc.Col([
            dbc.Label("Filtrar por Médico:"),
            dcc.Dropdown(id="filtro-medico-cons", placeholder="Selecione...", className="mb-2")
        ], md=3),
        dbc.Col([
            dbc.Label("\u2800"),
            dbc.Button("Aplicar Filtros", id="btn-aplicar-filtros", color="secondary", className="w-100")
        ], md=3)
    ], className="mb-3"),
    
    html.Div(id="tabela-consultas"),
    
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id="modal-consulta-titulo")),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Clínica *"),
                        dcc.Dropdown(id="input-clinica-cons", placeholder="Selecione a clínica")
                    ], md=4),
                    dbc.Col([
                        dbc.Label("Médico *"),
                        dcc.Dropdown(id="input-medico-cons", placeholder="Selecione o médico")
                    ], md=4),
                    dbc.Col([
                        dbc.Label("Paciente *"),
                        dcc.Dropdown(id="input-paciente-cons", placeholder="Selecione o paciente")
                    ], md=4)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Data *"),
                        dbc.Input(id="input-data-cons", type="date", required=True)
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Hora *"),
                        dbc.Input(id="input-hora-cons", type="time", required=True)
                    ], md=6)
                ])
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Salvar", id="btn-salvar-consulta", color="warning"),
            dbc.Button("Cancelar", id="btn-fechar-modal-consulta", color="secondary")
        ])
    ], id="modal-consulta", size="lg", is_open=False),
    
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Confirmar Exclusão")),
        dbc.ModalBody("Tem certeza que deseja excluir esta consulta?"),
        dbc.ModalFooter([
            dbc.Button("Confirmar", id="btn-confirmar-delete-cons", color="danger"),
            dbc.Button("Cancelar", id="btn-cancelar-delete-cons", color="secondary")
        ])
    ], id="modal-delete-consulta", is_open=False),
    
    # Modal para avisos dos triggers
    dbc.Modal([
        dbc.ModalHeader([
            html.I(className="bi bi-exclamation-triangle-fill text-warning me-2"),
            "Regra de Negócio Violada"
        ], close_button=True),
        dbc.ModalBody([
            html.Div(id="modal-trigger-content", className="text-center py-4")
        ]),
        dbc.ModalFooter([
            dbc.Button("Entendi", id="btn-fechar-modal-trigger", color="warning", className="w-100")
        ])
    ], id="modal-trigger-aviso", is_open=False, centered=True, size="lg"),
    
    dcc.Store(id='store-consulta-acao'),
    dcc.Store(id='store-consulta-delete'),
    dcc.Store(id='store-refresh-trigger-cons', data=0),
    html.Div(id="alert-consulta")
], fluid=True)

@callback(
    Output("tabela-consultas", "children"),
    Output("filtro-medico-cons", "options"),
    Input("btn-aplicar-filtros", "n_clicks"),
    Input("store-refresh-trigger-cons", "data"),
    State("filtro-data-inicio", "value"),
    State("filtro-data-fim", "value"),
    State("filtro-medico-cons", "value")
)
def atualizar_tabela(apply_click, refresh_trigger, data_ini, data_fim, medico_filtro):
    # proteção: se sem conexão, retornar alerta e opções vazias
    if not db.ensure_connected():
        return dbc.Alert("Sem conexão com o banco de dados. Verifique o arquivo .env e o serviço MySQL.", color="danger"), []

    query = """
    SELECT 
        c.CodCli, c.CodMed, c.CpfPaciente, c.Data_Hora,
        cl.NomeCli, m.NomeMed, p.NomePac
    FROM tabelaconsulta c
    JOIN tabelaclinica cl ON c.CodCli = cl.CodCli
    JOIN tabelamedico m ON c.CodMed = m.CodMed
    JOIN tabelapaciente p ON c.CpfPaciente = p.CpfPaciente
    WHERE 1=1
    """
    params = []
    
    if data_ini:
        query += " AND DATE(c.Data_Hora) >= %s"
        params.append(data_ini)
    
    if data_fim:
        query += " AND DATE(c.Data_Hora) <= %s"
        params.append(data_fim)
    
    if medico_filtro:
        query += " AND c.CodMed = %s"
        params.append(medico_filtro)
    
    query += " ORDER BY c.Data_Hora DESC"
    
    consultas = db.fetch_all(query, tuple(params) if params else None)
    
    medicos = db.fetch_all("SELECT CodMed, NomeMed FROM tabelamedico")
    medico_options = [{"label": f"{m['CodMed']} - {m['NomeMed']}", "value": m['CodMed']} for m in medicos]
    
    if not consultas:
        return dbc.Alert("Nenhuma consulta encontrada", color="info"), medico_options
    
    df = pd.DataFrame(consultas)
    
    table_header = [html.Thead(html.Tr([
        html.Th("Data/Hora"), html.Th("Paciente"), html.Th("Médico"),
        html.Th("Clínica"), html.Th("Ações")
    ]))]
    
    rows = []
    for _, row in df.iterrows():
        data_hora_str = row['Data_Hora'].strftime('%d/%m/%Y %H:%M') if isinstance(row['Data_Hora'], datetime) else str(row['Data_Hora'])
        
        rows.append(html.Tr([
            html.Td(data_hora_str),
            html.Td(row['NomePac']),
            html.Td(row['NomeMed']),
            html.Td(row['NomeCli']),
            html.Td([
                dbc.Button("\U0001f5d1\ufe0f", 
                          id={'type': 'btn-delete-cons', 
                              'index': f"{row['CodCli']}|{row['CodMed']}|{row['CpfPaciente']}|{row['Data_Hora']}"}, 
                          color="danger", size="sm")
            ])
        ]))
    
    table_body = [html.Tbody(rows)]
    return dbc.Table(table_header + table_body, bordered=True, hover=True, responsive=True, striped=True), medico_options

@callback(
    Output("modal-consulta", "is_open"),
    Output("modal-consulta-titulo", "children"),
    Output("store-consulta-acao", "data"),
    Output("input-clinica-cons", "options"),
    Output("input-medico-cons", "options"),
    Output("input-paciente-cons", "options"),
    Output("input-clinica-cons", "value"),
    Output("input-medico-cons", "value"),
    Output("input-paciente-cons", "value"),
    Output("input-data-cons", "value"),
    Output("input-hora-cons", "value"),
    Input("btn-nova-consulta", "n_clicks"),
    Input("btn-fechar-modal-consulta", "n_clicks"),
    prevent_initial_call=True
)
def toggle_modal(novo_click, fechar_click):
    ctx = callback_context
    
    if not ctx.triggered:
        return False, "", None, [], [], [], None, None, None, "", ""

    triggered = ctx.triggered[0]
    if triggered.get('value') in (None, 0, False, ''):
        return False, "", None, [], [], [], None, None, None, "", ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    clinicas = db.fetch_all("SELECT CodCli, NomeCli FROM tabelaclinica")
    medicos = db.fetch_all("SELECT CodMed, NomeMed FROM tabelamedico")
    pacientes = db.fetch_all("SELECT CpfPaciente, NomePac FROM tabelapaciente")
    
    cli_opts = [{"label": f"{c['CodCli']} - {c['NomeCli']}", "value": c['CodCli']} for c in clinicas]
    med_opts = [{"label": f"{m['CodMed']} - {m['NomeMed']}", "value": m['CodMed']} for m in medicos]
    pac_opts = [{"label": f"{p['CpfPaciente']} - {p['NomePac']}", "value": p['CpfPaciente']} for p in pacientes]
    
    if "btn-nova-consulta" in trigger_id:
        return True, "Nova Consulta", "create", cli_opts, med_opts, pac_opts, None, None, None, "", ""
    
    if "btn-fechar-modal-consulta" in trigger_id:
        return False, "", None, cli_opts, med_opts, pac_opts, None, None, None, "", ""
    
    return False, "", None, cli_opts, med_opts, pac_opts, None, None, None, "", ""

@callback(
    Output("alert-consulta", "children"),
    Output("modal-consulta", "is_open", allow_duplicate=True),
    Output("store-refresh-trigger-cons", "data"),
    Output("modal-trigger-aviso", "is_open", allow_duplicate=True),
    Output("modal-trigger-content", "children"),
    Input("btn-salvar-consulta", "n_clicks"),
    State("input-clinica-cons", "value"),
    State("input-medico-cons", "value"),
    State("input-paciente-cons", "value"),
    State("input-data-cons", "value"),
    State("input-hora-cons", "value"),
    State("store-refresh-trigger-cons", "data"),
    prevent_initial_call=True
)
def salvar_consulta(n_clicks, cli, med, pac, data, hora, current_trigger):
    if not all([cli, med, pac, data, hora]):
        return dbc.Alert("Todos os campos são obrigatórios!", color="danger", duration=3000), True, current_trigger or 0, False, ""
    
    try:
        data_hora = f"{data} {hora}:00"
        
        query = """
        INSERT INTO tabelaconsulta (CodCli, CodMed, CpfPaciente, Data_Hora)
        VALUES (%s, %s, %s, %s)
        """
        params = (cli, med, pac, data_hora)
        
        success, msg = db.execute_query(query, params)
        
        if success:
            # Verifica se há warnings/avisos na mensagem (ex: triggers)
            if "Avisos:" in msg:
                return dbc.Alert(["Consulta agendada! ", html.Br(), msg], color="warning", duration=5000), False, (current_trigger or 0) + 1, False, ""
            return dbc.Alert("Consulta agendada com sucesso!", color="success", duration=3000), False, (current_trigger or 0) + 1, False, ""
        else:
            # Mensagens de erro dos triggers aparecem aqui - detecta TRIGGER_AVISO
            if "TRIGGER_AVISO" in msg:
                # Extrai a mensagem do trigger
                aviso_msg = msg.split("TRIGGER_AVISO:")[-1].strip().replace("'", "").replace('"', '')
                modal_content = [
                    html.Div([
                        html.I(className="bi bi-exclamation-circle text-warning", style={"fontSize": "4rem"}),
                    ], className="mb-3"),
                    html.H4("Atenção!", className="mb-3 text-warning"),
                    html.P(aviso_msg, className="lead mb-4", style={"fontSize": "1.2rem"}),
                    html.Hr(),
                    html.Small([
                        html.I(className="bi bi-info-circle me-2"),
                        "Esta é uma regra de negócio do consultório aplicada automaticamente"
                    ], className="text-muted")
                ]
                # Mantém o modal de cadastro aberto para o usuário corrigir
                return None, True, current_trigger or 0, True, modal_content
            
            if "Duplicate entry" in msg or "já existe" in msg:
                return dbc.Alert("⚠️ Já existe uma consulta agendada neste horário para este médico!", color="danger", duration=5000), True, current_trigger or 0, False, ""
            
            # Qualquer outro erro
            return dbc.Alert(f"Erro: {msg}", color="danger", duration=5000), True, current_trigger or 0, False, ""
    except Exception as e:
        return dbc.Alert(f"Erro inesperado: {str(e)}", color="danger", duration=5000), True, current_trigger or 0, False, ""

@callback(
    Output("modal-trigger-aviso", "is_open"),
    Input("btn-fechar-modal-trigger", "n_clicks"),
    prevent_initial_call=True
)
def fechar_modal_trigger(n_clicks):
    return False

@callback(
    Output("modal-delete-consulta", "is_open"),
    Output("store-consulta-delete", "data"),
    Input({'type': 'btn-delete-cons', 'index': ALL}, "n_clicks"),
    Input("btn-confirmar-delete-cons", "n_clicks"),
    Input("btn-cancelar-delete-cons", "n_clicks"),
    State({'type': 'btn-delete-cons', 'index': ALL}, "id"),
    prevent_initial_call=True
)
def toggle_delete_modal(delete_clicks, confirm_click, cancel_click, delete_ids):
    ctx = callback_context
    
    if not ctx.triggered:
        return False, None

    triggered = ctx.triggered[0]
    if triggered.get('value') in (None, 0, False, ''):
        return False, None

    trigger_id = triggered['prop_id'].split('.')[0]
    
    if "btn-delete-cons" in trigger_id:
        button_id = json.loads(trigger_id)
        return True, button_id['index']
    
    return False, None

@callback(
    Output("alert-consulta", "children", allow_duplicate=True),
    Output("modal-delete-consulta", "is_open", allow_duplicate=True),
    Output("store-refresh-trigger-cons", "data", allow_duplicate=True),
    Input("btn-confirmar-delete-cons", "n_clicks"),
    State("store-consulta-delete", "data"),
    State("store-refresh-trigger-cons", "data"),
    prevent_initial_call=True
)
def deletar_consulta(n_clicks, dados, current_trigger):
    if dados:
        parts = dados.split('|')
        if len(parts) == 4:
            cli, med, pac, data_hora = parts
            
            query = """
            DELETE FROM tabelaconsulta 
            WHERE CodCli=%s AND CodMed=%s AND CpfPaciente=%s AND Data_Hora=%s
            """
            success, msg = db.execute_query(query, (cli, med, pac, data_hora))
            
            if success:
                # Verifica se há warnings/avisos na mensagem
                if "Avisos:" in msg:
                    return dbc.Alert(["Consulta excluída! ", html.Br(), msg], color="warning", duration=5000), False, (current_trigger or 0) + 1
                return dbc.Alert("Consulta excluída com sucesso!", color="success", duration=3000), False, (current_trigger or 0) + 1
            else:
                return dbc.Alert(f"Erro ao excluir: {msg}", color="danger", duration=5000), True, current_trigger or 0
    
    return None, False, current_trigger or 0 