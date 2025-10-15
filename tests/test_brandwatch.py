import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from app.infra.brandwatch_client import BrandwatchClient


def test_alerta_exemplo_brandwatch(capsys):
    """
    Teste real: busca um alerta de exemplo na Brandwatch usando filtro conforme bcr-api.
    """
    load_dotenv()
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path and not cred_path.startswith(".."):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"..{cred_path}"

    bw_email = os.getenv("BW_EMAIL")
    bw_password = os.getenv("BW_PASSWORD")
    bw_project = os.getenv("BW_PROJECT")
    bw_query_name = os.getenv("BW_QUERY_NAME")  # Usar o nome da query conforme bcr-api

    assert bw_email, "BW_EMAIL não está definido no ambiente."
    assert bw_password, "BW_PASSWORD não está definido no ambiente."
    assert bw_project, "BW_PROJECT não está definido no ambiente."
    assert bw_query_name, "BW_QUERY_NAME não está definido no ambiente."

    # Exemplo: alerta do dia 06/10/2025 às 08h50
    end_local = datetime(2025, 10, 6, 8, 50, tzinfo=ZoneInfo("America/Sao_Paulo"))
    start_local = end_local - timedelta(hours=24)
    start_utc = start_local.astimezone(ZoneInfo("UTC"))
    end_utc = end_local.astimezone(ZoneInfo("UTC"))

    link = "https://www.agazeta.com.br/brasil/lei-magnitsky-quem-tem-conta-no-banco-do-brasil-nao-corre-risco-de-perder-dinheiro-1025"

    print("==== Janela de busca (UTC) ====")
    print("start_utc:", start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("end_utc  :", end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))

    bw = BrandwatchClient()
    # Filtro para buscar menções que contenham o link
    filters = {
        "url": link
    }
    mentions = bw.get_filtered_mentions(
        query_name=bw_query_name,
        start_datetime=start_utc,
        end_datetime=end_utc,
        filters=filters,
        limit=10
    )

    print("\n--- LINK ---------------------------------------")
    print(link)

    if not mentions:
        print("found      : False")
        assert False, "Nenhuma menção localizada para o alerta de exemplo no período informado."
    else:
        print("found      : True")
        for mention in mentions:
            print("guid       :", mention.get("guid"))
            print("resource   :", mention.get("resourceType"))
            print("pageType   :", mention.get("pageType"))
            print("date       :", mention.get("date"))
            print("queryId    :", mention.get("queryId"))
            print("queryName  :", mention.get("queryName"))
            print("url        :", mention.get("url"))
            cats = BrandwatchClient.extract_categories(mention)
            names = [c.get("name") for c in cats.get("categoryDetails")]
            print("categories :", cats.get("categories"))
            print("cat_names  :", names)
            print("cat_metrics:", cats.get("categoryMetrics"))

    capsys.readouterr()
