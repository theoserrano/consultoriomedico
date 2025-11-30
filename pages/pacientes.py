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
    html.Div(id="alert-paciente")
], fluid=True)

@callback(
    Output("tabela-pacientes", "children"),
    Input("filtro-paciente", "value"),
    Input("btn-salvar-paciente", "n_clicks"),
    Input("btn-confirmar-delete", "n_clicks")
)
def atualizar_tabela(filtro, save_clicks, del_clicks):
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
    Input("btn-salvar-paciente", "n_clicks"),
    State("store-paciente-acao", "data"),
    State("input-cpf", "value"),
    State("input-nome-pac", "value"),
    State("input-data-nasc", "value"),
    State("input-genero-pac", "value"),
    State("input-tel-pac", "value"),
    State("input-email-pac", "value"),
    prevent_initial_call=True
)
def salvar_paciente(n_clicks, acao, cpf, nome, data_nasc, genero, tel, email):
    if not cpf or not nome:
        return dbc.Alert("CPF e Nome são obrigatórios!", color="danger", duration=3000)
    
    if len(cpf) != 11:
        return dbc.Alert("CPF deve ter 11 dígitos!", color="danger", duration=3000)
    
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
        return dbc.Alert("Paciente salvo com sucesso!", color="success", duration=3000)
    else:
        return dbc.Alert(f"Erro: {msg}", color="danger", duration=5000)

@callback(
    Output("modal-delete-paciente", "is_open"),
    Output("store-cpf-delete", "data"),
    Input({'type': 'btn-delete-pac', 'index': ALL}, "n_clicks"),
    Input('btn-delete-selected-pac', 'n_clicks'),
    Input("btn-confirmar-delete", "n_clicks"),
    Input("btn-cancelar-delete", "n_clicks"),
    State({'type': 'btn-delete-pac', 'index': ALL}, "id"),
    State('pacientes-datatable', 'selected_rows'),
    State('pacientes-datatable', 'data'),
    prevent_initial_call=True
)
def toggle_delete_modal(delete_clicks, delete_selected_click, confirm_click, cancel_click, delete_ids, selected_rows, table_data):
    ctx = callback_context
    
    if not ctx.triggered:
        return False, None
    triggered = ctx.triggered[0]
    if triggered.get('value') in (None, 0, False, ''):
        return False, None

    trigger_id = triggered['prop_id'].split('.')[0]

    if 'btn-delete-selected-pac' in trigger_id:
        if not selected_rows or not table_data:
            return False, None
        idx = selected_rows[0]
        try:
            row = table_data[idx]
            cpf = row.get('CpfPaciente')
        except Exception:
            return False, None
        return True, cpf

    if "btn-delete-pac" in trigger_id:
        button_id = json.loads(trigger_id)
        return True, button_id['index']
    
    return False, None

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
            return dbc.Alert("Paciente excluído com sucesso!", color="success", duration=3000)
        else:
            return dbc.Alert(f"Erro ao excluir: {msg}", color="danger", duration=5000)
    
    return None