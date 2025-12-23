import os
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, make_transient
from app.models.user import User
from app.models.mailing import Mailing
from app.models.alert import Alert

# Lista de modelos para copiar
MODELS_TO_COPY = [User, Mailing, Alert]

def get_db_url(env_file):
    """Lê o arquivo .env e monta a string de conexão do PostgreSQL."""
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"Arquivo {env_file} não encontrado.")
    
    config = dotenv_values(env_file)
    
    required_keys = ['DB_USER', 'DB_PASS', 'DB_HOST', 'DB_NAME']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Chave {key} não encontrada em {env_file}")

    return f"postgresql://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_HOST']}:5432/{config['DB_NAME']}"

def copy_data():
    print("--- Iniciando Cópia de Dados: PROD (Leitura) -> DEV (Escrita) ---")

    # 1. Configurar Conexão de Origem (PROD) - APENAS LEITURA
    try:
        prod_url = get_db_url('.env_prod')
        print(f"Conectando em PROD (Origem)...")
        # isolation_level="READ UNCOMMITTED" pode ajudar na performance de leitura
        engine_source = create_engine(prod_url) 
        SessionSource = sessionmaker(bind=engine_source)
        session_source = SessionSource()
    except Exception as e:
        print(f"Erro ao conectar em PROD: {e}")
        return

    # 2. Configurar Conexão de Destino (DEV) - ESCRITA
    try:
        dev_url = get_db_url('.env_dev')
        print(f"Conectando em DEV (Destino)...")
        engine_target = create_engine(dev_url)
        SessionTarget = sessionmaker(bind=engine_target)
        session_target = SessionTarget()
    except Exception as e:
        print(f"Erro ao conectar em DEV: {e}")
        return

    # 3. Processo de Cópia
    for model in MODELS_TO_COPY:
        table_name = model.__tablename__
        print(f"\nProcessando tabela: {table_name}")

        try:
            # Ler dados de PROD (Origem)
            # Apenas consultas são feitas na session_source
            records = session_source.query(model).all()
            total = len(records)
            print(f"  - Lidos {total} registros de PROD.")

            if total == 0:
                continue

            count = 0
            for record in records:
                # Desvincula o objeto da sessão de origem (PROD)
                session_source.expunge(record)
                
                # Remove o estado de persistência do objeto, tornando-o "novo"
                make_transient(record)
                
                # Insere ou atualiza na sessão de destino (DEV)
                session_target.merge(record)
                
                count += 1
                if count % 100 == 0:
                    print(f"  - Processados {count}/{total}...")

            # Commit APENAS na sessão de destino (DEV)
            session_target.commit()
            print(f"  - Sucesso! {count} registros gravados em DEV.")

        except Exception as e:
            session_target.rollback() # Rollback apenas no destino em caso de erro
            print(f"  - Erro ao copiar tabela {table_name}: {e}")

    # Fechar sessões
    # NUNCA chamamos commit() na session_source
    session_source.close() 
    session_target.close()
    print("\n--- Cópia Finalizada ---")

if __name__ == "__main__":
    copy_data()
