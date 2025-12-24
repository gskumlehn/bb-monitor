import os
from dotenv import dotenv_values
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, make_transient
from sqlalchemy.exc import ProgrammingError, OperationalError
from app.models.user import User
from app.models.mailing import Mailing
from app.models.alert import Alert

# Mapeamento de modelos para seus respectivos bancos de dados
MODEL_DB_MAP = {
    User: 'ADMIN_DB_NAME',
    Mailing: None,
    Alert: None
}

def get_db_config(env_file):
    """Lê o arquivo .env e retorna um dicionário com as configurações."""
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"Arquivo {env_file} não encontrado.")
    
    config = dotenv_values(env_file)
    required_keys = ['DB_USER', 'DB_PASS', 'DB_HOST', 'DB_NAME']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Chave {key} não encontrada em {env_file}")
    return config

def get_connection_url(config, db_name):
    return f"postgresql://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_HOST']}:5432/{db_name}"

def create_database_if_not_exists(config, target_db_name):
    """Conecta ao banco administrativo para criar o banco de destino se não existir."""
    admin_dbs = ['postgres', 'template1']
    engine = None
    
    for admin_db in admin_dbs:
        try:
            url = get_connection_url(config, admin_db)
            print(f"  -> Tentando conectar ao banco administrativo '{admin_db}'...")
            engine = create_engine(url, isolation_level="AUTOCOMMIT")
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            break 
        except OperationalError:
            engine = None
    
    if not engine:
        raise Exception("Não foi possível conectar a nenhum banco administrativo (postgres, template1).")

    with engine.connect() as conn:
        exists = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{target_db_name}'")).scalar()
        if not exists:
            print(f"  -> Criando banco de dados '{target_db_name}'...")
            conn.execute(text(f'CREATE DATABASE "{target_db_name}"'))
        else:
            print(f"  -> Banco de dados '{target_db_name}' já existe.")
    engine.dispose()

def setup_local_structure(dev_config):
    """Cria bancos, schemas e tabelas no ambiente local (DEV)."""
    print("\n--- Configurando Estrutura Local (DEV) ---")
    
    dbs_to_create = {dev_config['DB_NAME']}
    if dev_config.get('ADMIN_DB_NAME'):
        dbs_to_create.add(dev_config['ADMIN_DB_NAME'])

    for db_name in dbs_to_create:
        create_database_if_not_exists(dev_config, db_name)

    for model, db_key in MODEL_DB_MAP.items():
        target_db_name = dev_config.get(db_key) if db_key else dev_config['DB_NAME']
        engine = create_engine(get_connection_url(dev_config, target_db_name))
        
        table_args = getattr(model, '__table_args__', {})
        schema_name = table_args.get('schema')
        
        with engine.connect() as conn:
            if schema_name:
                # Removida a condição que impedia a criação do schema 'public'
                if not engine.dialect.has_schema(conn, schema_name):
                    print(f"  -> Criando schema '{schema_name}' no banco '{target_db_name}'...")
                    conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"'))
                    conn.commit()
            
            print(f"  -> Verificando/Criando tabela '{model.__tablename__}' no schema '{schema_name or 'default'}'...")
            model.metadata.create_all(engine)
        
        engine.dispose()

def copy_data():
    try:
        prod_config = get_db_config('.env_prod')
        dev_config = get_db_config('.env_dev')
    except Exception as e:
        print(f"Erro ao ler configurações: {e}")
        return

    setup_local_structure(dev_config)

    print("\n--- Iniciando Cópia de Dados: PROD (Leitura) -> DEV (Escrita) ---")

    engines_source = {}
    engines_target = {}

    def get_engines(model):
        db_key = MODEL_DB_MAP.get(model)
        prod_db = prod_config.get(db_key) if db_key else prod_config['DB_NAME']
        dev_db = dev_config.get(db_key) if db_key else dev_config['DB_NAME']
        conn_id = db_key if db_key else 'DEFAULT'

        if conn_id not in engines_source:
            engines_source[conn_id] = create_engine(get_connection_url(prod_config, prod_db))
        if conn_id not in engines_target:
            engines_target[conn_id] = create_engine(get_connection_url(dev_config, dev_db))
            
        return engines_source[conn_id], engines_target[conn_id]

    for model in MODEL_DB_MAP.keys():
        table_name = model.__tablename__
        print(f"\nProcessando dados da tabela: {table_name}")

        try:
            engine_source, engine_target = get_engines(model)
            SessionSource = sessionmaker(bind=engine_source)
            SessionTarget = sessionmaker(bind=engine_target)
            session_source = SessionSource()
            session_target = SessionTarget()

            try:
                records = session_source.query(model).all()
            except ProgrammingError:
                print(f"  - Aviso: Tabela '{table_name}' não encontrada em PROD. Pulando.")
                session_source.rollback()
                continue

            total = len(records)
            print(f"  - Lidos {total} registros de PROD.")
            if total == 0: continue

            for record in records:
                session_source.expunge(record)
                make_transient(record)
                session_target.merge(record)

            session_target.commit()
            print(f"  - Sucesso! {total} registros gravados em DEV.")

        except Exception as e:
            if 'session_target' in locals(): session_target.rollback()
            print(f"  - Erro ao copiar dados de {table_name}: {e}")
        finally:
            if 'session_source' in locals(): session_source.close()
            if 'session_target' in locals(): session_target.close()

    print("\n--- Processo Finalizado ---")

if __name__ == "__main__":
    copy_data()
