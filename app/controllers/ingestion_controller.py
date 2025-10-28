from flask import Blueprint, jsonify, request, render_template
from app.services.ingestion_service import IngestionService

ingestion_bp = Blueprint("ingestion", __name__)

@ingestion_bp.route("/ingest", methods=["POST"])
def ingest():
    try:
        row = request.json.get("row")
        if row is None:
            return jsonify({"error": "O parâmetro 'row' é obrigatório."}), 400

        ingestion_service = IngestionService()
        alerts = ingestion_service.ingest(row)
        return jsonify({"message": "Ingestão concluída com sucesso.", "alerts": [alert.urls for alert in alerts]}), 200
    except Exception as e:
        return jsonify({"error": "Erro ao executar a ingestão.", "details": str(e)}), 500

@ingestion_bp.route("/ui", methods=["GET"])
def index():
    return render_template("ingestion.html")
