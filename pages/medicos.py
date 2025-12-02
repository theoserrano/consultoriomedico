# -*- coding: utf-8 -*-
from dash import html, dcc, callback, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
from db import db
import json

layout = dbc.Container([
    html.H2("Gerenciamento de Médicos", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Button("➕ Novo Médico", id="btn-novo-medico", color="success", className="mb-3")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Input(id="filtro-medico", placeholder="Filtrar por nome ou especialidade...", 
                     type="text", className="mb-3")
        ], md=6)
    ]),
    
    html.Div(id="tabela-medicos"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Média de Consultas por Médico")),
                dbc.CardBody(id="media-consultas-medico")
            ], className="mt-4")
        ])
    ]),
    
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id="modal-medico-titulo")),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Código Médico *"),
                        dbc.Input(id="input-codmed", placeholder="7 dígitos", maxLength=7, required=True)
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Nome Completo *"),
                        dbc.Input(id="input-nome-med", placeholder="Nome completo", required=True)
                    ], md=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Especialidade *"),
                        dbc.Input(id="input-especialidade", placeholder="Ex: Cardiologia", required=True)
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Gênero"),
                        dbc.Select(id="input-genero-med", options=[
                            {"label": "Masculino", "value": "M"},
                            {"label": "Feminino", "value": "F"}
                        ])
                    ], md=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Telefone"),
                        dbc.Input(id="input-tel-med", placeholder="(81) 99999-9999")
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Email"),
                        dbc.Input(id="input-email-med", type="email", placeholder="email@exemplo.com")
                    ], md=6)
                ])
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Salvar", id="btn-salvar-medico", color="success"),
            dbc.Button("Cancelar", id="btn-fechar-modal-medico", color="secondary")
        ])
    ], id="modal-medico", size="lg", is_open=False),
    
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Confirmar Exclusão")),
        dbc.ModalBody("Tem certeza que deseja excluir este médico?"),
        dbc.ModalFooter([
            dbc.Button("Confirmar", id="btn-confirmar-delete-med", color="danger"),
            dbc.Button("Cancelar", id="btn-cancelar-delete-med", color="secondary")
        ])
    ], id="modal-delete-medico", is_open=False),
    
    dcc.Store(id='store-medico-acao'),
    dcc.Store(id='store-codmed-delete'),
    html.Div(id="alert-medico")
], fluid=True)

@callback(
    Output("tabela-medicos", "children"),
    Output("media-consultas-medico", "children"),
    Input("filtro-medico", "value"),
    Input("btn-salvar-medico", "n_clicks"),
    Input("btn-confirmar-delete-med", "n_clicks")
)
def atualizar_tabela(filtro, save_clicks, del_clicks):
    if not db.ensure_connected():
        return dbc.Alert("Sem conexão com o banco de dados. Verifique o arquivo .env e o serviço MySQL.", color="danger"), "Nenhuma consulta registrada"

    query = "SELECT * FROM tabelamedico"
    params = None
    
    if filtro:
        query += " WHERE NomeMed LIKE %s OR Especialidade LIKE %s"
        params = (f"%{filtro}%", f"%{filtro}%")
    
    medicos = db.fetch_all(query, params)
    
    # Consulta não trivial: média de consultas por médico
    query_media = """
    SELECT 
        AVG(total) as media_consultas
    FROM (
        SELECT CodMed, COUNT(*) as total
        FROM tabelaconsulta
        GROUP BY CodMed
    ) as subconsulta
    """
    media_result = db.fetch_one(query_media)
    media_txt = f"Média: {media_result['media_consultas']:.2f} consultas por médico" if media_result and media_result['media_consultas'] else "Nenhuma consulta registrada"
    
    if not medicos:
        return dbc.Alert("Nenhum m�dico encontrado", color="info"), media_txt
    
    df = pd.DataFrame(medicos)
    
    table_header = [html.Thead(html.Tr([
        html.Th("Código"), html.Th("Nome"), html.Th("Especialidade"),
        html.Th("Gênero"), html.Th("Telefone"), html.Th("Email"), html.Th("Ações")
    ]))]
    
    rows = []
    for _, row in df.iterrows():
        rows.append(html.Tr([
            html.Td(row['CodMed']),
            html.Td(row['NomeMed']),
            html.Td(row['Especialidade']),
            html.Td(row['Genero']),
            html.Td(row['Telefone']),
            html.Td(row['Email']),
            html.Td([
                dbc.Button("\u270f\ufe0f", id={'type': 'btn-edit-med', 'index': row['CodMed']}, 
                          color="warning", size="sm", className="me-1"),
                dbc.Button("\U0001f5d1\ufe0f", id={'type': 'btn-delete-med', 'index': row['CodMed']}, 
                          color="danger", size="sm")
            ])
        ]))
    
    table_body = [html.Tbody(rows)]
    return dbc.Table(table_header + table_body, bordered=True, hover=True, responsive=True, striped=True), media_txt

@callback(
    Output("modal-medico", "is_open"),
    Output("modal-medico-titulo", "children"),
    Output("store-medico-acao", "data"),
    Output("input-codmed", "value"),
    Output("input-codmed", "disabled"),
    Output("input-nome-med", "value"),
    Output("input-especialidade", "value"),
    Output("input-genero-med", "value"),
    Output("input-tel-med", "value"),
    Output("input-email-med", "value"),
    Input("btn-novo-medico", "n_clicks"),
    Input({'type': 'btn-edit-med', 'index': ALL}, "n_clicks"),
    Input("btn-fechar-modal-medico", "n_clicks"),
    State({'type': 'btn-edit-med', 'index': ALL}, "id"),
    prevent_initial_call=True
)
def toggle_modal(novo_click, edit_clicks, fechar_click, edit_ids):
    ctx = callback_context
    
    if not ctx.triggered:
        return False, "", None, "", False, "", "", "", "", ""

    triggered = ctx.triggered[0]
    if triggered.get('value') in (None, 0, False, ''):
        return False, "", None, "", False, "", "", "", "", ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if "btn-novo-medico" in trigger_id:
        return True, "Novo Médico", "create", "", False, "", "", "", "", ""
    
    if "btn-fechar-modal-medico" in trigger_id:
        return False, "", None, "", False, "", "", "", "", ""
    
    if "btn-edit-med" in trigger_id:
        button_id = json.loads(trigger_id)
        cod = button_id['index']
        
        medico = db.fetch_one("SELECT * FROM tabelamedico WHERE CodMed = %s", (cod,))
        
        if medico:
            return (True, "Editar Médico", "update", cod, True,
                   medico['NomeMed'], medico['Especialidade'],
                   medico['Genero'], medico['Telefone'], medico['Email'])
    
    return False, "", None, "", False, "", "", "", "", ""

@callback(
    Output("alert-medico", "children"),
    Input("btn-salvar-medico", "n_clicks"),
    State("store-medico-acao", "data"),
    State("input-codmed", "value"),
    State("input-nome-med", "value"),
    State("input-especialidade", "value"),
    State("input-genero-med", "value"),
    State("input-tel-med", "value"),
    State("input-email-med", "value"),
    prevent_initial_call=True
)
def salvar_medico(n_clicks, acao, cod, nome, espec, genero, tel, email):
    if not cod or not nome or not espec:
        return dbc.Alert("Código, Nome e Especialidade são obrigatórios!", color="danger", duration=3000)
    
    if len(cod) != 7:
        return dbc.Alert("Código deve ter 7 dígitos!", color="danger", duration=3000)
    
    if acao == "create":
        query = """
        INSERT INTO tabelamedico (CodMed, NomeMed, Genero, Telefone, Email, Especialidade)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (cod, nome, genero or None, tel or None, email or None, espec)
    else:
        query = """
        UPDATE tabelamedico 
        SET NomeMed=%s, Genero=%s, Telefone=%s, Email=%s, Especialidade=%s
        WHERE CodMed=%s
        """
        params = (nome, genero or None, tel or None, email or None, espec, cod)
    
    success, msg = db.execute_query(query, params)
    
    if success:
        return dbc.Alert("Médico salvo com sucesso!", color="success", duration=3000)
    else:
        return dbc.Alert(f"Erro: {msg}", color="danger", duration=5000)

@callback(
    Output("modal-delete-medico", "is_open"),
    Output("store-codmed-delete", "data"),
    Input({'type': 'btn-delete-med', 'index': ALL}, "n_clicks"),
    Input("btn-confirmar-delete-med", "n_clicks"),
    Input("btn-cancelar-delete-med", "n_clicks"),
    State({'type': 'btn-delete-med', 'index': ALL}, "id"),
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
    
    if "btn-delete-med" in trigger_id:
        button_id = json.loads(trigger_id)
        return True, button_id['index']
    
    return False, None

@callback(
    Output("alert-medico", "children", allow_duplicate=True),
    Input("btn-confirmar-delete-med", "n_clicks"),
    State("store-codmed-delete", "data"),
    prevent_initial_call=True
)
def deletar_medico(n_clicks, cod):
    if cod:
        success, msg = db.execute_query("DELETE FROM tabelamedico WHERE CodMed = %s", (cod,))
        
        if success:
            return dbc.Alert("Médico excluído com sucesso!", color="success", duration=3000)
        else:
            return dbc.Alert(f"Erro ao excluir: {msg}", color="danger", duration=5000)
    
    return None