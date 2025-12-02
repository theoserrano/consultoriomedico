#!/usr/bin/env python3
"""
Script de teste de conexão Firebase
Valida que o Firebase está configurado corretamente e não interfere com MySQL
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def test_firebase_connection():
    """Testa conexão com Firebase"""
    print("=" * 60)
    print("🔥 TESTE DE CONEXÃO FIREBASE")
    print("=" * 60)
    
    try:
        from nosql.db_nosql import FirebaseDatabase
        
        print("\n1️⃣ Importação dos módulos... ✅")
        
        # Tenta conectar
        print("\n2️⃣ Tentando conectar ao Firebase...")
        db = FirebaseDatabase()
        
        if db.connect():
            print("   ✅ Conexão bem-sucedida!")
            
            # Testa operação básica
            print("\n3️⃣ Testando operação básica (count)...")
            try:
                count = db.count_documents('pacientes')
                print(f"   ✅ Total de pacientes no Firestore: {count}")
            except Exception as e:
                print(f"   ⚠️  Aviso: {e}")
                print("   (Isso é normal se ainda não houve migração)")
            
            print("\n" + "=" * 60)
            print("✅ FIREBASE ESTÁ CONFIGURADO E FUNCIONANDO!")
            print("=" * 60)
            return True
        else:
            print("   ❌ Falha na conexão")
            return False
            
    except FileNotFoundError as e:
        print(f"\n❌ ERRO: Arquivo de credenciais não encontrado")
        print(f"   {e}")
        print("\n📝 Ações necessárias:")
        print("   1. Crie um projeto no Firebase Console")
        print("   2. Baixe o arquivo firebase-credentials.json")
        print("   3. Coloque-o na raiz do projeto")
        print("   4. Configure o .env com FIREBASE_CREDENTIALS_PATH")
        return False
        
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mysql_still_works():
    """Verifica que MySQL ainda funciona (não foi afetado)"""
    print("\n" + "=" * 60)
    print("🗄️  TESTE DE INTEGRIDADE MYSQL")
    print("=" * 60)
    
    try:
        from db import get_db_connection
        
        print("\n1️⃣ Importação do módulo MySQL... ✅")
        
        print("\n2️⃣ Tentando conectar ao MySQL...")
        conn = get_db_connection()
        
        if conn:
            print("   ✅ Conexão MySQL bem-sucedida!")
            
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tabelapaciente")
            count = cursor.fetchone()[0]
            print(f"   ✅ Total de pacientes no MySQL: {count}")
            
            conn.close()
            
            print("\n" + "=" * 60)
            print("✅ MYSQL CONTINUA FUNCIONANDO NORMALMENTE!")
            print("=" * 60)
            return True
        else:
            print("   ⚠️  MySQL não conectado (configure .env)")
            return False
            
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa todos os testes"""
    print("\n🧪 INICIANDO TESTES DE INTEGRAÇÃO\n")
    
    # Teste 1: Firebase
    firebase_ok = test_firebase_connection()
    
    # Teste 2: MySQL (verificar que não foi afetado)
    mysql_ok = test_mysql_still_works()
    
    # Resultado final
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL DOS TESTES")
    print("=" * 60)
    print(f"Firebase: {'✅ OK' if firebase_ok else '❌ FALHOU'}")
    print(f"MySQL:    {'✅ OK' if mysql_ok else '⚠️  Não configurado/disponível'}")
    
    if firebase_ok and mysql_ok:
        print("\n🎉 SUCESSO! Ambos os bancos estão funcionando!")
        print("   - Firebase configurado corretamente")
        print("   - MySQL não foi afetado pela integração")
        print("\n📝 Próximos passos:")
        print("   1. Execute: python -m nosql.migration --migrar-tudo")
        print("   2. Teste os scripts de demonstração")
        print("   3. Acesse a interface web para demonstração")
    elif firebase_ok:
        print("\n⚠️  Firebase OK, mas MySQL precisa de configuração")
        print("   Configure o MySQL no .env para testes completos")
    else:
        print("\n❌ Firebase precisa de configuração")
        print("   Siga o guia: docs/INSTALACAO_NOSQL.md")
    
    print("=" * 60 + "\n")
    
    return 0 if firebase_ok else 1

if __name__ == "__main__":
    sys.exit(main())
