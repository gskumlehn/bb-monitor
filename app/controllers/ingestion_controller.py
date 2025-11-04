from flask import Blueprint, jsonify, render_template, request
from app.services.ingestion_service import IngestionService

ingestion_bp = Blueprint("ingestion", __name__)

ingestion_service = IngestionService()

@ingestion_bp.get("/ui")
def index():
    return render_template("ingestion.html")

@ingestion_bp.route("/ingest", methods=["POST"])
def ingest():
    try:
        row = request.json.get("row")
        start_row = request.json.get("start_row")
        end_row = request.json.get("end_row")

        if row is not None:
            start_row = end_row = row
        elif start_row is None or end_row is None:
            return jsonify({"error": "Os parâmetros 'start_row' e 'end_row' são obrigatórios se 'row' não for fornecido."}), 400

        result = ingestion_service.ingest(start_row, end_row)

        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Erro ao executar a ingestão.", "details": str(e)}), 500
