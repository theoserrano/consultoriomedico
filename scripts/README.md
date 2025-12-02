# 🔧 Scripts Auxiliares

Scripts para instalação, população de dados e demonstrações.

## 📋 Scripts Disponíveis

### `setup_nosql.py`
Script para instalação e configuração inicial do banco NoSQL.

**Uso:**
```bash
python scripts/setup_nosql.py
```

### `populate_nosql.py`
Popula o banco NoSQL com dados de exemplo ou migra do MySQL.

**Uso:**
```bash
python scripts/populate_nosql.py --source mysql
```

### `comparativo_crud.py`
Script de demonstração que compara operações CRUD entre MySQL e NoSQL.

**Uso:**
```bash
python scripts/comparativo_crud.py
```

## 🎯 Ordem de Execução

1. `setup_nosql.py` - Configurar o banco
2. `populate_nosql.py` - Popular com dados
3. `comparativo_crud.py` - Testar e comparar operações
