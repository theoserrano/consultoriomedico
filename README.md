# Sistema de Consultório Médico

Sistema web completo para gerenciamento de consultório médico desenvolvido em Python com Dash, MySQL e triggers de auditoria.

## 📋 Requisitos do Sistema

### Software Necessário
- **Python**: 3.10 ou superior
- **MySQL**: 8.0 ou superior
- **Navegador**: Chrome, Firefox ou Edge (versões recentes)

### Bibliotecas Python
Todas as dependências estão listadas em `requirements.txt`.

---

## 🚀 Instalação e Configuração
## ⚙️ Produção

Para rodar em produção recomendamos usar Gunicorn (WSGI) + container Docker. Após instalar dependências, inicie com:

```bash
# local, com gunicorn
gunicorn -w 4 -b 0.0.0.0:8050 wsgi:server

# ou usando Docker (build no diretório consultoriomedico):
docker build -t consultorio-app .
docker run -e DB_HOST=... -e DB_USER=... -e DB_PASSWORD=... -e DB_NAME=consultoriomedico -p 8050:8050 consultorio-app
```

Use um usuário de aplicação (não `root`) no `.env` e não versionar `.env`.
 
### Deploy usando Firebase (Cloud Run)

1. Instale e autentique a Firebase CLI e o Google Cloud SDK.

2. Suba a imagem para o Google Cloud Artifact Registry / Container Registry or let Firebase deploy Cloud Run for you.

3. Configure `firebase.json` e `.firebaserc` (já incluídos no projeto). Edite `.firebaserc` e substitua `YOUR_FIREBASE_PROJECT_ID` pelo seu project id.

4. Deploy Cloud Run service (exemplo manual):

```bash
# build image
docker build -t gcr.io/YOUR_FIREBASE_PROJECT_ID/consultorio-app:latest .
# push
docker push gcr.io/YOUR_FIREBASE_PROJECT_ID/consultorio-app:latest
# deploy to Cloud Run
gcloud run deploy consultorio-app --image gcr.io/YOUR_FIREBASE_PROJECT_ID/consultorio-app:latest --platform managed --region us-central1 --allow-unauthenticated --set-env-vars DB_HOST=mysql-host,DB_USER=appuser,DB_PASSWORD=senha,DB_NAME=consultoriomedico
```

5. Or use Firebase Hosting to route traffic to Cloud Run (the included `firebase.json` rewrites all requests to `consultorio-app`). Then run:

```bash
firebase deploy --only hosting,run
```

Note: Replace environment variables appropriately — Firebase Hosting's rewrite will route to the Cloud Run service you deployed. If you prefer full automation, I can add a `cloudbuild.yaml` to trigger builds on push.

### Passo 1: Clonar/Baixar o Projeto
```bash
# Extrair o arquivo ZIP ou clonar o repositório
cd consultorio-medico
```

### Passo 2: Criar Ambiente Virtual Python
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Banco de Dados MySQL

#### 4.1 Criar o Banco de Dados
```bash
# Acesse o MySQL
mysql -u root -p

# No prompt do MySQL, crie o banco:
CREATE DATABASE consultoriomedico CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
EXIT;
```

#### 4.2 Importar o Dump
```bash
# No terminal (fora do MySQL):
mysql -u root -p consultoriomedico < Dump20251128.sql
```

**Verificação:**
```sql
USE consultoriomedico;
SHOW TABLES;
SELECT COUNT(*) FROM tabelapaciente;
SELECT COUNT(*) FROM tabelamedico;
SELECT COUNT(*) FROM tabelaclinica;
SELECT COUNT(*) FROM tabelaconsulta;
```

#### 4.3 Aplicar os Triggers
```bash
mysql -u root -p consultoriomedico < trigger_auditoria.sql
```

**Verificar triggers:**
```sql
USE consultoriomedico;
SHOW TRIGGERS;
```

Você deve ver 4 triggers:
- `trg_auditoria_consulta_insert`
- `trg_auditoria_consulta_update`
- `trg_auditoria_consulta_delete`
- `trg_prevenir_consulta_duplicada`

### Passo 5: Configurar Variáveis de Ambiente

#### 5.1 Copiar arquivo de exemplo
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

#### 5.2 Editar o arquivo `.env`
Abra o arquivo `.env` em um editor de texto e configure:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha_mysql_aqui
DB_NAME=consultoriomedico
```

**⚠️ IMPORTANTE:** Substitua `sua_senha_mysql_aqui` pela senha real do seu MySQL.

### Passo 6: Executar a Aplicação
```bash
python app.py
```
4) Criar ambiente Python, instalar dependências e executar a app Dash (fish):

```fish
./run.sh
```

Se preferir manualmente:

```fish
python3 -m venv .venv
source .venv/bin/activate.fish
pip install -r requirements.txt
python3 app.py
```

Ferramenta de diagnóstico

Também foi adicionada uma ferramenta simples para checar a conexão com o banco:

```fish
python3 scripts/check_db.py
```

Ela tentará reconectar e imprimirá passos recomendados caso falhe.
Dash is running on http://0.0.0.0:8050/

 * Serving Flask app 'app'
 * Debug mode: on
```

### Passo 7: Acessar o Sistema
Abra o navegador e acesse: **http://localhost:8050**

---

## 📊 Gerar DER no MySQL Workbench

### Método: Engenharia Reversa

1. **Abrir MySQL Workbench**
2. **Conectar ao servidor MySQL**
   - Clique em "Database" → "Connect to Database"
   - Digite as credenciais (usuário: root, senha: sua senha)
   
3. **Engenharia Reversa**
   - Menu: `Database` → `Reverse Engineer...`
   - **Stored Connection**: Selecione sua conexão
   - Clique em `Next`
   
4. **Selecionar Schema**
   - Marque o banco `consultoriomedico`
   - Clique em `Next` até a tela de seleção de objetos
   
5. **Selecionar Tabelas**
   - Marque todas as tabelas:
     - `tabelaclinica`
     - `tabelamedico`
     - `tabelapaciente`
     - `tabelaconsulta`
     - `auditoria_consultas`
   - Clique em `Execute` → `Next` → `Close`
   
6. **Visualizar e Exportar DER**
   - O DER será gerado automaticamente
   - Para exportar: `File` → `Export` → `Export as PNG/PDF`
   - Salve como: `DER_ConsultorioMedico.png`

"""
# Sistema de Consultório Médico — Guia de Instalação e Uso

Este repositório contém uma aplicação web em Python para gerenciamento de um consultório médico.
A interface principal agora é feita com **Streamlit** (fácil de rodar) e a camada de dados usa **MySQL** com **SQLAlchemy**.

O que entregamos:
- Código-fonte da aplicação (Streamlit)
- Scripts SQL (dump e triggers)
- `requirements.txt`, `.env.example`, `run.sh`
- Documentação de instalação, testes e roteiro de vídeo

Observação: o arquivo do dump fornecido pelo avaliador está em `/mnt/data/Dump20251128 (1).sql` (use esse caminho ao importar).

----

## Requisitos
- Python 3.10+
- MySQL 8.0+

## Estrutura (resumida)

```
consultoriomedico/
├── streamlit_app.py           # Aplicação principal (Streamlit)
├── app.py                    # App Dash (exemplo/legacy)
├── db.py                     # Conexão MySQL (SQLAlchemy)
├── config.py                 # Leitura de .env
├── requirements.txt
├── .env.example
├── Dump20251128 (1).sql     # Dump fornecido (path de exemplo)
├── trigger_auditoria.sql
├── trigger_prevent_duplicate.sql
├── run.sh
├── README.md
└── tests/test_cases.md
```

## Instalação e execução (passo-a-passo)

1) Copie `.env.example` para `.env` e edite com suas credenciais:

```fish
cp .env.example .env
# Edite .env e defina: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
```

2) Criar o banco e importar o dump (usar o arquivo do avaliador em `/mnt/data/...`):

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS consultoriomedico CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
mysql -u root -p consultoriomedico < "/mnt/data/Dump20251128 (1).sql"
```

3) (Opcional) aplicar triggers de auditoria e prevenção:

```bash
mysql -u root -p consultoriomedico < trigger_auditoria.sql
mysql -u root -p consultoriomedico < trigger_prevent_duplicate.sql
```

4) Criar ambiente Python, instalar dependências e executar a app Streamlit (fish):

```fish
./run.sh
```

Se preferir manualmente:

```fish
python3 -m venv .venv
source .venv/bin/activate.fish
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8050
```

5) Abra o navegador em `http://localhost:8050`.

----

## Trigger escolhido (regra de negócio)

Nome: `trg_prevent_duplicate_consulta` — Objetivo: prevenir agendamento duplicado.

Motivação: impede que duas consultas sejam agendadas para o mesmo médico no mesmo horário; garante consistência de agenda no nível do banco.

SQL (arquivo: `trigger_prevent_duplicate.sql`):

```sql
DELIMITER $$
CREATE TRIGGER trg_prevent_duplicate_consulta
BEFORE INSERT ON tabelaconsulta
FOR EACH ROW
BEGIN
    IF EXISTS(SELECT 1 FROM tabelaconsulta WHERE CodMed = NEW.CodMed AND Data_Hora = NEW.Data_Hora) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Agendamento duplicado para este médico no mesmo horário';
    END IF;
END$$
DELIMITER ;
```

Aplicação:
```bash
mysql -u root -p consultoriomedico < trigger_prevent_duplicate.sql
```

----

## DER (MySQL Workbench) — passo-a-passo breve

1. Abra MySQL Workbench.
2. Conecte ao servidor onde importou o dump.
3. Menu: `Database` → `Reverse Engineer...` → escolha a conexão.
4. Selecione o schema `consultoriomedico` e prossiga até a conclusão.
5. Exporte o diagrama via `File` → `Export` → `Export as PNG/PDF`.

----

## Testes e checagens (manuais)

1. Verificar importação do dump:

```bash
mysql -u root -p -e "USE consultoriomedico; SHOW TABLES; SELECT COUNT(*) FROM tabelapaciente;"
```

2. Rodar a aplicação Streamlit e acessar `http://localhost:8050`.

3. Casos de teste mínimos (descritos no arquivo `tests/test_cases.md`):
   - Inserir paciente via UI e verificar no banco
   - Atualizar paciente via UI
   - Inserir consulta duplicada (mesmo médico/hora) — deve ser bloqueado pelo trigger
   - Violação de FK ao usar clínica inexistente — deve haver erro
   - Executar consultas não triviais (consultas por especialidade / média por médico)

----

## Roteiro do vídeo (~15 minutos)

Tempo e tópicos sugeridos (preencha nomes dos integrantes):

- 00:00–01:30 — Introdução e objetivos (Integrante A)
- 01:30–03:30 — DER e estrutura do banco (Integrante B)
- 03:30–06:00 — CRUD Pacientes (Integrante C)
- 06:00–08:30 — CRUD Médicos/Clínicas (Integrante A)
- 08:30–11:00 — Agendamento, trigger e auditoria (Integrante B)
- 11:00–13:00 — Consultas não triviais e análise (Integrante C)
- 13:00–14:30 — Testes de integridade / violação FK (Integrante A)
- 14:30–15:00 — Conclusão e próximos passos (Integrante B)

Inclua em cada trecho comandos, telas do Workbench, e demonstrações ao vivo dos casos de teste.

----

## Arquivos principais (o que faz cada um)

- `streamlit_app.py`: App Streamlit — páginas: Overview, Pacientes (CRUD), Médicos (lista), Consultas (CRUD), Análises.
- `db.py`: Funções de conexão usando SQLAlchemy (`get_engine()`, `test_connection()`).
- `config.py`: Lê `.env` com `python-dotenv` e retorna as configurações.
- `trigger_prevent_duplicate.sql`: Trigger de prevenção de duplicados (BEFORE INSERT).
- `trigger_auditoria.sql`: Exemplo de trigger de auditoria (FORNECIDO).
- `requirements.txt`: dependências com versões fixas.
- `run.sh`: script que cria `.venv`, instala dependências e roda Streamlit.

----

## Como empacotar / gerar ZIP de entrega

No diretório do projeto:

```bash
zip -r consultorio_medico_submission.zip . -x "*.git*" 
```

----

## Casos de teste rápidos (resumo)

1. Importar dump e verificar `SELECT COUNT(*) FROM tabelapaciente;` retorna > 0.
2. Inserir paciente via UI → verificar SELECT.
3. Atualizar paciente via UI → verificar alteração no DB.
4. Inserir consulta duplicada (mesmo `CodMed` e `Data_Hora`) → trigger impede (erro SQLSTATE 45000).
5. Inserir consulta com `CodCli` inexistente → erro de FK.

----

Se quiser, posso:

- Gerar um `docker-compose.yml` que sobe MySQL + app Streamlit automaticamente (bônus).
- Implementar forms mais completos para `médicos` e `clínicas` (CRUD total).
- Criar testes automatizados simples (pytest) cobrindo inserção e leitura via SQLAlchemy.

---

Contato/Créditos
- Integrantes: preencher manualmente
- Disciplina: Banco de Dados
- Data: Novembro/2025

"""
├── db.py                       # Conexão MySQL
├── config.py                   # Configurações
├── requirements.txt            # Dependências
├── .env.example               # Template de variáveis
├── .env                       # Variáveis reais (não commitar)
├── README.md                  # Este arquivo
├── Dump20251128.sql           # Dump do banco
├── trigger_auditoria.sql      # Script dos triggers
├── Dockerfile                 # Docker (opcional)
├── docker-compose.yml         # Docker compose (opcional)
├── pages/
│   ├── __init__.py
│   ├── home.py               # Dashboard
│   ├── pacientes.py          # CRUD Pacientes
│   ├── medicos.py            # CRUD Médicos
│   ├── clinicas.py           # CRUD Clínicas
│   └── consultas.py          # CRUD Consultas
└── tests/
    └── test_cases.md         # Casos de teste
```

---

## 🔧 Solução de Problemas

### Erro: "Access denied for user"
- Verifique usuário e senha no arquivo `.env`
- Confirme que o MySQL está rodando: `mysql -u root -p`

### Erro: "Unknown database"
- Certifique-se de ter criado o banco: `CREATE DATABASE consultoriomedico;`
- Importe o dump novamente

### Erro: "Module not found"
- Ative o ambiente virtual: `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)
- Reinstale dependências: `pip install -r requirements.txt`

### Aplicação não carrega
- Verifique se a porta 8050 está livre
- Tente acessar http://127.0.0.1:8050 em vez de localhost

### Triggers não funcionam
- Verifique se foram criados: `SHOW TRIGGERS FROM consultoriomedico;`
- Reaplique o script: `mysql -u root -p consultoriomedico < trigger_auditoria.sql`

---

## 👥 Créditos

**Integrantes:**
1. [Nome Integrante 1] - Responsável por: Dashboard e documentação
2. [Nome Integrante 2] - Responsável por: CRUD e banco de dados
3. [Nome Integrante 3] - Responsável por: Triggers e testes

**Instituição:** [Nome da Instituição]  
**Disciplina:** Banco de Dados  
**Professor:** [Nome do Professor]  
**Data:** Novembro/2025

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos.