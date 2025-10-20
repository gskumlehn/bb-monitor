import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from app.infra.brandwatch_client import BrandwatchClient

def test_alerta_exemplo_brandwatch(capsys):
    load_dotenv()
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path and not cred_path.startswith(".."):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"..{cred_path}"
    bw_email = os.getenv("BW_EMAIL")
    bw_password = os.getenv("BW_PASSWORD")
    bw_project = os.getenv("BW_PROJECT")
    bw_query_name = os.getenv("BW_QUERY_NAME")
    assert bw_email, "BW_EMAIL não está definido no ambiente."
    assert bw_password, "BW_PASSWORD não está definido no ambiente."
    assert bw_project, "BW_PROJECT não está definido no ambiente."
    assert bw_query_name, "BW_QUERY_NAME não está definido no ambiente."
    end_local = datetime(2025, 10, 16, 16, 30, tzinfo=ZoneInfo("America/Sao_Paulo"))
    start_local = datetime(2025, 10, 9, 0, 0, tzinfo=ZoneInfo("America/Sao_Paulo"))
    start_utc = start_local.astimezone(ZoneInfo("UTC"))
    end_utc = end_local.astimezone(ZoneInfo("UTC"))
    link = "https://g1.globo.com/mg/minas-gerais/noticia/2025/10/09/vereadores-de-bh-vao-ao-ccbb-com-guardas-e-pms-e-cobram-fechamento-de-exposicao.ghtml"
    print("==== Janela de busca (UTC) ====")
    print("start_utc:", start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("end_utc  :", end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))
    bw = BrandwatchClient()
    filters = {"url": link}
    mentions = bw.get_filtered_mentions(
        start_datetime=start_utc,
        end_datetime=end_utc,
        filters=filters,
        limit=500
    )
    print("\n--- LINK ---------------------------------------")
    print(link)
    if not mentions:
        print("found      : False")
        assert False, "Nenhuma menção localizada para o alerta de exemplo no período informado."
    exact = [m for m in mentions if m.get("url") == link or m.get("insightsUrl") == link]
    if not exact:
        print("found      : False")
        assert False, "Nenhuma menção com a URL exata localizada no período informado."
    print("found      : True")
    for mention in exact:
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
