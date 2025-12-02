# 💻 Exemplos de Operações CRUD - NoSQL

> Sistema de Consultório Médico
> 
> Banco NoSQL: **[DEFINIR: MongoDB/Redis/Cassandra/etc]**

---

## 📋 Estrutura dos Dados

### Entidades Principais:
- **Pacientes**: CPF, Nome, Data Nascimento, Gênero, Telefone, Email
- **Médicos**: Código, Nome, Gênero, Telefone, Email, Especialidade
- **Clínicas**: Código, Nome, Endereço, Telefone, Email
- **Consultas**: Paciente, Médico, Clínica, Data/Hora, Observações

---

## ✏️ CREATE - Inserção de Dados

### 1. Criar Paciente

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]
// Exemplo para MongoDB:
db.pacientes.insertOne({
  _id: "12345678900",
  nome: "João Silva",
  data_nascimento: "1990-05-15",
  genero: "M",
  contato: {
    telefone: "(11) 98765-4321",
    email: "joao.silva@email.com"
  }
})
```

**MySQL Equivalente:**
```sql
INSERT INTO tabelapaciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email)
VALUES ('12345678900', 'João Silva', '1990-05-15', 'M', '(11) 98765-4321', 'joao.silva@email.com');
```

**Comparação:**
- NoSQL: [PREENCHER VANTAGENS/DESVANTAGENS]
- MySQL: [PREENCHER VANTAGENS/DESVANTAGENS]

---

### 2. Criar Médico

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
INSERT INTO tabelamedico (CodMed, NomeMed, Genero, Telefone, Email, Especialidade)
VALUES ('1234567', 'Dra. Maria Santos', 'F', '(11) 3456-7890', 'maria.santos@clinica.com', 'Cardiologia');
```

---

### 3. Criar Clínica

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
INSERT INTO tabelaclinica (CodCli, NomeCli, Endereco, Telefone, Email)
VALUES ('628169', 'Clínica MedCare', 'Rua das Flores, 123', '(11) 3000-0000', 'contato@medcare.com');
```

---

### 4. Criar Consulta

#### Opção A: Embedded (Todos os dados em um documento)

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]
// Exemplo MongoDB com dados embedded:
db.consultas.insertOne({
  data_hora: ISODate("2024-12-02T14:30:00Z"),
  status: "agendada",
  paciente: {
    cpf: "12345678900",
    nome: "João Silva",
    email: "joao.silva@email.com"
  },
  medico: {
    codigo: "1234567",
    nome: "Dra. Maria Santos",
    especialidade: "Cardiologia"
  },
  clinica: {
    codigo: "628169",
    nome: "Clínica MedCare",
    endereco: "Rua das Flores, 123"
  },
  observacoes: "Consulta de rotina - Checkup anual",
  valor: 250.00
})
```

#### Opção B: Referências (Separado em coleções)

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]
// Exemplo MongoDB com referências:
db.consultas.insertOne({
  data_hora: ISODate("2024-12-02T14:30:00Z"),
  paciente_id: "12345678900",
  medico_id: "1234567",
  clinica_id: "628169",
  status: "agendada",
  observacoes: "Consulta de rotina - Checkup anual",
  valor: 250.00
})
```

**MySQL Equivalente:**
```sql
INSERT INTO tabelaconsulta (CpfPaciente, CodMed, CodCli, Data_Hora)
VALUES ('12345678900', '1234567', '628169', '2024-12-02 14:30:00');
```

**Comparação:**
- **Embedded**: [VANTAGENS - 1 query / DESVANTAGENS - redundância]
- **Referências**: [VANTAGENS - normalização / DESVANTAGENS - múltiplas queries]
- **MySQL**: [VANTAGENS - integridade referencial / DESVANTAGENS - joins]

---

## 📖 READ - Consulta de Dados

### 1. Buscar Todos os Pacientes

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
SELECT * FROM tabelapaciente ORDER BY NomePac;
```

---

### 2. Buscar Paciente por CPF

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
SELECT * FROM tabelapaciente WHERE CpfPaciente = '12345678900';
```

---

### 3. Buscar Médicos por Especialidade

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
SELECT * FROM tabelamedico WHERE Especialidade = 'Cardiologia' ORDER BY NomeMed;
```

---

### 4. Buscar Consultas com Dados Completos

#### Se usar Embedded:

**NoSQL:**
```javascript
// [PREENCHER - Query simples, dados já estão embedded]

```

#### Se usar Referências:

**NoSQL:**
```javascript
// [PREENCHER - Query com lookup/join]
// Exemplo MongoDB:
db.consultas.aggregate([
  {
    $lookup: {
      from: "pacientes",
      localField: "paciente_id",
      foreignField: "_id",
      as: "paciente"
    }
  },
  {
    $lookup: {
      from: "medicos",
      localField: "medico_id",
      foreignField: "_id",
      as: "medico"
    }
  },
  {
    $lookup: {
      from: "clinicas",
      localField: "clinica_id",
      foreignField: "_id",
      as: "clinica"
    }
  }
])
```

**MySQL Equivalente:**
```sql
SELECT 
    c.Data_Hora,
    p.CpfPaciente, p.NomePac, p.Email as EmailPaciente,
    m.CodMed, m.NomeMed, m.Especialidade,
    cl.CodCli, cl.NomeCli, cl.Endereco
FROM tabelaconsulta c
INNER JOIN tabelapaciente p ON c.CpfPaciente = p.CpfPaciente
INNER JOIN tabelamedico m ON c.CodMed = m.CodMed
INNER JOIN tabelaclinica cl ON c.CodCli = cl.CodCli
ORDER BY c.Data_Hora DESC;
```

**Comparação:**
- **Embedded**: 1 query simples vs MySQL precisa de 3 JOINs
- **Referências**: Ambos precisam de operações de join/lookup
- **Desempenho**: [ANALISAR na prática]

---

### 5. Buscar Consultas por Período

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
SELECT * FROM tabelaconsulta 
WHERE Data_Hora BETWEEN '2024-12-01' AND '2024-12-31'
ORDER BY Data_Hora;
```

---

### 6. Buscar Consultas de um Médico Específico

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
SELECT c.*, p.NomePac, m.NomeMed, cl.NomeCli
FROM tabelaconsulta c
INNER JOIN tabelapaciente p ON c.CpfPaciente = p.CpfPaciente
INNER JOIN tabelamedico m ON c.CodMed = m.CodMed
INNER JOIN tabelaclinica cl ON c.CodCli = cl.CodCli
WHERE m.CodMed = '1234567'
ORDER BY c.Data_Hora DESC;
```

---

### 7. Agregação: Contar Consultas por Especialidade

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]
// Exemplo MongoDB (embedded):
db.consultas.aggregate([
  {
    $group: {
      _id: "$medico.especialidade",
      total: { $sum: 1 }
    }
  },
  { $sort: { total: -1 } }
])
```

**MySQL Equivalente:**
```sql
SELECT m.Especialidade, COUNT(*) as Total
FROM tabelaconsulta c
INNER JOIN tabelamedico m ON c.CodMed = m.CodMed
GROUP BY m.Especialidade
ORDER BY Total DESC;
```

---

## 🔄 UPDATE - Atualização de Dados

### 1. Atualizar Email do Paciente

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
UPDATE tabelapaciente 
SET Email = 'joao.silva.novo@email.com'
WHERE CpfPaciente = '12345678900';
```

---

### 2. Atualizar Especialidade do Médico

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
UPDATE tabelamedico 
SET Especialidade = 'Cardiologia Pediátrica'
WHERE CodMed = '1234567';
```

---

### 3. Atualizar Status da Consulta

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
-- Nota: MySQL não tem campo 'status' na consulta, mas seria:
UPDATE tabelaconsulta 
SET Status = 'realizada'
WHERE CpfPaciente = '12345678900' 
  AND CodMed = '1234567' 
  AND Data_Hora = '2024-12-02 14:30:00';
```

---

### 4. Atualizar Documento Embedded (se aplicável)

**NoSQL:**
```javascript
// [PREENCHER - Atualizar email do médico dentro da consulta embedded]

```

**Comparação:**
- **Embedded**: [ANALISAR - precisa atualizar em múltiplos documentos?]
- **Referências**: [ANALISAR - atualiza só na coleção original]
- **MySQL**: [ANALISAR - atualiza só na tabela original]

---

## 🗑️ DELETE - Remoção de Dados

### 1. Deletar Paciente

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
DELETE FROM tabelapaciente WHERE CpfPaciente = '12345678900';
-- Nota: Falhará se houver consultas (FK constraint)
```

---

### 2. Deletar Consulta

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
DELETE FROM tabelaconsulta 
WHERE CpfPaciente = '12345678900' 
  AND CodMed = '1234567' 
  AND Data_Hora = '2024-12-02 14:30:00';
```

---

### 3. Deletar Consultas por Período

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
DELETE FROM tabelaconsulta 
WHERE Data_Hora < '2024-01-01';
```

---

### 4. Integridade Referencial

**Como o NoSQL trata?**
- [PREENCHER - Depende se é embedded ou referências]
- Embedded: [Dados órfãos?]
- Referências: [Cascade? Manual?]

**MySQL:**
- Foreign Keys garantem integridade
- Opções: CASCADE, RESTRICT, SET NULL

---

## 🔍 Queries Complexas com Relacionamentos

### 1. Top 5 Médicos com Mais Consultas

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
SELECT m.NomeMed, m.Especialidade, COUNT(*) as TotalConsultas
FROM tabelaconsulta c
INNER JOIN tabelamedico m ON c.CodMed = m.CodMed
GROUP BY m.CodMed, m.NomeMed, m.Especialidade
ORDER BY TotalConsultas DESC
LIMIT 5;
```

---

### 2. Consultas de Cardiologia no Último Mês

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
SELECT c.Data_Hora, p.NomePac, m.NomeMed, cl.NomeCli
FROM tabelaconsulta c
INNER JOIN tabelapaciente p ON c.CpfPaciente = p.CpfPaciente
INNER JOIN tabelamedico m ON c.CodMed = m.CodMed
INNER JOIN tabelaclinica cl ON c.CodCli = cl.CodCli
WHERE m.Especialidade = 'Cardiologia'
  AND c.Data_Hora >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
ORDER BY c.Data_Hora DESC;
```

---

### 3. Pacientes que Consultaram em Múltiplas Clínicas

**NoSQL:**
```javascript
// [PREENCHER COM COMANDO DO BANCO ESCOLHIDO]

```

**MySQL Equivalente:**
```sql
SELECT p.NomePac, COUNT(DISTINCT c.CodCli) as NumClinicas
FROM tabelaconsulta c
INNER JOIN tabelapaciente p ON c.CpfPaciente = p.CpfPaciente
GROUP BY p.CpfPaciente, p.NomePac
HAVING COUNT(DISTINCT c.CodCli) > 1
ORDER BY NumClinicas DESC;
```

---

## 📊 Resumo Comparativo

| Operação | NoSQL | MySQL | Vencedor |
|----------|-------|-------|----------|
| **CREATE** - Insert simples | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| **READ** - Busca por ID | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| **READ** - Query com relacionamentos | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| **UPDATE** - Registro único | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| **UPDATE** - Em massa | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| **DELETE** - Registro único | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| **Agregações** | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| **Integridade Referencial** | [PREENCHER] | [PREENCHER] | [PREENCHER] |

---

## 🎯 Conclusões

### Vantagens do NoSQL:
1. [PREENCHER após implementação]
2. [PREENCHER após implementação]
3. [PREENCHER após implementação]

### Desvantagens do NoSQL:
1. [PREENCHER após implementação]
2. [PREENCHER após implementação]
3. [PREENCHER após implementação]

### Vantagens do MySQL:
1. [PREENCHER após implementação]
2. [PREENCHER após implementação]
3. [PREENCHER após implementação]

### Desvantagens do MySQL:
1. [PREENCHER após implementação]
2. [PREENCHER após implementação]
3. [PREENCHER após implementação]

### Quando Usar Cada Um?

**Use NoSQL quando:**
- [PREENCHER]

**Use MySQL quando:**
- [PREENCHER]

---

## 📝 Notas de Implementação

### Desafios Encontrados:
- [PREENCHER durante implementação]

### Soluções Aplicadas:
- [PREENCHER durante implementação]

### Aprendizados:
- [PREENCHER durante implementação]

---

**Última Atualização**: [DATA]
**Banco NoSQL**: [NOME E VERSÃO]
**Responsável**: [NOME DA EQUIPE]
