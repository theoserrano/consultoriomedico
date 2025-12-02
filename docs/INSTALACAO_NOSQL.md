# 🔥 Guia de Instalação - Firebase Firestore

> Sistema de Consultório Médico - Integração NoSQL

---

## 📋 O Que é Firebase Firestore?

Firebase Firestore é um banco de dados NoSQL orientado a documentos, desenvolvido pelo Google. Características principais:

- **Orientado a Documentos**: Dados armazenados em documentos JSON-like
- **Coleções**: Documentos organizados em coleções (similar a tabelas)
- **Flexível**: Schema dinâmico, sem estrutura fixa
- **Tempo Real**: Suporta sincronização em tempo real
- **Escalável**: Escala horizontalmente automaticamente
- **Cloud ou Local**: Pode usar Firebase Cloud ou emulador local

---

## 🎯 Pré-requisitos

- Python 3.8+
- Conta Google (para Firebase Console)
- Projeto Firebase criado

---

## 📥 Passo 1: Criar Projeto no Firebase

### 1.1 Acessar Firebase Console

1. Acesse: https://console.firebase.google.com/
2. Faça login com sua conta Google
3. Clique em **"Adicionar projeto"**

### 1.2 Configurar Projeto

1. **Nome do projeto**: `consultorio-medico-nosql` (ou nome de sua escolha)
2. **Google Analytics**: Pode desabilitar (opcional para este projeto)
3. Clique em **"Criar projeto"**
4. Aguarde a criação (leva ~30 segundos)

### 1.3 Ativar Firestore

1. No menu lateral, clique em **"Firestore Database"**
2. Clique em **"Criar banco de dados"**
3. **Modo de produção** ou **Modo de teste**:
   - **Modo de teste**: Recomendado para desenvolvimento (acesso livre por 30 dias)
   - **Modo de produção**: Requer regras de segurança
4. **Localização**: Escolha uma próxima (ex: `southamerica-east1` para São Paulo)
5. Clique em **"Ativar"**

---

## 🔑 Passo 2: Obter Credenciais do Firebase

### 2.1 Criar Conta de Serviço

1. No Firebase Console, clique no ⚙️ (engrenagem) ao lado de "Visão geral do projeto"
2. Vá em **"Configurações do projeto"**
3. Clique na aba **"Contas de serviço"**
4. Clique em **"Gerar nova chave privada"**
5. Confirme clicando em **"Gerar chave"**
6. Um arquivo JSON será baixado automaticamente

### 2.2 Salvar Arquivo de Credenciais

1. Renomeie o arquivo baixado para: `firebase-credentials.json`
2. Mova para a pasta raiz do projeto:
   ```
   consultoriomedico/
   ├── firebase-credentials.json  ← Aqui!
   ├── app.py
   ├── requirements.txt
   └── ...
   ```

⚠️ **IMPORTANTE**: 
- **NUNCA** faça commit deste arquivo no Git
- Já está no `.gitignore` por segurança
- Guarde-o em local seguro

---

## 📦 Passo 3: Instalar Dependências Python

### 3.1 Instalar Bibliotecas Firebase

```bash
cd consultoriomedico
pip install -r requirements_nosql.txt
```

Isso instalará:
- `firebase-admin==6.5.0` - SDK Admin do Firebase
- `google-cloud-firestore==2.16.0` - Cliente Firestore

### 3.2 Verificar Instalação

```bash
python -c "import firebase_admin; print('Firebase instalado com sucesso!')"
```

---

## ⚙️ Passo 4: Configurar Variáveis de Ambiente (Opcional)

Você pode configurar opções no arquivo `.env`:

```env
# Caminho para credenciais Firebase
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json

# ID do projeto (opcional, será lido das credenciais)
FIREBASE_PROJECT_ID=consultorio-medico-nosql

# Modo de modelagem: 'embedded' ou 'referenced'
# embedded: dados completos em cada documento (recomendado)
# referenced: usa referências como MySQL FK
FIREBASE_MODELING_MODE=embedded

# Debug detalhado
FIREBASE_DEBUG=false
```

---

## 🧪 Passo 5: Testar Conexão

### 5.1 Criar Script de Teste

Crie um arquivo `test_firebase.py`:

```python
from nosql.db_nosql import firebase_db

# Tentar conectar
if firebase_db.connect():
    print("✓ Conectado ao Firestore com sucesso!")
    print(f"Projeto: {firebase_db.db.project}")
    
    # Testar criação de documento
    sucesso, msg = firebase_db.create_document(
        'test', 'doc1', {'teste': 'Hello Firestore!'}
    )
    
    if sucesso:
        print("✓ Documento de teste criado!")
        
        # Buscar documento
        doc = firebase_db.get_document('test', 'doc1')
        print(f"✓ Documento lido: {doc}")
        
        # Deletar documento
        firebase_db.delete_document('test', 'doc1')
        print("✓ Documento de teste deletado!")
    else:
        print(f"✗ Erro ao criar documento: {msg}")
else:
    print("✗ Erro ao conectar ao Firestore")
    print("Verifique se o arquivo firebase-credentials.json está correto")
```

### 5.2 Executar Teste

```bash
python test_firebase.py
```

**Saída esperada:**
```
✓ Conectado ao Firestore com sucesso!
Projeto: consultorio-medico-nosql
✓ Documento de teste criado!
✓ Documento lido: {'teste': 'Hello Firestore!', '_id': 'doc1'}
✓ Documento de teste deletado!
```

---

## 🔄 Passo 6: Migrar Dados do MySQL (Opcional)

Se você já tem dados no MySQL e quer migrá-los para Firestore:

```bash
# Migrar com limite de 100 consultas
python -m nosql.migration --limite-consultas 100

# Migrar tudo (pode demorar)
python -m nosql.migration --limite-consultas 0

# Com logs detalhados
python -m nosql.migration --debug
```

---

## 📊 Passo 7: Visualizar Dados no Console

1. Acesse https://console.firebase.google.com/
2. Selecione seu projeto
3. Vá em **"Firestore Database"**
4. Você verá as coleções criadas:
   - `pacientes`
   - `medicos`
   - `clinicas`
   - `consultas`
5. Clique em qualquer coleção para ver os documentos

---

## 🔧 Solução de Problemas

### Erro: "Arquivo de credenciais não encontrado"

**Causa**: Arquivo `firebase-credentials.json` não está no lugar certo.

**Solução**:
1. Verifique se o arquivo está na pasta raiz do projeto
2. Verifique o nome do arquivo (deve ser exatamente `firebase-credentials.json`)
3. Ou configure o caminho no `.env`:
   ```env
   FIREBASE_CREDENTIALS_PATH=/caminho/completo/para/firebase-credentials.json
   ```

---

### Erro: "Permission denied" ou "PERMISSION_DENIED"

**Causa**: Regras de segurança do Firestore bloqueando acesso.

**Solução**:
1. Acesse Firebase Console
2. Vá em **"Firestore Database"** → **"Regras"**
3. Para desenvolvimento, use regras permissivas:
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /{document=**} {
         allow read, write: if true;
       }
     }
   }
   ```
4. Clique em **"Publicar"**

⚠️ **ATENÇÃO**: Estas regras são inseguras! Use apenas em desenvolvimento.

---

### Erro: "Module 'firebase_admin' not found"

**Causa**: Dependências não instaladas.

**Solução**:
```bash
pip install -r requirements_nosql.txt
```

---

### Firestore muito lento ou timeout

**Causa**: Região do Firestore muito distante ou problemas de rede.

**Solução**:
1. Verifique sua conexão de internet
2. Considere usar região mais próxima (ao criar novo projeto)
3. Use emulador local para desenvolvimento:
   ```bash
   firebase emulators:start
   ```

---

## 🌐 Alternativa: Usar Emulador Local

Para desenvolvimento offline ou testes rápidos:

### 1. Instalar Firebase CLI

```bash
npm install -g firebase-tools
```

### 2. Inicializar Emulador

```bash
firebase init emulators
# Selecione: Firestore Emulator
```

### 3. Iniciar Emulador

```bash
firebase emulators:start
```

### 4. Configurar Python para Usar Emulador

```python
import os
os.environ['FIRESTORE_EMULATOR_HOST'] = 'localhost:8080'

from nosql.db_nosql import firebase_db
firebase_db.connect()
```

---

## 📚 Recursos Adicionais

### Documentação Oficial:
- **Firebase**: https://firebase.google.com/docs
- **Firestore**: https://firebase.google.com/docs/firestore
- **Python SDK**: https://firebase.google.com/docs/admin/setup

### Tutoriais:
- Introdução ao Firestore: https://firebase.google.com/docs/firestore/quickstart
- Modelagem de Dados: https://firebase.google.com/docs/firestore/data-model
- Queries: https://firebase.google.com/docs/firestore/query-data/queries

### Console Firebase:
- Firebase Console: https://console.firebase.google.com/
- Firestore Dashboard: Ver dados em tempo real

---

## ✅ Checklist de Instalação

- [ ] Conta Google criada
- [ ] Projeto Firebase criado
- [ ] Firestore Database ativado
- [ ] Arquivo `firebase-credentials.json` baixado
- [ ] Credenciais salvas na pasta do projeto
- [ ] Dependências Python instaladas (`pip install -r requirements_nosql.txt`)
- [ ] Teste de conexão executado com sucesso
- [ ] (Opcional) Dados migrados do MySQL
- [ ] (Opcional) Dados visualizados no Firebase Console

---

## 🎯 Próximos Passos

Agora que o Firebase está configurado:

1. Explore as operações CRUD em `nosql/crud_operations.py`
2. Veja exemplos em `docs/EXEMPLOS_CRUD.md`
3. Execute a migração de dados: `python -m nosql.migration`
4. Teste as queries: `python -m nosql.crud_operations`

---

**Firebase Firestore instalado e pronto para uso! 🎉**
