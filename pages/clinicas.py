# -*- coding: utf-8 -*-
from dash import html, dcc, callback, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
from db import db
import json

layout = dbc.Container([
    html.H2("Gerenciamento de Clínicas", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Button("➕ Nova Clínica", id="btn-nova-clinica", color="info", className="mb-3")
        ])
    ]),
    
    html.Div(id="tabela-clinicas"),
    
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id="modal-clinica-titulo")),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Código Clínica *"),
                        dbc.Input(id="input-codcli", placeholder="6 dígitos", maxLength=6, required=True)
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Nome Clínica *"),
                        dbc.Input(id="input-nome-cli", placeholder="Nome da clínica", required=True)
                    ], md=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Endereço"),
                        dbc.Input(id="input-endereco", placeholder="Endereço completo")
                    ])
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Telefone"),
                        dbc.Input(id="input-tel-cli", placeholder="(81) 99999-9999")
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Email"),
                        dbc.Input(id="input-email-cli", type="email", placeholder="email@exemplo.com")
                    ], md=6)
                ])
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Salvar", id="btn-salvar-clinica", color="info"),
            dbc.Button("Cancelar", id="btn-fechar-modal-clinica", color="secondary")
        ])
    ], id="modal-clinica", size="lg", is_open=False),
    
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Confirmar Exclusão")),
        dbc.ModalBody("Tem certeza que deseja excluir esta clínica?"),
        dbc.ModalFooter([
            dbc.Button("Confirmar", id="btn-confirmar-delete-cli", color="danger"),
            dbc.Button("Cancelar", id="btn-cancelar-delete-cli", color="secondary")
        ])
    ], id="modal-delete-clinica", is_open=False),
    
    dcc.Store(id='store-clinica-acao'),
    dcc.Store(id='store-codcli-delete'),
    dcc.Store(id='store-refresh-trigger-cli', data=0),
    html.Div(id="alert-clinica")
], fluid=True)

@callback(
    Output("tabela-clinicas", "children"),
    Input("store-refresh-trigger-cli", "data")
)
def atualizar_tabela(refresh_trigger):
    clinicas = db.fetch_all("SELECT * FROM tabelaclinica")
    
    if not clinicas:
        return dbc.Alert("Nenhuma clínica cadastrada", color="info")
    
    df = pd.DataFrame(clinicas)
    
    table_header = [html.Thead(html.Tr([
        html.Th("Código"), html.Th("Nome"), html.Th("Endereço"),
        html.Th("Telefone"), html.Th("Email"), html.Th("Ações")
    ]))]
    
    rows = []
    for _, row in df.iterrows():
        rows.append(html.Tr([
            html.Td(row['CodCli']),
            html.Td(row['NomeCli']),
            html.Td(row['Endereco']),
            html.Td(row['Telefone']),
            html.Td(row['Email']),
            html.Td([
                dbc.Button("✏️", id={'type': 'btn-edit-cli', 'index': row['CodCli']}, 
                          color="warning", size="sm", className="me-1"),
                dbc.Button("🗑️", id={'type': 'btn-delete-cli', 'index': row['CodCli']}, 
                          color="danger", size="sm")
            ])
        ]))
    
    table_body = [html.Tbody(rows)]
    return dbc.Table(table_header + table_body, bordered=True, hover=True, responsive=True, striped=True)

@callback(
    Output("modal-clinica", "is_open"),
    Output("modal-clinica-titulo", "children"),
    Output("store-clinica-acao", "data"),
    Output("input-codcli", "value"),
    Output("input-codcli", "disabled"),
    Output("input-nome-cli", "value"),
    Output("input-endereco", "value"),
    Output("input-tel-cli", "value"),
    Output("input-email-cli", "value"),
    Input("btn-nova-clinica", "n_clicks"),
    Input({'type': 'btn-edit-cli', 'index': ALL}, "n_clicks"),
    Input("btn-fechar-modal-clinica", "n_clicks"),
    State({'type': 'btn-edit-cli', 'index': ALL}, "id"),
    prevent_initial_call=True
)
def toggle_modal(novo_click, edit_clicks, fechar_click, edit_ids):
    ctx = callback_context
    
    if not ctx.triggered:
        return False, "", None, "", False, "", "", "", ""

    triggered = ctx.triggered[0]
    if triggered.get('value') in (None, 0, False, ''):
        return False, "", None, "", False, "", "", "", ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if "btn-nova-clinica" in trigger_id:
        return True, "Nova Clínica", "create", "", False, "", "", "", ""
    
    if "btn-fechar-modal-clinica" in trigger_id:
        return False, "", None, "", False, "", "", "", ""
    
    if "btn-edit-cli" in trigger_id:
        button_id = json.loads(trigger_id)
        cod = button_id['index']
        
        clinica = db.fetch_one("SELECT * FROM tabelaclinica WHERE CodCli = %s", (cod,))
        
        if clinica:
            return (True, "Editar Clínica", "update", cod, True,
                   clinica['NomeCli'], clinica['Endereco'],
                   clinica['Telefone'], clinica['Email'])
    
    return False, "", None, "", False, "", "", "", ""

@callback(
    Output("alert-clinica", "children"),
    Output("modal-clinica", "is_open", allow_duplicate=True),
    Output("store-refresh-trigger-cli", "data"),
    Input("btn-salvar-clinica", "n_clicks"),
    State("store-clinica-acao", "data"),
    State("input-codcli", "value"),
    State("input-nome-cli", "value"),
    State("input-endereco", "value"),
    State("input-tel-cli", "value"),
    State("input-email-cli", "value"),
    State("store-refresh-trigger-cli", "data"),
    prevent_initial_call=True
)
def salvar_clinica(n_clicks, acao, cod, nome, end, tel, email, current_trigger):
    if not cod or not nome:
        return dbc.Alert("Código e Nome são obrigatórios!", color="danger", duration=3000), True, current_trigger or 0
    
    if len(cod) != 6:
        return dbc.Alert("Código deve ter 6 dígitos!", color="danger", duration=3000), True, current_trigger or 0
    
    try:
        if acao == "create":
            query = """
            INSERT INTO tabelaclinica (CodCli, NomeCli, Endereco, Telefone, Email)
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (cod, nome, end or None, tel or None, email or None)
        else:
            query = """
            UPDATE tabelaclinica 
            SET NomeCli=%s, Endereco=%s, Telefone=%s, Email=%s
            WHERE CodCli=%s
            """
            params = (nome, end or None, tel or None, email or None, cod)
        
        success, msg = db.execute_query(query, params)
        
        if success:
            return dbc.Alert("Clínica salva com sucesso!", color="success", duration=3000), False, (current_trigger or 0) + 1
        else:
            return dbc.Alert(f"Erro: {msg}", color="danger", duration=5000), True, current_trigger or 0
    except Exception as e:
        return dbc.Alert(f"Erro inesperado: {str(e)}", color="danger", duration=5000), True, current_trigger or 0

@callback(
    Output("modal-delete-clinica", "is_open"),
    Output("store-codcli-delete", "data"),
    Input({'type': 'btn-delete-cli', 'index': ALL}, "n_clicks"),
    Input("btn-confirmar-delete-cli", "n_clicks"),
    Input("btn-cancelar-delete-cli", "n_clicks"),
    State({'type': 'btn-delete-cli', 'index': ALL}, "id"),
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
    
    if "btn-delete-cli" in trigger_id:
        button_id = json.loads(trigger_id)
        return True, button_id['index']
    
    return False, None

@callback(
    Output("alert-clinica", "children", allow_duplicate=True),
    Output("modal-delete-clinica", "is_open", allow_duplicate=True),
    Output("store-refresh-trigger-cli", "data", allow_duplicate=True),
    Input("btn-confirmar-delete-cli", "n_clicks"),
    State("store-codcli-delete", "data"),
    State("store-refresh-trigger-cli", "data"),
    prevent_initial_call=True
)
def deletar_clinica(n_clicks, cod, current_trigger):
    if cod:
        success, msg = db.execute_query("DELETE FROM tabelaclinica WHERE CodCli = %s", (cod,))
        
        if success:
            return dbc.Alert("Clínica excluída com sucesso!", color="success", duration=3000), False, (current_trigger or 0) + 1
        else:
            return dbc.Alert(f"Erro ao excluir: {msg}", color="danger", duration=5000), True, current_trigger or 0
    
    return None, False, current_trigger or 0