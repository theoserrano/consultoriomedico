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
            dbc.Button("\u2795 Nova Consulta", id="btn-nova-consulta", color="warning", className="mb-3")
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
            dbc.Label("Filtrar por M�dico:"),
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
                        dbc.Label("Cl�nica *"),
                        dcc.Dropdown(id="input-clinica-cons", placeholder="Selecione a cl�nica")
                    ], md=4),
                    dbc.Col([
                        dbc.Label("M�dico *"),
                        dcc.Dropdown(id="input-medico-cons", placeholder="Selecione o m�dico")
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
        dbc.ModalHeader(dbc.ModalTitle("Confirmar Exclus�o")),
        dbc.ModalBody("Tem certeza que deseja excluir esta consulta?"),
        dbc.ModalFooter([
            dbc.Button("Confirmar", id="btn-confirmar-delete-cons", color="danger"),
            dbc.Button("Cancelar", id="btn-cancelar-delete-cons", color="secondary")
        ])
    ], id="modal-delete-consulta", is_open=False),
    
    dcc.Store(id='store-consulta-acao'),
    dcc.Store(id='store-consulta-delete'),
    html.Div(id="alert-consulta")
], fluid=True)

@callback(
    Output("tabela-consultas", "children"),
    Output("filtro-medico-cons", "options"),
    Input("btn-aplicar-filtros", "n_clicks"),
    Input("btn-salvar-consulta", "n_clicks"),
    Input("btn-confirmar-delete-cons", "n_clicks"),
    State("filtro-data-inicio", "value"),
    State("filtro-data-fim", "value"),
    State("filtro-medico-cons", "value")
)
def atualizar_tabela(apply_click, save_click, del_click, data_ini, data_fim, medico_filtro):
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
        html.Th("Data/Hora"), html.Th("Paciente"), html.Th("M�dico"),
        html.Th("Cl�nica"), html.Th("A��es")
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
    Input("btn-salvar-consulta", "n_clicks"),
    State("input-clinica-cons", "value"),
    State("input-medico-cons", "value"),
    State("input-paciente-cons", "value"),
    State("input-data-cons", "value"),
    State("input-hora-cons", "value"),
    prevent_initial_call=True
)
def salvar_consulta(n_clicks, cli, med, pac, data, hora):
    if not all([cli, med, pac, data, hora]):
        return dbc.Alert("Todos os campos s�o obrigat�rios!", color="danger", duration=3000)
    
    data_hora = f"{data} {hora}:00"
    
    query = """
    INSERT INTO tabelaconsulta (CodCli, CodMed, CpfPaciente, Data_Hora)
    VALUES (%s, %s, %s, %s)
    """
    params = (cli, med, pac, data_hora)
    
    success, msg = db.execute_query(query, params)
    
    if success:
        return dbc.Alert("Consulta agendada com sucesso! (Trigger de auditoria ativado)", color="success", duration=3000)
    else:
        if "Duplicate entry" in msg or "j� existe" in msg:
            return dbc.Alert("Erro: J� existe uma consulta agendada neste hor�rio para este m�dico! (Trigger impediu duplica��o)", color="danger", duration=5000)
        return dbc.Alert(f"Erro: {msg}", color="danger", duration=5000)

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
    Input("btn-confirmar-delete-cons", "n_clicks"),
    State("store-consulta-delete", "data"),
    prevent_initial_call=True
)
def deletar_consulta(n_clicks, dados):
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
                return dbc.Alert("Consulta exclu�da com sucesso! (Trigger de auditoria ativado)", color="success", duration=3000)
            else:
                return dbc.Alert(f"Erro ao excluir: {msg}", color="danger", duration=5000)
    
    return None 