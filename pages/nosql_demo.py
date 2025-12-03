# -*- coding: utf-8 -*-
"""
Página de demonstração NoSQL (Firebase/Firestore)
Mostra comparação lado a lado: MySQL vs Firebase
"""

from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# Função para criar o layout (não importa Firebase se não configurado)
def build_layout():
    """Constrói o layout da página NoSQL"""
    
    return dbc.Container([
        # Cabeçalho
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2([
                        html.I(className="bi bi-fire me-3"),
                        "Demonstração NoSQL - Firebase Firestore"
                    ], className="text-primary mb-3"),
                    html.P([
                        "Esta página demonstra operações CRUD usando Firebase/Firestore ",
                        "em comparação com o MySQL tradicional. ",
                        html.Strong("Ambos os bancos funcionam simultaneamente sem interferência.")
                    ], className="lead text-muted")
                ])
            ])
        ], className="mb-4"),
        
        # Status da conexão Firebase
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id="firebase-status-display", children=[
                            dbc.Spinner(html.Div(id="firebase-status-loading"))
                        ])
                    ])
                ], className="shadow-sm mb-4")
            ])
        ]),
        
        # Botão para verificar conexão
        dbc.Row([
            dbc.Col([
                dbc.Button([
                    html.I(className="bi bi-arrow-clockwise me-2"),
                    "Verificar Conexão Firebase"
                ], id="btn-check-firebase", color="primary", size="lg", className="mb-4")
            ], width=12)
        ]),
        
        # Tabs de demonstração
        dbc.Row([
            dbc.Col([
                dbc.Tabs([
                    # Tab 1: Comparação MySQL vs Firebase
                    dbc.Tab(label="📊 Comparação MySQL vs Firebase", tab_id="tab-comparacao", children=[
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Estatísticas Comparativas", className="mb-4"),
                                dbc.Row([
                                    # MySQL Stats
                                    dbc.Col([
                                        html.Div([
                                            html.H5([
                                                html.I(className="bi bi-database me-2"),
                                                "MySQL (Relacional)"
                                            ], className="text-info"),
                                            html.Div(id="mysql-stats")
                                        ])
                                    ], md=6),
                                    
                                    # Firebase Stats
                                    dbc.Col([
                                        html.Div([
                                            html.H5([
                                                html.I(className="bi bi-fire me-2"),
                                                "Firebase (NoSQL)"
                                            ], className="text-warning"),
                                            html.Div(id="firebase-stats")
                                        ])
                                    ], md=6)
                                ]),
                                
                                html.Hr(className="my-4"),
                                
                                # Gráfico comparativo
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Graph(id="graph-comparacao")
                                    ])
                                ])
                            ])
                        ], className="shadow-sm mt-3")
                    ]),
                    
                    # Tab 2: CRUD Firebase
                    dbc.Tab(label="✏️ Operações CRUD Firebase", tab_id="tab-crud", children=[
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Teste de Operações CRUD", className="mb-4"),
                                
                                # Formulário de teste
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("CPF do Paciente"),
                                        dbc.Input(
                                            id="input-cpf-test",
                                            placeholder="12345678900",
                                            type="text",
                                            maxLength=11
                                        )
                                    ], md=4),
                                    dbc.Col([
                                        dbc.Label("Nome"),
                                        dbc.Input(
                                            id="input-nome-test",
                                            placeholder="Nome completo",
                                            type="text"
                                        )
                                    ], md=8)
                                ], className="mb-3"),
                                
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Email"),
                                        dbc.Input(
                                            id="input-email-test",
                                            placeholder="email@exemplo.com",
                                            type="email"
                                        )
                                    ], md=6),
                                    dbc.Col([
                                        dbc.Label("Telefone"),
                                        dbc.Input(
                                            id="input-telefone-test",
                                            placeholder="(11) 98765-4321",
                                            type="text"
                                        )
                                    ], md=6)
                                ], className="mb-4"),
                                
                                # Botões de ação
                                dbc.Row([
                                    dbc.Col([
                                        dbc.ButtonGroup([
                                            dbc.Button([
                                                html.I(className="bi bi-plus-circle me-2"),
                                                "Criar"
                                            ], id="btn-create", color="success"),
                                            dbc.Button([
                                                html.I(className="bi bi-search me-2"),
                                                "Buscar"
                                            ], id="btn-read", color="info"),
                                            dbc.Button([
                                                html.I(className="bi bi-pencil me-2"),
                                                "Atualizar"
                                            ], id="btn-update", color="warning"),
                                            dbc.Button([
                                                html.I(className="bi bi-trash me-2"),
                                                "Deletar"
                                            ], id="btn-delete", color="danger")
                                        ], size="lg")
                                    ])
                                ]),
                                
                                html.Hr(className="my-4"),
                                
                                # Resultado das operações
                                html.Div(id="crud-result", className="mt-3")
                            ])
                        ], className="shadow-sm mt-3")
                    ]),
                    
                    # Tab 3: Modelos de Dados
                    dbc.Tab(label="🗂️ Modelos de Dados", tab_id="tab-modelos", children=[
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Comparação: Estruturas de Dados", className="mb-4"),
                                
                                dbc.Row([
                                    # MySQL Schema
                                    dbc.Col([
                                        html.H5([
                                            html.I(className="bi bi-table me-2"),
                                            "MySQL - Tabelas Relacionais"
                                        ], className="text-info mb-3"),
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.Pre("""
📋 tabelapaciente
├── CpfPaciente (PK)
├── NomePac
├── DataNasc
├── Genero
├── Telefone
└── Email

👨‍⚕️ tabelamedico
├── CodMed (PK)
├── NomeMed
├── Especialidade
├── Telefone
└── Email

📅 tabelaconsulta
├── CodCli (FK)
├── CodMed (FK)
├── CpfPaciente (FK)
└── Data_Hora
                                                """, className="mb-0", style={"fontSize": "0.9rem"})
                                            ])
                                        ], className="bg-light")
                                    ], md=6),
                                    
                                    # Firebase Schema
                                    dbc.Col([
                                        html.H5([
                                            html.I(className="bi bi-file-earmark-code me-2"),
                                            "Firebase - Documentos NoSQL"
                                        ], className="text-warning mb-3"),
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.Pre("""
📁 Collection: consultas
{
  "id": "auto-generated",
  "data_hora": "2024-12-02T14:30:00",
  "status": "realizada",
  
  "paciente": {
    "cpf": "12345678900",
    "nome": "João Silva",
    "email": "joao@email.com"
  },
  
  "medico": {
    "codigo": "MED123",
    "nome": "Dra. Maria",
    "especialidade": "Cardiologia"
  },
  
  "clinica": {
    "codigo": "CLI456",
    "nome": "MedCare"
  }
}
                                                """, className="mb-0", style={"fontSize": "0.85rem"})
                                            ])
                                        ], className="bg-light")
                                    ], md=6)
                                ])
                            ])
                        ], className="shadow-sm mt-3")
                    ]),
                    
                    # Tab 4: Migração de Dados
                    dbc.Tab(label="🔄 Migração MySQL → Firebase", tab_id="tab-migracao", children=[
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Ferramenta de Migração de Dados", className="mb-4"),
                                
                                dbc.Alert([
                                    html.I(className="bi bi-info-circle me-2"),
                                    "Esta ferramenta copia dados do MySQL para o Firebase sem afetar o banco original."
                                ], color="info"),
                                
                                # Opções de migração
                                dbc.Row([
                                    dbc.Col([
                                        html.H5("Selecione o que migrar:", className="mb-3"),
                                        dbc.Checklist(
                                            id="migration-options",
                                            options=[
                                                {"label": " Pacientes", "value": "pacientes"},
                                                {"label": " Médicos", "value": "medicos"},
                                                {"label": " Clínicas", "value": "clinicas"},
                                                {"label": " Consultas", "value": "consultas"}
                                            ],
                                            value=["pacientes", "medicos", "clinicas", "consultas"],
                                            inline=True,
                                            className="mb-3"
                                        ),
                                        
                                        dbc.Button([
                                            html.I(className="bi bi-arrow-right-circle me-2"),
                                            "Iniciar Migração"
                                        ], id="btn-migrate", color="primary", size="lg", className="mt-3"),
                                        
                                        html.Div(id="migration-result", className="mt-4")
                                    ])
                                ])
                            ])
                        ], className="shadow-sm mt-3")
                    ])
                ], id="tabs-nosql", active_tab="tab-comparacao")
            ])
        ])
    ], fluid=True, className="py-4")

# Layout principal
layout = build_layout()

def register_callbacks(app):
    """Registra os callbacks da página NoSQL"""
    
    @callback(
        Output("firebase-status-display", "children"),
        Input("btn-check-firebase", "n_clicks"),
        prevent_initial_call=False
    )
    def check_firebase_status(_n_clicks):
        """Verifica status da conexão Firebase"""
        try:
            from nosql.db_nosql import FirebaseDatabase
            
            db = FirebaseDatabase()
            if db.connect():
                # Tenta contar documentos
                try:
                    count = db.count_documents('pacientes')
                    return dbc.Alert([
                        html.H5([
                            html.I(className="bi bi-check-circle-fill me-2"),
                            "Firebase Conectado!"
                        ], className="alert-heading mb-3"),
                        html.P(f"Total de pacientes no Firestore: {count}"),
                        html.Hr(),
                        html.P([
                            html.I(className="bi bi-info-circle me-2"),
                            "O Firebase está operacional e pronto para uso."
                        ], className="mb-0")
                    ], color="success")
                except Exception as e:
                    return dbc.Alert([
                        html.H5([
                            html.I(className="bi bi-exclamation-triangle-fill me-2"),
                            "Firebase Conectado (Sem Dados)"
                        ], className="alert-heading mb-3"),
                        html.P(f"Conexão OK, mas sem dados: {str(e)}"),
                        html.Hr(),
                        html.P("Execute a migração para popular o Firebase.")
                    ], color="warning")
            else:
                return dbc.Alert([
                    html.H5([
                        html.I(className="bi bi-x-circle-fill me-2"),
                        "Firebase Não Conectado"
                    ], className="alert-heading mb-3"),
                    html.P("Não foi possível conectar ao Firebase."),
                    html.Hr(),
                    html.P([
                        "Configure o Firebase seguindo: ",
                        html.Code("docs/INSTALACAO_NOSQL.md")
                    ])
                ], color="danger")
                
        except ImportError:
            return dbc.Alert([
                html.H5([
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    "Módulo NoSQL Não Instalado"
                ], className="alert-heading mb-3"),
                html.P("Instale as dependências: pip install -r requirements_nosql.txt"),
                html.Hr(),
                html.P("Depois, configure seguindo: docs/INSTALACAO_NOSQL.md")
            ], color="warning")
        except Exception as e:
            return dbc.Alert([
                html.H5([
                    html.I(className="bi bi-bug-fill me-2"),
                    "Erro Inesperado"
                ], className="alert-heading mb-3"),
                html.P(f"Erro: {str(e)}"),
                html.Hr(),
                html.P("Verifique os logs para mais detalhes.")
            ], color="danger")
    
    @callback(
        [Output("mysql-stats", "children"),
         Output("firebase-stats", "children"),
         Output("graph-comparacao", "figure")],
        Input("tabs-nosql", "active_tab")
    )
    def update_stats(active_tab):
        """Atualiza estatísticas comparativas"""
        if active_tab != "tab-comparacao":
            return [], [], {}
        
        # MySQL Stats
        try:
            from db import db
            mysql_stats = dbc.ListGroup([
                dbc.ListGroupItem([
                    html.Strong("Pacientes: "),
                    str(db.fetch_one("SELECT COUNT(*) as total FROM tabelapaciente")['total'])
                ]),
                dbc.ListGroupItem([
                    html.Strong("Médicos: "),
                    str(db.fetch_one("SELECT COUNT(*) as total FROM tabelamedico")['total'])
                ]),
                dbc.ListGroupItem([
                    html.Strong("Clínicas: "),
                    str(db.fetch_one("SELECT COUNT(*) as total FROM tabelaclinica")['total'])
                ]),
                dbc.ListGroupItem([
                    html.Strong("Consultas: "),
                    str(db.fetch_one("SELECT COUNT(*) as total FROM tabelaconsulta")['total'])
                ])
            ], flush=True)
        except Exception:
            mysql_stats = dbc.Alert("MySQL não disponível", color="warning")
        
        # Firebase Stats
        try:
            from nosql.db_nosql import FirebaseDatabase
            firebase_db = FirebaseDatabase()
            firebase_db.connect()
            
            firebase_stats = dbc.ListGroup([
                dbc.ListGroupItem([
                    html.Strong("Pacientes: "),
                    str(firebase_db.count_documents('pacientes'))
                ]),
                dbc.ListGroupItem([
                    html.Strong("Médicos: "),
                    str(firebase_db.count_documents('medicos'))
                ]),
                dbc.ListGroupItem([
                    html.Strong("Clínicas: "),
                    str(firebase_db.count_documents('clinicas'))
                ]),
                dbc.ListGroupItem([
                    html.Strong("Consultas: "),
                    str(firebase_db.count_documents('consultas'))
                ])
            ], flush=True)
            
            # Gráfico comparativo
            fig = go.Figure(data=[
                go.Bar(name='MySQL', x=['Pacientes', 'Médicos', 'Clínicas', 'Consultas'],
                       y=[db.fetch_one("SELECT COUNT(*) as total FROM tabelapaciente")['total'],
                          db.fetch_one("SELECT COUNT(*) as total FROM tabelamedico")['total'],
                          db.fetch_one("SELECT COUNT(*) as total FROM tabelaclinica")['total'],
                          db.fetch_one("SELECT COUNT(*) as total FROM tabelaconsulta")['total']]),
                go.Bar(name='Firebase', x=['Pacientes', 'Médicos', 'Clínicas', 'Consultas'],
                       y=[firebase_db.count_documents('pacientes'),
                          firebase_db.count_documents('medicos'),
                          firebase_db.count_documents('clinicas'),
                          firebase_db.count_documents('consultas')])
            ])
            fig.update_layout(title="Comparação de Dados: MySQL vs Firebase", barmode='group')
            
        except Exception:
            firebase_stats = dbc.Alert("Firebase não configurado", color="warning")
            fig = {}
        
        return mysql_stats, firebase_stats, fig
    
    @callback(
        Output("crud-result", "children"),
        Input("btn-create", "n_clicks"),
        Input("btn-read", "n_clicks"),
        Input("btn-update", "n_clicks"),
        Input("btn-delete", "n_clicks"),
        Input("input-cpf-test", "value"),
        Input("input-nome-test", "value"),
        Input("input-email-test", "value"),
        Input("input-telefone-test", "value"),
        prevent_initial_call=True
    )
    def handle_crud_operations(create_clicks, read_clicks, update_clicks, delete_clicks, cpf, nome, email, telefone):
        """Manipula operações CRUD do Firebase"""
        from dash import callback_context
        
        if not callback_context.triggered:
            return ""
        
        trigger_id = callback_context.triggered[0]['prop_id'].split('.')[0]
        
        # Ignorar mudanças nos inputs
        if trigger_id in ['input-cpf-test', 'input-nome-test', 'input-email-test', 'input-telefone-test']:
            return ""
        
        # Validação do CPF
        if not cpf or len(cpf) != 11:
            return dbc.Alert([
                html.I(className="bi bi-exclamation-triangle-fill me-2"),
                "Por favor, insira um CPF válido com 11 dígitos."
            ], color="warning")
        
        try:
            from nosql.crud_operations import crud
            from nosql.db_nosql import firebase_db
            
            # Conectar ao Firebase
            if not firebase_db.connect():
                return dbc.Alert([
                    html.I(className="bi bi-x-circle-fill me-2"),
                    "Erro: Não foi possível conectar ao Firebase. Verifique a configuração."
                ], color="danger")
            
            # CREATE
            if trigger_id == "btn-create":
                if not nome:
                    return dbc.Alert([
                        html.I(className="bi bi-exclamation-triangle-fill me-2"),
                        "Nome é obrigatório para criar um paciente."
                    ], color="warning")
                
                sucesso, msg = crud.criar_paciente(
                    cpf=cpf,
                    nome=nome,
                    data_nascimento="2000-01-01",  # Data padrão
                    genero="M",
                    telefone=telefone or "",
                    email=email or ""
                )
                
                if sucesso:
                    return dbc.Alert([
                        html.H5([
                            html.I(className="bi bi-check-circle-fill me-2"),
                            "Paciente Criado!"
                        ], className="alert-heading"),
                        html.P(f"CPF: {cpf}"),
                        html.P(f"Nome: {nome}"),
                        html.Hr(),
                        html.P(msg, className="mb-0")
                    ], color="success")
                else:
                    return dbc.Alert([
                        html.I(className="bi bi-x-circle-fill me-2"),
                        f"Erro ao criar: {msg}"
                    ], color="danger")
            
            # READ
            elif trigger_id == "btn-read":
                paciente = crud.buscar_paciente(cpf)
                
                if paciente:
                    return dbc.Alert([
                        html.H5([
                            html.I(className="bi bi-person-check-fill me-2"),
                            "Paciente Encontrado!"
                        ], className="alert-heading mb-3"),
                        dbc.ListGroup([
                            dbc.ListGroupItem([html.Strong("CPF: "), paciente.get('cpf', 'N/A')]),
                            dbc.ListGroupItem([html.Strong("Nome: "), paciente.get('nome', 'N/A')]),
                            dbc.ListGroupItem([html.Strong("Email: "), paciente.get('email', 'N/A')]),
                            dbc.ListGroupItem([html.Strong("Telefone: "), paciente.get('telefone', 'N/A')]),
                            dbc.ListGroupItem([html.Strong("Data Nascimento: "), str(paciente.get('data_nascimento', 'N/A'))]),
                            dbc.ListGroupItem([html.Strong("Gênero: "), paciente.get('genero', 'N/A')])
                        ], flush=True)
                    ], color="info")
                else:
                    return dbc.Alert([
                        html.I(className="bi bi-person-x-fill me-2"),
                        f"Paciente com CPF {cpf} não encontrado no Firebase."
                    ], color="warning")
            
            # UPDATE
            elif trigger_id == "btn-update":
                # Verificar se o paciente existe
                paciente_existente = crud.buscar_paciente(cpf)
                if not paciente_existente:
                    return dbc.Alert([
                        html.I(className="bi bi-person-x-fill me-2"),
                        f"Paciente com CPF {cpf} não encontrado. Crie-o primeiro."
                    ], color="warning")
                
                # Atualizar apenas campos fornecidos
                dados_atualizacao = {}
                if nome:
                    dados_atualizacao['nome'] = nome
                if email:
                    dados_atualizacao['email'] = email
                if telefone:
                    dados_atualizacao['telefone'] = telefone
                
                if not dados_atualizacao:
                    return dbc.Alert([
                        html.I(className="bi bi-exclamation-triangle-fill me-2"),
                        "Forneça pelo menos um campo para atualizar (nome, email ou telefone)."
                    ], color="warning")
                
                sucesso, msg = crud.atualizar_paciente(cpf, dados_atualizacao)
                
                if sucesso:
                    campos_atualizados = ", ".join(dados_atualizacao.keys())
                    return dbc.Alert([
                        html.H5([
                            html.I(className="bi bi-check-circle-fill me-2"),
                            "Paciente Atualizado!"
                        ], className="alert-heading"),
                        html.P(f"CPF: {cpf}"),
                        html.P(f"Campos atualizados: {campos_atualizados}"),
                        html.Hr(),
                        html.P(msg, className="mb-0")
                    ], color="success")
                else:
                    return dbc.Alert([
                        html.I(className="bi bi-x-circle-fill me-2"),
                        f"Erro ao atualizar: {msg}"
                    ], color="danger")
            
            # DELETE
            elif trigger_id == "btn-delete":
                # Verificar se o paciente existe
                paciente_existente = crud.buscar_paciente(cpf)
                if not paciente_existente:
                    return dbc.Alert([
                        html.I(className="bi bi-person-x-fill me-2"),
                        f"Paciente com CPF {cpf} não encontrado."
                    ], color="warning")
                
                sucesso, msg = crud.deletar_paciente(cpf)
                
                if sucesso:
                    return dbc.Alert([
                        html.H5([
                            html.I(className="bi bi-trash-fill me-2"),
                            "Paciente Deletado!"
                        ], className="alert-heading"),
                        html.P(f"CPF: {cpf} foi removido do Firebase."),
                        html.Hr(),
                        html.P(msg, className="mb-0 small")
                    ], color="success")
                else:
                    return dbc.Alert([
                        html.I(className="bi bi-x-circle-fill me-2"),
                        f"Erro ao deletar: {msg}"
                    ], color="danger")
            
        except ImportError as e:
            return dbc.Alert([
                html.H5([
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    "Módulos NoSQL Não Instalados"
                ], className="alert-heading mb-3"),
                html.P("Instale: pip install -r requirements_nosql.txt"),
                html.Hr(),
                html.P(f"Erro: {str(e)}", className="mb-0 small")
            ], color="danger")
        except Exception as e:
            return dbc.Alert([
                html.H5([
                    html.I(className="bi bi-bug-fill me-2"),
                    "Erro Inesperado"
                ], className="alert-heading mb-3"),
                html.P(f"Erro: {str(e)}"),
                html.Hr(),
                html.P("Verifique os logs para mais detalhes.", className="mb-0")
            ], color="danger")
        
        return ""
    
    @callback(
        Output("migration-result", "children"),
        Input("btn-migrate", "n_clicks"),
        prevent_initial_call=True
    )
    def start_migration(n_clicks):
        """Inicia o processo de migração de dados"""
        if not n_clicks:
            return ""
        
        try:
            # Importar módulos necessários
            from nosql.migration import MySQLToFirestoreMigration
            from db import db as mysql_db
            from nosql.db_nosql import firebase_db
            
            # Verificar conexões
            if not mysql_db.ensure_connected():
                return dbc.Alert([
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    "Erro: Não foi possível conectar ao MySQL"
                ], color="danger")
            
            if not firebase_db.connect():
                return dbc.Alert([
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    "Erro: Não foi possível conectar ao Firebase"
                ], color="danger")
            
            # Criar instância de migração
            migration = MySQLToFirestoreMigration()
            
            # Executar migração
            sucesso = migration.migrar_tudo(limite_consultas=100)
            
            # Preparar resultado
            stats = migration.stats
            
            if sucesso:
                return dbc.Alert([
                    html.H5([
                        html.I(className="bi bi-check-circle-fill me-2"),
                        "Migração Concluída com Sucesso!"
                    ], className="alert-heading mb-3"),
                    html.Hr(),
                    html.H6("Resumo da Migração:"),
                    dbc.ListGroup([
                        dbc.ListGroupItem([
                            html.Strong("Pacientes: "),
                            f"{stats['pacientes']['migrados']} migrados, {stats['pacientes']['erros']} erros"
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("Médicos: "),
                            f"{stats['medicos']['migrados']} migrados, {stats['medicos']['erros']} erros"
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("Clínicas: "),
                            f"{stats['clinicas']['migrados']} migrados, {stats['clinicas']['erros']} erros"
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("Consultas: "),
                            f"{stats['consultas']['migrados']} migrados, {stats['consultas']['erros']} erros"
                        ])
                    ], flush=True, className="mt-3")
                ], color="success")
            else:
                return dbc.Alert([
                    html.H5([
                        html.I(className="bi bi-exclamation-triangle-fill me-2"),
                        "Migração Concluída com Alguns Erros"
                    ], className="alert-heading mb-3"),
                    html.Hr(),
                    html.H6("Resumo da Migração:"),
                    dbc.ListGroup([
                        dbc.ListGroupItem([
                            html.Strong("Pacientes: "),
                            f"{stats['pacientes']['migrados']} migrados, {stats['pacientes']['erros']} erros"
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("Médicos: "),
                            f"{stats['medicos']['migrados']} migrados, {stats['medicos']['erros']} erros"
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("Clínicas: "),
                            f"{stats['clinicas']['migrados']} migrados, {stats['clinicas']['erros']} erros"
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("Consultas: "),
                            f"{stats['consultas']['migrados']} migrados, {stats['consultas']['erros']} erros"
                        ])
                    ], flush=True, className="mt-3"),
                    html.Hr(),
                    html.P("Verifique os logs para mais detalhes sobre os erros.")
                ], color="warning")
                
        except ImportError as e:
            return dbc.Alert([
                html.H5([
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    "Erro: Módulos NoSQL Não Instalados"
                ], className="alert-heading mb-3"),
                html.P(f"Instale as dependências: pip install -r requirements_nosql.txt"),
                html.Hr(),
                html.P(f"Detalhes: {str(e)}")
            ], color="danger")
        except Exception as e:
            return dbc.Alert([
                html.H5([
                    html.I(className="bi bi-bug-fill me-2"),
                    "Erro Durante a Migração"
                ], className="alert-heading mb-3"),
                html.P(f"Erro: {str(e)}"),
                html.Hr(),
                html.P("Verifique os logs para mais detalhes.")
            ], color="danger")
