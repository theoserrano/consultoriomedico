# 🏥 Sistema de Consultório Médico

Sistema completo de gerenciamento para consultórios médicos com dashboard moderno, analytics avançados e integração dual MySQL + Firebase Firestore (NoSQL).

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/dash-2.14.2-brightgreen.svg)
![MySQL](https://img.shields.io/badge/mysql-8.0+-orange.svg)
![Firebase](https://img.shields.io/badge/firebase-firestore-yellow.svg)

---

## 📑 Índice

- [Funcionalidades](#-funcionalidades-principais)
- [Instalação Rápida](#-instalação-rápida)
- [Instalação MySQL](#-instalação-mysql-detalhada)
- [Instalação Firebase](#-instalação-firebase-nosql)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Uso do Sistema](#-como-usar)
- [Exemplos de Código](#-exemplos-de-código-crud)
- [Tecnologias](#-tecnologias-utilizadas)
- [Performance](#-otimizações-de-performance)
- [Modelagem](#-modelagem-de-dados)

---

## ✨ Funcionalidades Principais

### 🎯 Arquitetura Dual Database
- **MySQL**: Banco relacional tradicional (ACID, transações, integridade referencial)
- **Firebase Firestore**: NoSQL em tempo real (escalabilidade, flexibilidade, cloud-native)
- **Migração automática**: Transferência de dados MySQL → Firebase com progresso visual
- **Operações simultâneas**: Ambos bancos funcionam em paralelo sem interferência

### 🏠 Dashboard Interativo
- 📊 4 KPIs principais: Total de Pacientes, Médicos, Clínicas e Consultas
- 📈 Gráfico de tendência dos últimos 30 dias
- 👨‍⚕️ Top 5 médicos mais ativos
- 📅 Próximas consultas agendadas
- 🎨 Design moderno com animações e gradientes

### 📊 Analytics Avançado
- Série temporal de consultas por período
- Análise por médico, clínica e especialidade
- Heatmap de horários mais movimentados
- Distribuição de idades e gênero dos pacientes
- Boxplot e scatter plots interativos
- Filtros dinâmicos por clínica, médico e período

### 🔥 Demonstração NoSQL (Firebase)
- Interface comparativa MySQL vs Firebase lado a lado
- Migração de dados com **barra de progresso em tempo real**
- Operações CRUD completas no Firestore
- Estatísticas de ambos os bancos simultaneamente
- Suporte a dois modos de modelagem: Embedded e Referenced

### 📱 Gestão Completa
- **Pacientes**: CRUD completo com validação de CPF
- **Médicos**: Gestão com especialidades
- **Clínicas**: Cadastro com endereço e contato
- **Consultas**: Agendamento e histórico
- **CASCADE DELETE**: Exclusão automática de dados relacionados

---

## ⚡ Instalação Rápida

```bash
# 1. Clonar repositório
git clone <url-do-repositorio>
cd consultoriomedico

# 2. Instalar dependências Python
pip install -r requirements.txt

# 3. Importar banco de dados MySQL completo
mysql -u root -p < banco_completo.sql

# 4. Executar aplicação
python app.py

# 5. Acessar no navegador
http://127.0.0.1:8050
```

**Pronto!** O sistema estará rodando com MySQL e dados pré-carregados.

---

## 🗄️ Instalação MySQL (Detalhada)

### Pré-requisitos
- Python 3.8 ou superior
- MySQL 8.0 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências

```bash
pip install -r requirements.txt
```

**Principais dependências:**
- `dash==2.14.2` - Framework web
- `plotly==5.18.0` - Gráficos interativos
- `dash-bootstrap-components==1.5.0` - Componentes UI
- `pandas==2.1.4` - Análise de dados
- `mysql-connector-python==8.2.0` - Conexão MySQL
- `python-dotenv==1.0.0` - Variáveis de ambiente
- `Faker==22.0.0` - Geração de dados artificiais

### Passo 2: Configurar MySQL

**Opção A: Banco Completo (Recomendado)**

```bash
# Importar banco com estrutura + dados
mysql -u root -p < banco_completo.sql
```

Contém:
- ✅ 111 pacientes
- ✅ 45 médicos
- ✅ 6 clínicas
- ✅ 1500 consultas

**Opção B: Criar e Popular Manualmente**

```bash
# 1. Criar banco e estrutura
mysql -u root -p
CREATE DATABASE consultoriomedico;
USE consultoriomedico;
SOURCE consultoriomedio.sql;
exit;

# 2. Popular com dados artificiais
python populate_mysql.py
```

### Passo 3: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configuração MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=consultoriomedico

# Configuração da Aplicação
DEMO=false
DB_USE_SQLITE_FALLBACK=true
```

### Passo 4: Testar Conexão

```bash
python -c "from db import db; print('✅ MySQL conectado!' if db.ensure_connected() else '❌ Erro de conexão')"
```

### Passo 5: Aplicar Otimizações (Opcional)

```bash
# Criar índices para melhor performance
mysql -u root -p consultoriomedico < create_indexes.sql

# Ou aplicar via Python
python apply_indexes.py
```

---

## 🔥 Instalação Firebase (NoSQL)

### Por que Firebase Firestore?
- ☁️ **Cloud-native**: Sem necessidade de servidor próprio
- ⚡ **Tempo real**: Sincronização automática de dados
- 📈 **Escalável**: Cresce automaticamente com a demanda
- 🔒 **Seguro**: Autenticação e regras de segurança integradas
- 🆓 **Gratuito**: Tier grátis generoso para desenvolvimento

### Passo 1: Criar Projeto Firebase

1. Acesse: https://console.firebase.google.com/
2. Faça login com conta Google
3. Clique em **"Adicionar projeto"**
4. Nome: `consultorio-medico-nosql`
5. Desabilite Google Analytics (opcional)
6. Clique em **"Criar projeto"**

### Passo 2: Ativar Firestore

1. No menu lateral: **"Firestore Database"**
2. Clique em **"Criar banco de dados"**
3. Escolha **"Modo de teste"** (desenvolvimento)
4. Localização: `southamerica-east1` (São Paulo)
5. Clique em **"Ativar"**

### Passo 3: Obter Credenciais

1. Vá em **Configurações do Projeto** (ícone de engrenagem)
2. Aba **"Contas de serviço"**
3. Clique em **"Gerar nova chave privada"**
4. Salve o arquivo JSON como `firebase-credentials.json` na raiz do projeto

⚠️ **IMPORTANTE**: Adicione ao `.gitignore`:
```
firebase-credentials.json
```

### Passo 4: Instalar Dependências Firebase

```bash
pip install -r requirements_nosql.txt
```

Contém:
- `firebase-admin==6.3.0` - SDK Firebase
- `google-cloud-firestore==2.14.0` - Cliente Firestore

### Passo 5: Configurar .env

Adicione ao seu arquivo `.env`:

```env
# Firebase Configuration
FIREBASE_CREDENTIALS=firebase-credentials.json
FIREBASE_MODELING_MODE=embedded  # ou 'referenced'
```

### Passo 6: Testar Conexão Firebase

```bash
python scripts/test_firebase_connection.py
```

Deve exibir:
```
✅ Firebase Conectado!
✅ Total de pacientes no Firestore: 0
```

### Passo 7: Migrar Dados MySQL → Firebase

Execute a aplicação e acesse a página **"Demonstração NoSQL"**:

```bash
python app.py
# Acesse: http://127.0.0.1:8050
# Vá na aba "🔄 Migração MySQL → Firebase"
# Clique em "Iniciar Migração"
```

Você verá:
- 📊 Barra de progresso em tempo real
- 📈 Contador de registros migrados
- ✅ Resumo final com estatísticas

---

## 📦 Estrutura do Projeto

```
consultoriomedico/
│
├── app.py                      # 🚀 Aplicação principal Dash
├── db.py                       # 🗄️ Conexão MySQL com pooling
├── config.py                   # ⚙️ Configurações e variáveis de ambiente
├── populate_mysql.py           # 🎲 Gera dados artificiais MySQL
├── apply_indexes.py            # 📈 Aplica otimizações de índices
│
├── requirements.txt            # 📋 Dependências MySQL
├── requirements_nosql.txt      # 📋 Dependências Firebase
├── banco_completo.sql          # 💾 Backup completo do banco
├── create_indexes.sql          # 🔧 Script SQL de índices
├── triggers.sql                # ⚡ Triggers do banco
│
├── .env                        # 🔐 Variáveis de ambiente (criar)
├── firebase-credentials.json   # 🔑 Credenciais Firebase (criar)
│
├── assets/
│   ├── styles.css             # 🎨 CSS customizado profissional
│   └── icons/                 # 🖼️ Ícones do sistema
│
├── pages/
│   ├── __init__.py
│   ├── home.py                # 🏠 Dashboard principal
│   ├── analytics.py           # 📊 Analytics avançado
│   ├── pacientes.py           # 👥 CRUD Pacientes
│   ├── medicos.py             # ⚕️ CRUD Médicos
│   ├── clinicas.py            # 🏥 CRUD Clínicas
│   ├── consultas.py           # 📅 CRUD Consultas
│   └── nosql_demo.py          # 🔥 Demonstração Firebase
│
├── nosql/
│   ├── __init__.py
│   ├── config_nosql.py        # ⚙️ Configurações Firebase
│   ├── db_nosql.py            # 🔥 Conexão Firestore
│   ├── models_nosql.py        # 📋 Modelos Firestore
│   ├── crud_operations.py     # 🛠️ CRUD Firebase (classe FirestoreCRUD)
│   └── migration.py           # 🔄 Migração MySQL → Firebase
│
└── scripts/
    ├── test_firebase_connection.py   # ✅ Testa conexão Firebase
    └── demo_crud_firebase.py         # 🎬 Demo CRUD interativo
```

---

## 🎮 Como Usar

### Executar Aplicação

```bash
python app.py
```

Acesse: `http://127.0.0.1:8050`

### Navegação

| Página | Descrição | URL |
|--------|-----------|-----|
| 🏠 **Início** | Dashboard com KPIs e visão geral | `/` |
| 👥 **Pacientes** | Gestão completa de pacientes | `/pacientes` |
| ⚕️ **Médicos** | Cadastro e controle de médicos | `/medicos` |
| 🏥 **Clínicas** | Gerenciamento de clínicas | `/clinicas` |
| 📅 **Consultas** | Agendamento e histórico | `/consultas` |
| 📊 **Analytics** | Gráficos e análises avançadas | `/analytics` |
| 🔥 **NoSQL Demo** | Firebase/Firestore demo | `/nosql-demo` |

### Operações Principais

#### Cadastrar Paciente
1. Vá em **Pacientes**
2. Clique em **"+ Novo Paciente"**
3. Preencha: CPF, Nome, Data Nascimento, Gênero, Telefone, Email
4. Clique em **"Salvar"**

#### Agendar Consulta
1. Vá em **Consultas**
2. Clique em **"+ Nova Consulta"**
3. Selecione: Paciente, Médico, Clínica, Data/Hora
4. Clique em **"Agendar"**

#### Visualizar Analytics
1. Vá em **Analytics**
2. Use filtros: Clínica, Médico, Período
3. Explore os gráficos interativos

#### Usar Firebase (NoSQL)
1. Vá em **Demonstração NoSQL**
2. **Aba Comparação**: Veja MySQL vs Firebase lado a lado
3. **Aba CRUD**: Teste operações CREATE, READ, UPDATE, DELETE
4. **Aba Migração**: Migre dados MySQL → Firebase com progresso visual

---

## 💻 Exemplos de Código CRUD

### MySQL (usando db.py)

```python
from db import db

# CREATE - Inserir paciente
db.execute("""
    INSERT INTO tabelapaciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email)
    VALUES (%s, %s, %s, %s, %s, %s)
""", ('12345678900', 'João Silva', '1990-01-01', 'M', '11999999999', 'joao@email.com'))

# READ - Buscar paciente
paciente = db.fetch_one("SELECT * FROM tabelapaciente WHERE CpfPaciente = %s", ('12345678900',))
print(paciente)

# UPDATE - Atualizar email
db.execute(
    "UPDATE tabelapaciente SET Email = %s WHERE CpfPaciente = %s",
    ('novo@email.com', '12345678900')
)

# DELETE - Remover paciente
db.execute("DELETE FROM tabelapaciente WHERE CpfPaciente = %s", ('12345678900',))

# READ ALL - Listar todos
pacientes = db.fetch_all("SELECT * FROM tabelapaciente ORDER BY NomePac")
for p in pacientes:
    print(f"{p['CpfPaciente']} - {p['NomePac']}")
```

### Firebase Firestore (usando nosql/crud_operations.py)

```python
from nosql.crud_operations import crud
from nosql.db_nosql import firebase_db

# Conectar
firebase_db.connect()

# CREATE - Criar paciente
success, message = crud.criar_paciente(
    cpf="12345678900",
    nome="João Silva",
    data_nascimento="1990-01-01",
    genero="M",
    telefone="11999999999",
    email="joao@email.com"
)
print(f"Criado: {success} - {message}")

# READ - Buscar paciente
paciente = crud.buscar_paciente("12345678900")
if paciente:
    print(f"Nome: {paciente['nome']}")
    print(f"Email: {paciente['email']}")

# UPDATE - Atualizar dados
success, message = crud.atualizar_paciente(
    "12345678900",
    {
        "email": "novo@email.com",
        "telefone": "11888888888"
    }
)
print(f"Atualizado: {success}")

# DELETE - Remover paciente (CASCADE automático)
success, message = crud.deletar_paciente("12345678900")
print(f"Deletado: {success} - {message}")

# READ ALL - Listar todos
pacientes = crud.listar_pacientes(limit=10)
for p in pacientes:
    print(f"{p['cpf']} - {p['nome']}")
```

### Migração MySQL → Firebase

```python
from nosql.migration import MySQLToFirestoreMigration

# Criar instância
migration = MySQLToFirestoreMigration()

# Migrar tudo (limite de 100 consultas)
sucesso = migration.migrar_tudo(limite_consultas=100)

# Ver progresso em tempo real
progress = MySQLToFirestoreMigration.get_progress()
print(f"Status: {progress['status']}")
print(f"Pacientes: {progress['pacientes']['migrados']}/{progress['pacientes']['total']}")
print(f"Médicos: {progress['medicos']['migrados']}/{progress['medicos']['total']}")

# Ver estatísticas finais
stats = migration.stats
print(f"Total migrado: {stats['pacientes']['migrados'] + stats['medicos']['migrados']}")
```

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Dash 2.14.2** - Framework web para Python
- **Plotly 5.18.0** - Biblioteca de gráficos interativos
- **Pandas 2.1.4** - Análise e manipulação de dados

### Bancos de Dados
- **MySQL 8.0+** - Banco relacional com suporte a JSON
- **Firebase Firestore** - NoSQL cloud-native do Google
- **SQLite** - Fallback automático (desenvolvimento)

### Frontend
- **Dash Bootstrap Components 1.5.0** - Componentes Bootstrap
- **Bootstrap Icons** - Ícones modernos
- **CSS3** - Animações e gradientes customizados

### Ferramentas
- **Faker 22.0.0** - Geração de dados artificiais
- **python-dotenv 1.0.0** - Gerenciamento de variáveis de ambiente
- **mysql-connector-python 8.2.0** - Driver MySQL
- **firebase-admin 6.3.0** - SDK Firebase

---

## 📊 Modelagem de Dados

### MySQL (Relacional)

```
┌─────────────────┐       ┌─────────────────┐
│  tabelapaciente │       │   tabelamedico  │
├─────────────────┤       ├─────────────────┤
│ CpfPaciente PK  │   ┌───│ CodMed PK       │
│ NomePac         │   │   │ NomeMed         │
│ DataNascimento  │   │   │ Especialidade   │
│ Genero          │   │   │ Genero          │
│ Telefone        │   │   │ Telefone        │
│ Email           │   │   │ Email           │
└─────────────────┘   │   └─────────────────┘
        │             │            │
        │             │            │
        │             │            │
        └─────┬───────┴────────┬───┘
              │                │
       ┌──────▼────────────────▼─────┐
       │     tabelaconsulta          │
       ├─────────────────────────────┤
       │ CpfPaciente FK              │
       │ CodMed FK                   │
       │ CodCli FK                   │
       │ Data_Hora                   │
       └─────────────────────────────┘
              │
              │
       ┌──────▼──────────┐
       │ tabelaclinica   │
       ├─────────────────┤
       │ CodCli PK       │
       │ NomeCli         │
       │ Endereco        │
       │ Telefone        │
       │ Email           │
       └─────────────────┘
```

### Firebase Firestore (NoSQL)

**Modo Embedded (Padrão)**: Dados desnormalizados para performance

```
Collection: consultas
Document: auto-id
{
  "data_hora": "2024-12-04T14:30:00",
  "status": "realizada",
  "observacoes": "Consulta de rotina",
  
  "paciente": {
    "cpf": "12345678900",
    "nome": "João Silva",
    "email": "joao@email.com"
  },
  
  "medico": {
    "codigo": "MED123",
    "nome": "Dra. Maria Santos",
    "especialidade": "Cardiologia"
  },
  
  "clinica": {
    "codigo": "CLI456",
    "nome": "MedCare Centro",
    "endereco": "Rua X, 100"
  }
}
```

**Modo Referenced**: Dados normalizados com referências

```
Collection: consultas
Document: auto-id
{
  "cpf_paciente": "12345678900",
  "cod_medico": "MED123",
  "cod_clinica": "CLI456",
  "data_hora": "2024-12-04T14:30:00",
  "status": "realizada"
}

Collection: pacientes
Document: 12345678900
{
  "nome": "João Silva",
  "email": "joao@email.com",
  ...
}
```

---

## ⚡ Otimizações de Performance

### Índices MySQL

```sql
-- Índices em chaves estrangeiras
CREATE INDEX idx_consulta_paciente ON tabelaconsulta(CpfPaciente);
CREATE INDEX idx_consulta_medico ON tabelaconsulta(CodMed);
CREATE INDEX idx_consulta_clinica ON tabelaconsulta(CodCli);

-- Índice composto para queries frequentes
CREATE INDEX idx_consulta_data_medico ON tabelaconsulta(Data_Hora, CodMed);

-- Índices de busca
CREATE INDEX idx_paciente_nome ON tabelapaciente(NomePac);
CREATE INDEX idx_medico_especialidade ON tabelamedico(Especialidade);
```

Aplicar índices:
```bash
python apply_indexes.py
```

### Connection Pooling

O sistema usa **connection pooling** para reutilizar conexões MySQL:

```python
# Em db.py
self.pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="consultorio_pool",
    pool_size=5,
    pool_reset_session=True,
    **connection_config
)
```

### Firebase: Embedded vs Referenced

- **Embedded**: Melhor performance de leitura (1 query)
- **Referenced**: Melhor para dados que mudam frequentemente

Configure em `.env`:
```env
FIREBASE_MODELING_MODE=embedded  # ou 'referenced'
```

---

## 📈 Comparação MySQL vs Firebase

| Característica | MySQL | Firebase Firestore |
|----------------|-------|-------------------|
| **Tipo** | Relacional (SQL) | NoSQL (Documentos) |
| **Schema** | Fixo, definido | Flexível, dinâmico |
| **Transações** | ACID completo | Limitadas (documentos únicos) |
| **Escalabilidade** | Vertical | Horizontal (automática) |
| **Consultas** | SQL complexo com JOINs | Queries simples sem JOINs |
| **Integridade** | Chaves estrangeiras, constraints | Gerenciada pela aplicação |
| **Performance** | Ótima para dados estruturados | Ótima para leitura/escrita rápida |
| **Hospedagem** | Servidor próprio | Cloud (Firebase) |
| **Custo** | Servidor + manutenção | Pay-as-you-go |
| **Backup** | Manual ou scripts | Automático (Firebase) |
| **Tempo Real** | Polling necessário | Built-in |

### Quando Usar MySQL
✅ Dados fortemente estruturados  
✅ Relacionamentos complexos  
✅ Necessidade de transações ACID  
✅ Queries complexas com múltiplos JOINs  
✅ Integridade referencial crítica  

### Quando Usar Firebase
✅ Dados semi-estruturados ou flexíveis  
✅ Necessidade de escalabilidade automática  
✅ Aplicações real-time  
✅ Prototipagem rápida  
✅ Sincronização multi-dispositivo  

---

## 🔧 Configurações Avançadas

### Variáveis de Ambiente (.env)

```env
# ========== MySQL Configuration ==========
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=consultoriomedico

# ========== Firebase Configuration ==========
FIREBASE_CREDENTIALS=firebase-credentials.json
FIREBASE_MODELING_MODE=embedded  # ou 'referenced'

# ========== Application Settings ==========
DEMO=false
DB_USE_SQLITE_FALLBACK=true
DEBUG=false

# ========== Server Configuration ==========
HOST=0.0.0.0
PORT=8050
```

---

## 🐛 Troubleshooting

### Erro de Conexão MySQL

**Problema**: `mysql.connector.errors.InterfaceError: Can't connect to MySQL server`

**Solução**:
```bash
# Verificar se MySQL está rodando
mysql --version
mysql -u root -p -e "SELECT 1"

# Verificar credenciais no .env
cat .env | grep DB_

# Testar conexão Python
python -c "from db import db; db.ensure_connected()"
```

### Erro Firebase Credentials

**Problema**: `FileNotFoundError: firebase-credentials.json not found`

**Solução**:
1. Baixe credenciais do Firebase Console
2. Salve como `firebase-credentials.json` na raiz
3. Verifique permissões do arquivo
4. Confirme caminho no `.env`

### Erro de Importação

**Problema**: `ModuleNotFoundError: No module named 'dash'`

**Solução**:
```bash
# Reinstalar todas as dependências
pip install -r requirements.txt
pip install -r requirements_nosql.txt

# Verificar instalação
pip list | grep dash
pip list | grep firebase
```

---

## 📝 Scripts Úteis

### Testar Conexão Firebase
```bash
python scripts/test_firebase_connection.py
```

### Demo CRUD Firebase Interativo
```bash
python scripts/demo_crud_firebase.py
```

### Popular Banco MySQL
```bash
python populate_mysql.py
```

### Aplicar Índices de Performance
```bash
python apply_indexes.py
```

### Backup do Banco MySQL
```bash
mysqldump -u root -p consultoriomedico > backup_$(date +%Y%m%d).sql
```

### Restaurar Backup
```bash
mysql -u root -p consultoriomedico < backup_20241204.sql
```

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/MinhaFeature`
3. Commit: `git commit -m 'Adiciona MinhaFeature'`
4. Push: `git push origin feature/MinhaFeature`
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é de uso acadêmico.

---

## 🎓 Recursos de Aprendizado

### Documentação Oficial
- [Dash Documentation](https://dash.plotly.com/)
- [Plotly Python](https://plotly.com/python/)
- [MySQL Reference](https://dev.mysql.com/doc/)
- [Firebase Firestore](https://firebase.google.com/docs/firestore)
- [Python Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)

---

**🎉 Sistema pronto para uso! Aproveite! 🎉**
