from flask import Blueprint, jsonify
from app.services.ingestion_service import IngestionService

ingestion_bp = Blueprint("ingestion", __name__)

@ingestion_bp.route("/ingest", methods=["POST"])
def ingest():
    try:
        ingestion_service = IngestionService()
        alerts = ingestion_service.ingest()
        return jsonify({"message": "Ingestão concluída com sucesso.", "alerts": [alert.url for alert in alerts]}), 200
    except Exception as e:
        return jsonify({"error": "Erro ao executar a ingestão.", "details": str(e)}), 500
