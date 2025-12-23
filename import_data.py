import pandas as pd
import os
from app import create_app
from app.infra.database import db
from app.models.alert import Alert

def transform_to_pg_array(value):
    """
    Transforma uma string como '[val1, val2]' em uma lista Python ['val1', 'val2'].
    O SQLAlchemy cuidará da conversão para o formato de array do PostgreSQL.
    """
    if pd.isna(value) or value in ('[]', ''):
        return []
    
    if isinstance(value, str):
        value = value.strip()
        if value.startswith('[') and value.endswith(']'):
            content = value[1:-1]
            items = content.split(',')
            
            clean_items = []
            for item in items:
                item = item.strip()
                if item:
                    # Remove aspas extras que possam estar no CSV, pois o SQLAlchemy adicionará as suas
                    item = item.replace('"', '')
                    clean_items.append(item)
            return clean_items
            
    return []

def import_data():
    """Lê o alerts.csv e importa os dados para a tabela 'alert' usando o modelo SQLAlchemy."""
    app = create_app()
    with app.app_context():
        project_root = os.path.dirname(app.root_path)
        csv_path = os.path.join(project_root, 'alerts.csv')

        print(f"Lendo dados de {csv_path}...")
        try:
            df = pd.read_csv(csv_path, parse_dates=['delivery_datetime'])
        except FileNotFoundError:
            print(f"Erro: Arquivo {csv_path} não encontrado.")
            return

        print("Transformando dados...")

        # Colunas de array
        array_columns = [
            'alert_types', 'critical_topic', 'press_sources', 'social_media_sources',
            'social_media_engagements', 'repercussions', 'stakeholders',
            'profiles_or_portals', 'urls', 'previous_alerts_ids',
            'subcategories', 'categories'
        ]

        for col in array_columns:
            if col in df.columns:
                df[col] = df[col].apply(transform_to_pg_array)

        if 'is_repercussion' in df.columns:
            df['is_repercussion'] = df['is_repercussion'].astype(bool)

        print("Inserindo dados no banco...")
        
        alerts_to_insert = []
        for _, row in df.iterrows():
            alert_data = row.to_dict()
            # Remove chaves que não estão no modelo (se houver)
            valid_keys = [c.key for c in Alert.__table__.columns]
            filtered_data = {k: v for k, v in alert_data.items() if k in valid_keys}
            
            alerts_to_insert.append(Alert(**filtered_data))

        try:
            db.session.bulk_save_objects(alerts_to_insert)
            db.session.commit()
            print(f"Importação concluída! {len(alerts_to_insert)} registros inseridos.")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao inserir dados: {e}")

if __name__ == '__main__':
    import_data()
