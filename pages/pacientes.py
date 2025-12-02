# -*- coding: utf-8 -*-
from dash import html, dcc, callback, callback_context, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
from db import db
import json

layout = dbc.Container([
    html.H2("Gerenciamento de Pacientes", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Button("➕ Novo Paciente", id="btn-novo-paciente", color="primary", className="mb-3 btn-icon"),
            html.Span(className="ms-2 action-buttons", children=[
                dbc.Button([html.Img(src='/assets/icons/icon-edit.svg', height='18'), " Editar selecionado"], id='btn-edit-selected-pac', color='warning', size='sm'),
                dbc.Button([html.Img(src='/assets/icons/icon-delete.svg', height='18'), " Excluir selecionado"], id='btn-delete-selected-pac', color='danger', size='sm')
            ])
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Input(id="filtro-paciente", placeholder="Filtrar por nome...", type="text", className="mb-3 table-search", debounce=True)
        ], md=6)
    ]),
    
    html.Div(id="tabela-pacientes"),
    
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id="modal-paciente-titulo")),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("CPF *"),
                        dbc.Input(id="input-cpf", placeholder="11 dígitos", maxLength=11, required=True)
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Nome Completo *"),
                        dbc.Input(id="input-nome-pac", placeholder="Nome completo", required=True)
                    ], md=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Data de Nascimento"),
                        dbc.Input(id="input-data-nasc", type="date")
                    ], md=4),
                    dbc.Col([
                        dbc.Label("Gênero"),
                        dbc.Select(id="input-genero-pac", options=[
                            {"label": "Masculino", "value": "M"},
                            {"label": "Feminino", "value": "F"}
                        ])
                    ], md=4),
                    dbc.Col([
                        dbc.Label("Telefone"),
                        dbc.Input(id="input-tel-pac", placeholder="(81) 99999-9999")
                    ], md=4)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Email"),
                        dbc.Input(id="input-email-pac", type="email", placeholder="email@exemplo.com")
                    ])
                ])
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Salvar", id="btn-salvar-paciente", color="primary"),
            dbc.Button("Cancelar", id="btn-fechar-modal-paciente", color="secondary")
        ])
    ], id="modal-paciente", size="lg", is_open=False),
    
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Confirmar Exclusão")),
        dbc.ModalBody("Tem certeza que deseja excluir este paciente?"),
        dbc.ModalFooter([
            dbc.Button("Confirmar", id="btn-confirmar-delete", color="danger"),
            dbc.Button("Cancelar", id="btn-cancelar-delete", color="secondary")
        ])
    ], id="modal-delete-paciente", is_open=False),
    
    dcc.Store(id='store-paciente-acao'),
    dcc.Store(id='store-cpf-delete'),
    dcc.Store(id='store-refresh-trigger', data=0),
    html.Div(id="alert-paciente")
], fluid=True)

@callback(
    Output("tabela-pacientes", "children"),
    Input("filtro-paciente", "value"),
    Input("store-refresh-trigger", "data")
)
def atualizar_tabela(filtro, refresh_trigger):
    # Se não conectado, retornar alerta informativo
    if not db.ensure_connected():
        return dbc.Alert("Sem conexão com o banco de dados. Verifique o arquivo .env e o serviço MySQL.", color="danger")
    query = "SELECT * FROM tabelapaciente"
    params = None
    
    if filtro:
        query += " WHERE NomePac LIKE %s"
        params = (f"%{filtro}%",)
    
    pacientes = db.fetch_all(query, params)
    
    if not pacientes:
        return dbc.Alert("Nenhum paciente encontrado", color="info")
    
    df = pd.DataFrame(pacientes)

    # DataTable provides native filtering/sorting for a friendlier search experience
    columns = [
        {"name": "CPF", "id": "CpfPaciente"},
        {"name": "Nome", "id": "NomePac"},
        {"name": "Data Nasc.", "id": "DataNascimento"},
        {"name": "Gênero", "id": "Genero"},
        {"name": "Telefone", "id": "Telefone"},
        {"name": "Email", "id": "Email"},
    ]

    table = dash_table.DataTable(
        id='pacientes-datatable',
        columns=columns,
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        page_size=10,
        style_table={'overflowX': 'auto'},
        row_selectable='single',
        selected_rows=[],
        style_cell={'textAlign': 'left', 'padding': '6px'},
        style_header={'fontWeight': 'bold'},
    )

    return html.Div(className='data-table-container', children=[table])

@callback(
    Output("modal-paciente", "is_open"),
    Output("modal-paciente-titulo", "children"),
    Output("store-paciente-acao", "data"),
    Output("input-cpf", "value"),
    Output("input-cpf", "disabled"),
    Output("input-nome-pac", "value"),
    Output("input-data-nasc", "value"),
    Output("input-genero-pac", "value"),
    Output("input-tel-pac", "value"),
    Output("input-email-pac", "value"),
    Input("btn-novo-paciente", "n_clicks"),
    Input('btn-edit-selected-pac', 'n_clicks'),
    Input({'type': 'btn-edit-pac', 'index': ALL}, "n_clicks"),
    Input("btn-fechar-modal-paciente", "n_clicks"),
    State({'type': 'btn-edit-pac', 'index': ALL}, "id"),
    State('pacientes-datatable', 'selected_rows'),
    State('pacientes-datatable', 'data'),
    prevent_initial_call=True
)
def toggle_modal(novo_click, edit_selected_click, edit_clicks, fechar_click, edit_ids, selected_rows, table_data):
    ctx = callback_context
    
    if not ctx.triggered:
        return False, "", None, "", False, "", "", "", "", ""

    # proteger contra triggers iniciais com valor None/0
    triggered = ctx.triggered[0]
    if triggered.get('value') in (None, 0, False, ''):
        return False, "", None, "", False, "", "", "", "", ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if "btn-novo-paciente" in trigger_id:
        return True, "Novo Paciente", "create", "", False, "", "", "", "", ""
    
    if "btn-fechar-modal-paciente" in trigger_id:
        return False, "", None, "", False, "", "", "", "", ""
    # editar selecionado (DataTable)
    if 'btn-edit-selected-pac' in trigger_id:
        # abrir modal para edição do item selecionado na tabela
        if not selected_rows or not table_data:
            return False, "", None, "", False, "", "", "", "", ""
        idx = selected_rows[0]
        try:
            row = table_data[idx]
            cpf = row.get('CpfPaciente')
        except Exception:
            return False, "", None, "", False, "", "", "", "", ""

        if not db.ensure_connected():
            return False, "", None, "", False, "", "", "", "", ""

        paciente = db.fetch_one("SELECT * FROM tabelapaciente WHERE CpfPaciente = %s", (cpf,))
        if paciente:
            return (True, "Editar Paciente", "update", cpf, True,
                   paciente['NomePac'], 
                   str(paciente['DataNascimento']) if paciente['DataNascimento'] else "",
                   paciente['Genero'], paciente['Telefone'], paciente['Email'])

    if "btn-edit-pac" in trigger_id:
        button_id = json.loads(trigger_id)
        cpf = button_id['index']
        # proteger caso sem conexão
        if not db.ensure_connected():
            return False, "", None, "", False, "", "", "", "", ""

        paciente = db.fetch_one("SELECT * FROM tabelapaciente WHERE CpfPaciente = %s", (cpf,))

        if paciente:
            return (True, "Editar Paciente", "update", cpf, True,
                   paciente['NomePac'], 
                   str(paciente['DataNascimento']) if paciente['DataNascimento'] else "",
                   paciente['Genero'], paciente['Telefone'], paciente['Email'])
    
    return False, "", None, "", False, "", "", "", "", ""

@callback(
    Output("alert-paciente", "children"),
    Output("modal-paciente", "is_open", allow_duplicate=True),
    Output("store-refresh-trigger", "data"),
    Input("btn-salvar-paciente", "n_clicks"),
    State("store-paciente-acao", "data"),
    State("input-cpf", "value"),
    State("input-nome-pac", "value"),
    State("input-data-nasc", "value"),
    State("input-genero-pac", "value"),
    State("input-tel-pac", "value"),
    State("input-email-pac", "value"),
    State("store-refresh-trigger", "data"),
    prevent_initial_call=True
)
def salvar_paciente(n_clicks, acao, cpf, nome, data_nasc, genero, tel, email, current_trigger):
    if not cpf or not nome:
        return dbc.Alert("CPF e Nome são obrigatórios!", color="danger", duration=3000), True, current_trigger or 0
    
    if len(cpf) != 11:
        return dbc.Alert("CPF deve ter 11 dígitos!", color="danger", duration=3000), True, current_trigger or 0
    
    try:
        if acao == "create":
            query = """
            INSERT INTO tabelapaciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (cpf, nome, data_nasc or None, genero or None, tel or None, email or None)
        else:
            query = """
            UPDATE tabelapaciente 
            SET NomePac=%s, DataNascimento=%s, Genero=%s, Telefone=%s, Email=%s
            WHERE CpfPaciente=%s
            """
            params = (nome, data_nasc or None, genero or None, tel or None, email or None, cpf)
        
        success, msg = db.execute_query(query, params)
        
        if success:
            # Verifica se há warnings/avisos na mensagem
            if "Avisos:" in msg:
                return dbc.Alert(["Paciente salvo! ", html.Br(), msg], color="warning", duration=5000), False, (current_trigger or 0) + 1
            return dbc.Alert("Paciente salvo com sucesso!", color="success", duration=3000), False, (current_trigger or 0) + 1
        else:
            return dbc.Alert(f"Erro: {msg}", color="danger", duration=5000), True, current_trigger or 0
    except Exception as e:
        return dbc.Alert(f"Erro inesperado: {str(e)}", color="danger", duration=5000), True, current_trigger or 0

@callback(
    Output("modal-delete-paciente", "is_open"),
    Output("store-cpf-delete", "data"),
    Output("store-refresh-trigger", "data", allow_duplicate=True),
    Input({'type': 'btn-delete-pac', 'index': ALL}, "n_clicks"),
    Input('btn-delete-selected-pac', 'n_clicks'),
    Input("btn-confirmar-delete", "n_clicks"),
    Input("btn-cancelar-delete", "n_clicks"),
    State({'type': 'btn-delete-pac', 'index': ALL}, "id"),
    State('pacientes-datatable', 'selected_rows'),
    State('pacientes-datatable', 'data'),
    State('store-cpf-delete', 'data'),
    State('store-refresh-trigger', 'data'),
    prevent_initial_call=True
)
def toggle_delete_modal(delete_clicks, delete_selected_click, confirm_click, cancel_click, delete_ids, selected_rows, table_data, cpf_stored, current_trigger):
    ctx = callback_context
    
    if not ctx.triggered:
        return False, None, current_trigger or 0
    triggered = ctx.triggered[0]
    if triggered.get('value') in (None, 0, False, ''):
        return False, None, current_trigger or 0

    trigger_id = triggered['prop_id'].split('.')[0]

    if 'btn-delete-selected-pac' in trigger_id:
        if not selected_rows or not table_data:
            return False, None, current_trigger or 0
        idx = selected_rows[0]
        try:
            row = table_data[idx]
            cpf = row.get('CpfPaciente')
        except Exception:
            return False, None, current_trigger or 0
        return True, cpf, current_trigger or 0

    if "btn-delete-pac" in trigger_id:
        button_id = json.loads(trigger_id)
        return True, button_id['index'], current_trigger or 0
    
    if "btn-confirmar-delete" in trigger_id and cpf_stored:
        try:
            db.execute_query("DELETE FROM tabelapaciente WHERE CpfPaciente = %s", (cpf_stored,))
        except Exception:
            pass
        return False, None, (current_trigger or 0) + 1
    
    if "btn-cancelar-delete" in trigger_id:
        return False, None, current_trigger or 0
    
    return False, None, current_trigger or 0

@callback(
    Output("alert-paciente", "children", allow_duplicate=True),
    Input("btn-confirmar-delete", "n_clicks"),
    State("store-cpf-delete", "data"),
    prevent_initial_call=True
)
def deletar_paciente(n_clicks, cpf):
    if cpf:
        success, msg = db.execute_query("DELETE FROM tabelapaciente WHERE CpfPaciente = %s", (cpf,))
        
        if success:
            # Verifica se há warnings/avisos na mensagem
            if "Avisos:" in msg:
                return dbc.Alert(["Paciente excluído! ", html.Br(), msg], color="warning", duration=5000)
            return dbc.Alert("Paciente excluído com sucesso!", color="success", duration=3000)
        else:
            return dbc.Alert(f"Erro ao excluir: {msg}", color="danger", duration=5000)
    
    return None