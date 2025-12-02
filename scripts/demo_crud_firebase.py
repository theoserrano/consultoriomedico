#!/usr/bin/env python3
"""
Script de demonstração CRUD completo com Firebase
Mostra exemplos práticos de Create, Read, Update, Delete
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from nosql.crud_operations import FirestoreCRUD
from nosql.db_nosql import FirebaseDatabase

def print_section(title):
    """Imprime um título de seção"""
    print("\n" + "=" * 70)
    print(f"📝 {title}")
    print("=" * 70)

def demo_criar_paciente():
    """Demonstra criação de paciente"""
    print_section("CREATE - Criando Novo Paciente")
    
    crud = FirestoreCRUD()
    
    # Dados do paciente de demonstração
    paciente_data = {
        'cpf': '99988877766',
        'nome': 'Ana Paula Oliveira',
        'data_nascimento': '1995-08-20',
        'genero': 'F',
        'telefone': '(11) 99999-8888',
        'email': 'ana.oliveira@email.com',
        'endereco': 'Rua das Palmeiras, 456',
        'cidade': 'São Paulo',
        'estado': 'SP'
    }
    
    print("\n📋 Dados do paciente:")
    for key, value in paciente_data.items():
        print(f"   {key}: {value}")
    
    print("\n⏳ Criando paciente no Firestore...")
    success, message, doc_id = crud.criar_paciente(paciente_data)
    
    if success:
        print(f"✅ {message}")
        print(f"   ID do documento: {doc_id}")
    else:
        print(f"❌ Erro: {message}")
    
    return paciente_data['cpf'] if success else None

def demo_buscar_paciente(cpf):
    """Demonstra busca de paciente"""
    print_section("READ - Buscando Paciente por CPF")
    
    crud = FirestoreCRUD()
    
    print(f"\n🔍 Buscando paciente com CPF: {cpf}")
    
    success, message, data = crud.buscar_paciente(cpf)
    
    if success:
        print(f"✅ {message}")
        print("\n📋 Dados encontrados:")
        for key, value in data.items():
            if key != 'document_id':
                print(f"   {key}: {value}")
    else:
        print(f"❌ {message}")
    
    return data if success else None

def demo_atualizar_paciente(cpf):
    """Demonstra atualização de paciente"""
    print_section("UPDATE - Atualizando Dados do Paciente")
    
    crud = FirestoreCRUD()
    
    # Dados para atualizar
    updates = {
        'telefone': '(11) 98888-7777',
        'email': 'ana.oliveira.novo@email.com',
        'endereco': 'Avenida Paulista, 1000 - Apto 501'
    }
    
    print(f"\n🔍 Atualizando paciente CPF: {cpf}")
    print("\n📝 Novos dados:")
    for key, value in updates.items():
        print(f"   {key}: {value}")
    
    print("\n⏳ Atualizando no Firestore...")
    success, message = crud.atualizar_paciente(cpf, updates)
    
    if success:
        print(f"✅ {message}")
        
        # Busca novamente para confirmar
        print("\n🔍 Confirmando atualização...")
        _, _, data = crud.buscar_paciente(cpf)
        if data:
            print("📋 Dados atualizados:")
            for key in updates.keys():
                print(f"   {key}: {data.get(key)}")
    else:
        print(f"❌ Erro: {message}")
    
    return success

def demo_criar_consulta(cpf_paciente):
    """Demonstra criação de consulta"""
    print_section("CREATE - Criando Nova Consulta")
    
    crud = FirestoreCRUD()
    
    # Dados da consulta
    consulta_data = {
        'cpf_paciente': cpf_paciente,
        'cod_medico': 'MED123',
        'cod_clinica': 'CLI456',
        'data_hora': (datetime.now() + timedelta(days=7)).isoformat(),
        'status': 'agendada',
        'especialidade': 'Cardiologia',
        'observacoes': 'Consulta de acompanhamento',
        'valor': 250.00
    }
    
    print("\n📋 Dados da consulta:")
    for key, value in consulta_data.items():
        print(f"   {key}: {value}")
    
    print("\n⏳ Criando consulta no Firestore...")
    success, message, doc_id = crud.criar_consulta(consulta_data)
    
    if success:
        print(f"✅ {message}")
        print(f"   ID da consulta: {doc_id}")
    else:
        print(f"❌ Erro: {message}")
    
    return doc_id if success else None

def demo_buscar_consultas(cpf_paciente):
    """Demonstra busca de consultas por paciente"""
    print_section("READ - Buscando Consultas do Paciente")
    
    crud = FirestoreCRUD()
    
    print(f"\n🔍 Buscando consultas do paciente CPF: {cpf_paciente}")
    
    success, message, consultas = crud.buscar_consultas_por_paciente(cpf_paciente)
    
    if success:
        print(f"✅ {message}")
        print(f"\n📊 Total de consultas encontradas: {len(consultas)}")
        
        if consultas:
            print("\n📋 Consultas:")
            for i, consulta in enumerate(consultas, 1):
                print(f"\n   Consulta {i}:")
                print(f"      ID: {consulta.get('document_id', 'N/A')}")
                print(f"      Data/Hora: {consulta.get('data_hora', 'N/A')}")
                print(f"      Status: {consulta.get('status', 'N/A')}")
                print(f"      Especialidade: {consulta.get('especialidade', 'N/A')}")
    else:
        print(f"❌ {message}")
    
    return consultas if success else []

def demo_deletar_paciente(cpf):
    """Demonstra exclusão de paciente"""
    print_section("DELETE - Deletando Paciente (Demonstração)")
    
    crud = FirestoreCRUD()
    
    print(f"\n⚠️  ATENÇÃO: Esta operação deletará o paciente CPF: {cpf}")
    print("   (Esta é apenas uma demonstração)")
    
    # Pergunta confirmação (em ambiente real)
    print("\n🔍 Verificando se paciente existe...")
    success, message, data = crud.buscar_paciente(cpf)
    
    if success and data:
        print(f"✅ Paciente encontrado: {data.get('nome')}")
        
        print("\n⏳ Deletando paciente do Firestore...")
        success_del, message_del = crud.deletar_paciente(cpf)
        
        if success_del:
            print(f"✅ {message_del}")
            
            # Verifica se foi realmente deletado
            print("\n🔍 Verificando exclusão...")
            success_check, _, data_check = crud.buscar_paciente(cpf)
            
            if not success_check or not data_check:
                print("✅ Confirmado: Paciente foi removido do banco")
            else:
                print("⚠️  Aviso: Paciente ainda aparece no banco")
        else:
            print(f"❌ Erro ao deletar: {message_del}")
    else:
        print(f"⚠️  {message}")

def demo_estatisticas():
    """Demonstra consultas agregadas e estatísticas"""
    print_section("ANALYTICS - Estatísticas e Agregações")
    
    crud = FirestoreCRUD()
    
    print("\n📊 Consultando estatísticas do Firestore...")
    
    # Total de documentos por coleção
    db = FirebaseDatabase()
    db.connect()
    
    collections = ['pacientes', 'medicos', 'clinicas', 'consultas']
    print("\n📈 Total de documentos por coleção:")
    for collection in collections:
        try:
            count = db.count_documents(collection)
            print(f"   {collection}: {count}")
        except Exception as e:
            print(f"   {collection}: ⚠️  Erro ao contar - {e}")
    
    # Consultas por especialidade
    print("\n🏥 Consultas por especialidade:")
    try:
        success, message, resultado = crud.contar_consultas_por_especialidade()
        if success and resultado:
            for esp, count in resultado.items():
                print(f"   {esp}: {count} consultas")
        else:
            print(f"   ⚠️  {message}")
    except Exception as e:
        print(f"   ⚠️  Erro: {e}")

def main():
    """Executa demonstração completa do CRUD"""
    print("\n" + "🔥" * 35)
    print("🔥 DEMONSTRAÇÃO COMPLETA FIREBASE CRUD 🔥")
    print("🔥" * 35)
    
    try:
        # Verifica conexão
        print("\n⏳ Verificando conexão com Firebase...")
        db = FirebaseDatabase()
        if not db.connect():
            print("❌ Erro: Não foi possível conectar ao Firebase")
            print("   Configure o Firebase seguindo: docs/INSTALACAO_NOSQL.md")
            return 1
        
        print("✅ Conectado ao Firebase!")
        
        # CREATE - Paciente
        cpf = demo_criar_paciente()
        
        if cpf:
            # READ - Paciente
            input("\n⏸️  Pressione ENTER para continuar com READ...")
            demo_buscar_paciente(cpf)
            
            # UPDATE - Paciente
            input("\n⏸️  Pressione ENTER para continuar com UPDATE...")
            demo_atualizar_paciente(cpf)
            
            # CREATE - Consulta
            input("\n⏸️  Pressione ENTER para criar uma CONSULTA...")
            demo_criar_consulta(cpf)
            
            # READ - Consultas
            input("\n⏸️  Pressione ENTER para buscar CONSULTAS...")
            demo_buscar_consultas(cpf)
            
            # ANALYTICS
            input("\n⏸️  Pressione ENTER para ver ESTATÍSTICAS...")
            demo_estatisticas()
            
            # DELETE - Paciente (opcional)
            input("\n⏸️  Pressione ENTER para DELETAR (demonstração)...")
            demo_deletar_paciente(cpf)
        
        # Resultado final
        print("\n" + "=" * 70)
        print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print("\n✅ Operações demonstradas:")
        print("   ✓ CREATE - Criar paciente e consulta")
        print("   ✓ READ   - Buscar por CPF e listar consultas")
        print("   ✓ UPDATE - Atualizar dados do paciente")
        print("   ✓ DELETE - Remover paciente do banco")
        print("   ✓ ANALYTICS - Estatísticas e agregações")
        
        print("\n📝 Próximos passos:")
        print("   1. Acesse a interface web: python app.py")
        print("   2. Execute a migração completa: python -m nosql.migration --migrar-tudo")
        print("   3. Explore os exemplos em: docs/EXEMPLOS_CRUD.md")
        
        print("\n" + "=" * 70 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstração interrompida pelo usuário")
        return 0
    except Exception as e:
        print(f"\n\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
