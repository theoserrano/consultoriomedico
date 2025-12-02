# 📦 Módulo NoSQL

Este módulo contém toda a implementação da integração com o banco de dados NoSQL escolhido.

## 📁 Estrutura

- `config_nosql.py` - Configurações de conexão e parâmetros
- `db_nosql.py` - Classe de conexão e gerenciamento do banco NoSQL
- `models_nosql.py` - Modelos e schemas dos documentos/coleções
- `crud_operations.py` - Implementação das operações CRUD
- `migration.py` - Script para migrar dados do MySQL para NoSQL

## 🚀 Como Usar

```python
from nosql.db_nosql import NoSQLDatabase

# Conectar ao banco
db = NoSQLDatabase()
db.connect()

# Realizar operações CRUD
# (ver exemplos em crud_operations.py)
```

## 📝 Próximos Passos

1. Escolher o banco NoSQL (MongoDB recomendado)
2. Implementar `config_nosql.py` com as configurações
3. Implementar `db_nosql.py` com a classe de conexão
4. Definir modelos em `models_nosql.py`
5. Implementar operações CRUD em `crud_operations.py`
6. Criar script de migração em `migration.py`
