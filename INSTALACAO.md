# 🚀 Guia de Instalação - Sistema Consultório Médico

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **MySQL 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
3. **Git** (opcional) - [Download Git](https://git-scm.com/downloads)

---

## 📥 Passo 1: Obter o Código

### Opção A: Clonar com Git
```bash
git clone https://github.com/theoserrano/consultoriomedico.git
cd consultoriomedico/consultoriomedico
```

### Opção B: Download ZIP
1. Baixe o arquivo ZIP do repositório
2. Extraia em uma pasta de sua preferência
3. Navegue até a pasta `consultoriomedico/consultoriomedico`

---

## 🗄️ Passo 2: Configurar o Banco de Dados MySQL

### 2.1 Criar o Banco de Dados

Abra o MySQL Workbench ou o terminal MySQL e execute:

```sql
CREATE DATABASE consultoriomedico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2.2 Criar as Tabelas

Execute o script SQL fornecido:

```bash
# No terminal MySQL
USE consultoriomedico;
SOURCE consultoriomedio.sql;
```

Ou no MySQL Workbench:
- File → Open SQL Script
- Selecione o arquivo `consultoriomedio.sql`
- Execute o script (⚡ ícone de raio)

---

## ⚙️ Passo 3: Configurar Variáveis de Ambiente

### 3.1 Criar arquivo .env

Copie o arquivo de exemplo:

```bash
# Windows (PowerShell)
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 3.2 Editar o arquivo .env

Abra o arquivo `.env` com um editor de texto e configure suas credenciais:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=SUA_SENHA_MYSQL_AQUI  # ← ALTERE AQUI!
DB_NAME=consultoriomedico
DB_USE_SQLITE_FALLBACK=false
```

> ⚠️ **IMPORTANTE**: Substitua `SUA_SENHA_MYSQL_AQUI` pela senha do seu usuário MySQL!

---

## 📦 Passo 4: Instalar Dependências Python

Abra o terminal na pasta do projeto e execute:

```bash
# Windows
pip install -r requirements.txt

# Linux/Mac (pode precisar de pip3)
pip3 install -r requirements.txt
```

**Dependências instaladas:**
- `dash` - Framework web
- `dash-bootstrap-components` - Componentes UI
- `plotly` - Gráficos interativos
- `mysql-connector-python` - Conexão MySQL
- `pandas` - Manipulação de dados
- `python-dotenv` - Gerenciamento de variáveis de ambiente
- `faker` - Geração de dados artificiais

---

## 🎲 Passo 5: Popular o Banco com Dados de Teste (Opcional)

Para ter dados de demonstração:

```bash
python populate_mysql.py
```

Isso irá criar:
- ~200 pacientes
- ~80 médicos
- ~12 clínicas
- ~1500 consultas

---

## ▶️ Passo 6: Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em: **http://127.0.0.1:8050/**

---

## 🌐 Navegação do Sistema

Após iniciar, você terá acesso a:

- **🏠 Início** - Dashboard com KPIs e gráficos
- **👥 Pacientes** - Gerenciar pacientes (CRUD completo)
- **⚕️ Médicos** - Gerenciar médicos (CRUD completo)
- **🏥 Clínicas** - Gerenciar clínicas (CRUD completo)
- **📅 Consultas** - Gerenciar consultas (CRUD completo)
- **📊 Analytics** - Análises avançadas e visualizações

---

## 🔧 Solução de Problemas

### Erro: "Access denied for user"
- Verifique se a senha no `.env` está correta
- Confirme que o usuário tem permissões no banco
```sql
GRANT ALL PRIVILEGES ON consultoriomedico.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Erro: "Unknown database"
- Certifique-se de ter criado o banco: `CREATE DATABASE consultoriomedico;`
- Verifique se o nome no `.env` está correto

### Erro: "Can't connect to MySQL server"
- Verifique se o MySQL está rodando
- Confirme host e porta no `.env`

### Erro: "Module not found"
- Reinstale as dependências: `pip install -r requirements.txt`

### Porta 8050 já em uso
- Pare outras instâncias do Dash
- Ou altere a porta em `app.py`: `app.run_server(debug=True, port=8051)`

---

## 🔒 Segurança

### Para Uso em Produção:

1. **Nunca commit o arquivo .env**
   - Já está no `.gitignore`
   - Use variáveis de ambiente do servidor

2. **Mude o secret key do Dash**
   - Adicione em `app.py`: `server.secret_key = 'sua-chave-secreta-aqui'`

3. **Desabilite modo debug**
   - Em `app.py`: `app.run_server(debug=False)`

4. **Use HTTPS em produção**
   - Configure um reverse proxy (Nginx/Apache)
   - Obtenha certificado SSL (Let's Encrypt)

5. **Crie usuário MySQL específico**
```sql
CREATE USER 'consultorio_user'@'localhost' IDENTIFIED BY 'senha_forte';
GRANT SELECT, INSERT, UPDATE, DELETE ON consultoriomedico.* TO 'consultorio_user'@'localhost';
```

---

## 📝 Estrutura de Arquivos

```
consultoriomedico/
├── consultoriomedico/
│   ├── app.py                    # Aplicação principal
│   ├── db.py                     # Gerenciamento de banco de dados
│   ├── config.py                 # Configurações
│   ├── .env                      # Credenciais (NÃO COMMITAR)
│   ├── .env.example              # Exemplo de configuração
│   ├── requirements.txt          # Dependências Python
│   ├── consultoriomedio.sql      # Schema do banco
│   ├── populate_mysql.py         # Script de dados de teste
│   ├── pages/
│   │   ├── home.py               # Dashboard principal
│   │   ├── pacientes.py          # Gestão de pacientes
│   │   ├── medicos.py            # Gestão de médicos
│   │   ├── clinicas.py           # Gestão de clínicas
│   │   ├── consultas.py          # Gestão de consultas
│   │   └── analytics.py          # Análises e relatórios
│   └── assets/
│       └── styles.css            # Estilos customizados
└── README.md
```

---

## 🆘 Suporte

Problemas ou dúvidas?
- Abra uma issue no GitHub
- Consulte a documentação do MySQL: https://dev.mysql.com/doc/
- Documentação do Dash: https://dash.plotly.com/

---

## 📄 Licença

Este projeto é de código aberto. Sinta-se livre para usar e modificar conforme necessário.

---

**Desenvolvido com ❤️ usando Python e Dash**
