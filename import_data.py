import pandas as pd
import os
from app import create_app
from app.infra.database import db
from app.models.alert import Alert
from app.enums.mailing_status import MailingStatus
from app.enums.criticality_level import CriticalityLevel
from app.enums.alert_type import AlertType
from app.enums.critical_topic import CriticalTopic
from app.enums.press_source import PressSource
from app.enums.social_media_source import SocialMediaSource
from app.enums.social_media_engagement import SocialMediaEngagement
from app.enums.repercussion import Repercussion
from app.enums.alert_category import AlertCategory
from app.enums.alert_subcategory import AlertSubcategory
from app.enums.stakeholders import Stakeholders

def transform_to_pg_array(value):
    if pd.isna(value) or value in ('[]', ''):
        return []
    if isinstance(value, str):
        value = value.strip()
        if value.startswith('[') and value.endswith(']'):
            content = value[1:-1]
            items = content.split(',')
            clean_items = [item.strip().replace('"', '') for item in items if item.strip()]
            return clean_items
    return []

def import_data():
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
            
            # Converte strings para Enums
            alert_data['mailing_status'] = MailingStatus.from_name(alert_data.get('mailing_status'))
            alert_data['criticality_level'] = CriticalityLevel.from_name(alert_data.get('criticality_level'))
            if alert_data.get('alert_types'):
                alert_data['alert_types'] = [AlertType.from_name(at) for at in alert_data['alert_types']]
            if alert_data.get('critical_topic'):
                alert_data['critical_topic'] = [CriticalTopic.from_name(ct) for ct in alert_data['critical_topic']]
            if alert_data.get('press_sources'):
                alert_data['press_sources'] = [PressSource.from_name(ps) for ps in alert_data['press_sources']]
            if alert_data.get('social_media_sources'):
                alert_data['social_media_sources'] = [SocialMediaSource.from_name(sms) for sms in alert_data['social_media_sources']]
            if alert_data.get('social_media_engagements'):
                alert_data['social_media_engagements'] = [SocialMediaEngagement.from_name(sme) for sme in alert_data['social_media_engagements']]
            if alert_data.get('repercussions'):
                alert_data['repercussions'] = [Repercussion.from_name(r) for r in alert_data['repercussions']]
            if alert_data.get('stakeholders'):
                alert_data['stakeholders'] = [Stakeholders.from_name(s) for s in alert_data['stakeholders']]
            if alert_data.get('subcategories'):
                alert_data['subcategories'] = [AlertSubcategory.from_name(sc) for sc in alert_data['subcategories']]
            if alert_data.get('categories'):
                alert_data['categories'] = [AlertCategory.from_name(c) for c in alert_data['categories']]

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
