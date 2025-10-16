from flask import Blueprint, jsonify
from app.services.alert_mailing_job_service import AlertMailingJobService

scheduler_bp = Blueprint("scheduler", __name__)

@scheduler_bp.route("/alert-mailing", methods=["POST"])
def alert_mailing():
    """
    Endpoint acionado pelo Cloud Scheduler para iniciar o processo:
    1. Busca na planilha Google.
    2. Busca na Brandwatch pela categoria.
    3. Envio do e-mail formatado.
    """
    try:
        job_service = AlertMailingJobService()
        results_sent = job_service.execute_scheduled_task()
        return jsonify({"message": "Processo concluído com sucesso.", "results_sent": results_sent}), 200
    except Exception as e:
        return jsonify({"error": "Erro ao executar a tarefa agendada.", "details": str(e)}), 500
