# 📋 Planejamento: Integração NoSQL ao Sistema de Consultório Médico

## 🎯 Objetivo do Projeto
Implementar um banco de dados NoSQL em paralelo ao MySQL existente, demonstrando operações CRUD e comparando as abordagens relacional vs. não-relacional para dados de consultas médicas.

---

## 🗂️ Estrutura de Dados Atual (MySQL)

### Tabelas Existentes:
1. **tabelapaciente** - Informações dos pacientes (CPF, Nome, Data Nascimento, Gênero, Telefone, Email)
2. **tabelamedico** - Informações dos médicos (CodMed, Nome, Gênero, Telefone, Email, Especialidade)
3. **tabelaclinica** - Informações das clínicas (CodCli, Nome, Endereço, Telefone, Email)
4. **tabelaconsulta** - Registro de consultas (CodCli, CodMed, CpfPaciente, Data_Hora)

### Relacionamentos MySQL:
```
tabelaconsulta ─┬─> tabelapaciente (CpfPaciente)
                ├─> tabelamedico (CodMed)
                └─> tabelaclinica (CodCli)
```

---

## 🔧 Opções de Bancos NoSQL (Escolher 1)

### Recomendações por Tipo:

#### 1. **MongoDB** (Orientado a Documentos) ⭐ RECOMENDADO
- **Vantagens**: 
  - Muito popular e bem documentado
  - Queries flexíveis e expressivas
  - Embedding e referências para relacionamentos
  - Facilidade de instalação (MongoDB Community ou Atlas Cloud)
- **Uso**: Ideal para armazenar consultas completas com dados embedded de paciente/médico/clínica

#### 2. **Redis** (Chave-Valor com estruturas)
- **Vantagens**:
  - Extremamente rápido
  - Suporta Hash, Lists, Sets, Sorted Sets
  - Bom para cache e dados em tempo real
- **Uso**: Cache de consultas recentes, filas de agendamento

#### 3. **Cassandra** (Orientado a Colunas)
- **Vantagens**:
  - Altamente escalável
  - Excelente para grandes volumes
  - Wide-column store
- **Uso**: Histórico massivo de consultas

#### 4. **Neo4j** (Orientado a Grafos)
- **Vantagens**:
  - Excelente para relacionamentos complexos
  - Queries Cypher muito intuitivas
- **Uso**: Rede de referências médico-paciente-clínica

---

## 📊 Modelagem NoSQL Proposta

### Opção A: MongoDB (Embedded Documents)

```javascript
// Coleção: consultas
{
  "_id": ObjectId("..."),
  "data_hora": ISODate("2024-12-02T14:30:00Z"),
  "status": "realizada",
  
  // Dados do paciente embedded
  "paciente": {
    "cpf": "12345678900",
    "nome": "João Silva",
    "data_nascimento": "1990-05-15",
    "genero": "M",
    "telefone": "(11) 98765-4321",
    "email": "joao@email.com"
  },
  
  // Dados do médico embedded
  "medico": {
    "codigo": "1234567",
    "nome": "Dra. Maria Santos",
    "especialidade": "Cardiologia",
    "telefone": "(11) 3456-7890",
    "email": "maria@clinica.com"
  },
  
  // Dados da clínica embedded
  "clinica": {
    "codigo": "628169",
    "nome": "Clínica MedCare",
    "endereco": "Rua das Flores, 123",
    "telefone": "(11) 3000-0000",
    "email": "contato@medcare.com"
  },
  
  // Informações adicionais da consulta
  "observacoes": "Consulta de rotina",
  "valor": 250.00,
  "forma_pagamento": "Plano de Saúde",
  "created_at": ISODate("2024-11-28T10:00:00Z"),
  "updated_at": ISODate("2024-12-02T14:35:00Z")
}
```

### Opção B: MongoDB (Referências)

```javascript
// Coleção: pacientes
{
  "_id": "12345678900",  // CPF como _id
  "nome": "João Silva",
  "data_nascimento": "1990-05-15",
  "genero": "M",
  "contato": {
    "telefone": "(11) 98765-4321",
    "email": "joao@email.com"
  }
}

// Coleção: medicos
{
  "_id": "1234567",  // CodMed como _id
  "nome": "Dra. Maria Santos",
  "especialidade": "Cardiologia",
  "contato": {
    "telefone": "(11) 3456-7890",
    "email": "maria@clinica.com"
  }
}

// Coleção: clinicas
{
  "_id": "628169",  // CodCli como _id
  "nome": "Clínica MedCare",
  "endereco": "Rua das Flores, 123",
  "contato": {
    "telefone": "(11) 3000-0000",
    "email": "contato@medcare.com"
  }
}

// Coleção: consultas (com referências)
{
  "_id": ObjectId("..."),
  "data_hora": ISODate("2024-12-02T14:30:00Z"),
  "paciente_id": "12345678900",      // Referência
  "medico_id": "1234567",             // Referência
  "clinica_id": "628169",             // Referência
  "status": "realizada",
  "observacoes": "Consulta de rotina",
  "valor": 250.00
}
```

---

## 🛠️ Estrutura de Arquivos a Criar

```
consultoriomedico/
├── nosql/
│   ├── __init__.py
│   ├── config_nosql.py          # Configurações do banco NoSQL
│   ├── db_nosql.py               # Classe de conexão NoSQL
│   ├── models_nosql.py           # Modelos/schemas NoSQL
│   ├── crud_operations.py        # Operações CRUD
│   └── migration.py              # Script para migrar dados MySQL -> NoSQL
│
├── scripts/
│   ├── setup_nosql.py            # Script de instalação/setup
│   ├── populate_nosql.py         # Popular dados no NoSQL
│   └── comparativo_crud.py       # Comparar operações MySQL vs NoSQL
│
├── pages/
│   ├── nosql_demo.py             # Nova página no dashboard para demo NoSQL
│   └── comparativo.py            # Página comparativa MySQL vs NoSQL
│
├── docs/
│   ├── INSTALACAO_NOSQL.md       # Guia de instalação do banco NoSQL
│   ├── MODELAGEM_NOSQL.md        # Documentação da modelagem
│   ├── EXEMPLOS_CRUD.md          # Exemplos de operações CRUD
│   └── COMPARATIVO.md            # Comparativo MySQL vs NoSQL
│
├── diagrams/
│   ├── modelagem_mysql.png       # DER do MySQL (já existe implicitamente)
│   └── modelagem_nosql.png       # Diagrama da modelagem NoSQL
│
└── requirements_nosql.txt        # Dependências adicionais para NoSQL
```

---

## 📝 Tarefas Práticas a Implementar

### 1. **Configuração Inicial**
- [ ] Escolher o banco NoSQL (MongoDB recomendado)
- [ ] Instalar o banco localmente
- [ ] Criar arquivo de configuração
- [ ] Documentar processo de instalação

### 2. **Implementação da Conexão**
- [ ] Criar classe de conexão NoSQL
- [ ] Implementar tratamento de erros
- [ ] Testar conectividade

### 3. **Definir Modelagem**
- [ ] Definir estrutura dos documentos/coleções
- [ ] Criar diagramas de modelagem conceitual
- [ ] Documentar relacionamentos
- [ ] Comparar com modelagem MySQL (DER)

### 4. **Operações CRUD - CREATE**
- [ ] Implementar inserção de pacientes
- [ ] Implementar inserção de médicos
- [ ] Implementar inserção de clínicas
- [ ] Implementar inserção de consultas
- [ ] Criar exemplos práticos com dados reais
- [ ] Comparar com INSERT do MySQL

### 5. **Operações CRUD - READ**
- [ ] Buscar todos os registros
- [ ] Buscar por filtros específicos
- [ ] Buscar com relacionamentos (joins/lookups/embedded)
- [ ] Implementar agregações
- [ ] Criar exemplos práticos
- [ ] Comparar com SELECT do MySQL

### 6. **Operações CRUD - UPDATE**
- [ ] Atualizar registros individuais
- [ ] Atualizar múltiplos registros
- [ ] Atualizar documentos embedded
- [ ] Criar exemplos práticos
- [ ] Comparar com UPDATE do MySQL

### 7. **Operações CRUD - DELETE**
- [ ] Deletar registros individuais
- [ ] Deletar múltiplos registros
- [ ] Tratar integridade referencial
- [ ] Criar exemplos práticos
- [ ] Comparar com DELETE do MySQL

### 8. **Queries com Relacionamentos**
- [ ] Listar consultas com dados do paciente
- [ ] Listar consultas com dados do médico
- [ ] Listar consultas completas (paciente + médico + clínica)
- [ ] Consultas por especialidade
- [ ] Consultas por período
- [ ] Consultas por clínica
- [ ] Comparar com JOINs do MySQL

### 9. **Script de Migração**
- [ ] Criar script para migrar dados do MySQL para NoSQL
- [ ] Validar integridade dos dados migrados
- [ ] Testar com dados de exemplo

### 10. **Interface no Dashboard**
- [ ] Criar página de demonstração NoSQL
- [ ] Adicionar formulários para operações CRUD
- [ ] Mostrar resultados em tempo real
- [ ] Implementar página comparativa

### 11. **Documentação**
- [ ] Guia de instalação detalhado
- [ ] Documentação da modelagem com diagramas
- [ ] Exemplos de todos os comandos CRUD
- [ ] Tabela comparativa MySQL vs NoSQL
- [ ] Casos de uso e vantagens de cada abordagem

---

## 🎬 Roteiro para Apresentação (10 min)

### 1. Introdução (1 min)
- Apresentação da equipe
- Banco NoSQL escolhido
- Objetivo: Consultas Médicas

### 2. Instalação/Configuração (1 min)
- Passo a passo resumido
- Screenshots principais
- Comandos essenciais

### 3. Modelagem Conceitual (2 min)
- Mostrar diagrama NoSQL
- Comparar com DER do MySQL
- Explicar relacionamentos no NoSQL
- Vantagens da modelagem escolhida

### 4. CRUD - CREATE (1.5 min)
- Comandos ao vivo: criar paciente, médico, clínica, consulta
- Comparar com INSERT do MySQL
- Mostrar dados inseridos

### 5. CRUD - READ (1.5 min)
- Comandos ao vivo: buscar consultas
- Query com relacionamentos (embedded/lookup/join)
- Comparar com SELECT+JOIN do MySQL

### 6. CRUD - UPDATE (1.5 min)
- Comandos ao vivo: atualizar consulta
- Atualizar dados embedded
- Comparar com UPDATE do MySQL

### 7. CRUD - DELETE (1 min)
- Comandos ao vivo: deletar consulta
- Tratar integridade referencial
- Comparar com DELETE do MySQL

### 8. Queries Complexas com Relacionamentos (1 min)
- Consultas por especialidade
- Consultas por período
- Agregações
- Mostrar diferença no desempenho

### 9. Conclusão (0.5 min)
- Vantagens e desvantagens observadas
- Quando usar cada tipo de banco
- Perguntas

---

## 📊 Comparativo MySQL vs NoSQL

### Aspectos a Comparar:

| Aspecto | MySQL (Relacional) | NoSQL (Escolhido) |
|---------|-------------------|-------------------|
| **Estrutura** | Tabelas com schema fixo | Documentos/Coleções flexíveis |
| **Relacionamentos** | Foreign Keys (FK) | Embedding ou Referências |
| **CRUD Syntax** | SQL (INSERT, SELECT, etc.) | API específica (find, insertOne, etc.) |
| **Joins** | JOIN nativo | Lookup/Population ou Embedding |
| **Escalabilidade** | Vertical (scale-up) | Horizontal (scale-out) |
| **Transações** | ACID completo | Depende do banco |
| **Flexibilidade** | Schema rígido | Schema dinâmico |
| **Desempenho** | Bom para consultas complexas | Bom para reads simples e writes |

---

## 🎨 Modelagem Visual a Criar

### 1. Diagrama MySQL (DER)
```
┌─────────────────┐
│ tabelapaciente  │
├─────────────────┤
│ CpfPaciente PK  │───┐
│ NomePac         │   │
│ DataNascimento  │   │
│ Genero          │   │
│ ...             │   │
└─────────────────┘   │
                      │
┌─────────────────┐   │    ┌─────────────────┐
│ tabelamedico    │   │    │ tabelaclinica   │
├─────────────────┤   │    ├─────────────────┤
│ CodMed PK       │───┼────│ CodCli PK       │
│ NomeMed         │   │    │ NomeCli         │
│ Especialidade   │   │    │ Endereco        │
│ ...             │   │    │ ...             │
└─────────────────┘   │    └─────────────────┘
         │            │             │
         │            │             │
         └────────────┼─────────────┘
                      │
              ┌───────▼────────┐
              │ tabelaconsulta │
              ├────────────────┤
              │ CpfPaciente FK │
              │ CodMed FK      │
              │ CodCli FK      │
              │ Data_Hora      │
              └────────────────┘
```

### 2. Diagrama NoSQL (MongoDB - Embedded)
```
┌────────────────────────────────────────────┐
│         Coleção: consultas                 │
├────────────────────────────────────────────┤
│ {                                          │
│   "_id": ObjectId,                         │
│   "data_hora": Date,                       │
│   "status": String,                        │
│   "paciente": {            ◄─── Embedded   │
│     "cpf": String,                         │
│     "nome": String,                        │
│     "data_nascimento": String,             │
│     ...                                    │
│   },                                       │
│   "medico": {              ◄─── Embedded   │
│     "codigo": String,                      │
│     "nome": String,                        │
│     "especialidade": String,               │
│     ...                                    │
│   },                                       │
│   "clinica": {             ◄─── Embedded   │
│     "codigo": String,                      │
│     "nome": String,                        │
│     "endereco": String,                    │
│     ...                                    │
│   }                                        │
│ }                                          │
└────────────────────────────────────────────┘

Vantagem: 1 única query para obter todos os dados!
```

### 3. Diagrama NoSQL (MongoDB - Referências)
```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   pacientes  │         │   medicos    │         │   clinicas   │
├──────────────┤         ├──────────────┤         ├──────────────┤
│ _id (CPF)    │         │ _id (Cod)    │         │ _id (Cod)    │
│ nome         │         │ nome         │         │ nome         │
│ ...          │         │ especialidade│         │ endereco     │
└──────────────┘         └──────────────┘         └──────────────┘
       ▲                        ▲                        ▲
       │                        │                        │
       │   Referências          │                        │
       │   (lookup)             │                        │
       │                        │                        │
┌──────┴────────────────────────┴────────────────────────┴──────┐
│                    Coleção: consultas                          │
├────────────────────────────────────────────────────────────────┤
│ {                                                              │
│   "_id": ObjectId,                                             │
│   "paciente_id": "12345678900",  ◄─── Referência               │
│   "medico_id": "1234567",        ◄─── Referência               │
│   "clinica_id": "628169",        ◄─── Referência               │
│   "data_hora": Date,                                           │
│   ...                                                          │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘

Requer: $lookup (aggregate) para juntar dados
Similar a: JOIN do MySQL
```

---

## 💡 Exemplos de Queries Comparativas

### Exemplo 1: Buscar Consulta Completa

**MySQL (com JOINs):**
```sql
SELECT 
    c.Data_Hora,
    p.NomePac, p.CpfPaciente, p.Email as EmailPaciente,
    m.NomeMed, m.Especialidade, m.Email as EmailMedico,
    cl.NomeCli, cl.Endereco, cl.Telefone as TelefoneCli
FROM tabelaconsulta c
INNER JOIN tabelapaciente p ON c.CpfPaciente = p.CpfPaciente
INNER JOIN tabelamedico m ON c.CodMed = m.CodMed
INNER JOIN tabelaclinica cl ON c.CodCli = cl.CodCli
WHERE c.Data_Hora > '2024-12-01'
ORDER BY c.Data_Hora DESC;
```

**MongoDB (Embedded - 1 query):**
```javascript
db.consultas.find({
  "data_hora": { $gt: ISODate("2024-12-01") }
}).sort({ "data_hora": -1 })
```

**MongoDB (Referências - com lookup):**
```javascript
db.consultas.aggregate([
  { $match: { "data_hora": { $gt: ISODate("2024-12-01") } } },
  { $lookup: {
      from: "pacientes",
      localField: "paciente_id",
      foreignField: "_id",
      as: "paciente"
  }},
  { $lookup: {
      from: "medicos",
      localField: "medico_id",
      foreignField: "_id",
      as: "medico"
  }},
  { $lookup: {
      from: "clinicas",
      localField: "clinica_id",
      foreignField: "_id",
      as: "clinica"
  }},
  { $sort: { "data_hora": -1 } }
])
```

---

## 🚀 Próximos Passos Imediatos

1. **Decisão**: Escolher qual banco NoSQL usar
2. **Instalação**: Instalar localmente e documentar
3. **Estruturação**: Criar pasta `nosql/` com arquivos base
4. **Modelagem**: Definir exatamente como serão os documentos/coleções
5. **CRUD Básico**: Implementar operações básicas
6. **Migração**: Criar script para popular com dados do MySQL
7. **Demonstração**: Criar página no dashboard para mostrar operações
8. **Documentação**: Documentar tudo para a apresentação

---

## 📌 Observações Importantes

- ✅ Foco em HANDS-ON: mostrar comandos sendo executados, não prints
- ✅ Todos os exemplos baseados em "Consultas Médicas"
- ✅ Comparar SEMPRE com MySQL equivalente
- ✅ Mostrar modelagem conceitual com diagramas
- ✅ Explicar como funcionam os relacionamentos no NoSQL
- ✅ Não se estender na instalação (máximo 1 minuto)
- ✅ Priorizar demonstração prática das operações CRUD

---

## 🎯 Entregáveis Finais

1. **Código Funcional**: Sistema rodando com MySQL + NoSQL
2. **Scripts CRUD**: Todos os exemplos de operações
3. **Documentação**: Markdown completo com comandos
4. **Diagramas**: Modelagem visual comparativa
5. **Script de Migração**: Dados MySQL → NoSQL
6. **Interface Demo**: Página no dashboard para demonstração
7. **Apresentação**: 10 minutos focada em prática

---

**Status**: 📋 Planejamento Estruturado - Aguardando Escolha do Banco NoSQL
