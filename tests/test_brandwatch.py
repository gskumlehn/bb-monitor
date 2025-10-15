import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from app.infra.brandwatch_client import BrandwatchClient


# -------------------- Helpers --------------------

def _window_utc_by_time_only(hora_str: str, end_local: datetime) -> tuple[datetime, datetime]:
    """
    Calcula a janela só com base no horário e na data/hora de envio (end_local).
    - início: (data de end_local + hora_str) - 45min (BRT)
    - fim   : end_local (BRT)
    """
    brt = ZoneInfo("America/Sao_Paulo")

    hh, mm = [int(x) for x in hora_str.strip().split(":")]
    base_local = end_local.replace(hour=hh, minute=mm, second=0, microsecond=0, tzinfo=brt)

    start_local = base_local - timedelta(minutes=45)

    start_utc = start_local.astimezone(ZoneInfo("UTC"))
    end_utc = end_local.astimezone(ZoneInfo("UTC"))

    return start_utc, end_utc


def _category_names(details):
    return [c.get("name") for c in (details or []) if isinstance(c, dict)]


def _mention_has_link(mention, link: str) -> bool:
    if not mention or not link:
        return False

    cands = []

    for k in ("url", "originalUrl"):
        if mention.get(k):
            cands.append(str(mention[k]).strip())

    for arr_k in ("expandedUrls", "displayUrls", "shortUrls", "mediaUrls"):
        arr = mention.get(arr_k) or []
        for u in arr:
            if u:
                cands.append(str(u).strip())

    return any(link == c or link in c for c in cands)


# -------------------- Mock Brandwatch --------------------

def _fake_mentions_payload():
    """
    Ajuste conforme seu cenário. Aqui simulamos:
    - um tweet com link externo nos expandedUrls
    - uma notícia com URL direta
    - ruído
    """
    return [
        {
            "resourceType": "twitter",
            "pageType": "twitter",
            "date": "2025-10-06T17:04:00.000+0000",  # 14:04 BRT
            "guid": "guid-x-001",
            "queryId": 2003603181,
            "queryName": "OPERAÇÃO BB :: MONITORAMENTO",
            "url": "https://x.com/user/status/1977782611306061964",
            "originalUrl": None,
            "expandedUrls": [
                "https://contrafcut.com.br/noticias/bb-mais-um-golpe-nos-funcionarios-do-varejo/"
            ],
            "displayUrls": [],
            "shortUrls": [],
            "mediaUrls": [],
            "categories": [24130283, 50001],
            "categoryDetails": [
                {"id": "24130283", "name": "Banco do Brasil", "parentName": "Marcas"},
                {"id": "50001", "name": "Pautas trabalhistas", "parentName": "Temas"},
            ],
            "categoryMetrics": {"count": 1},
        },
        {
            "resourceType": "news",
            "pageType": "news",
            "date": "2025-10-06T12:50:00.000+0000",  # ~09:50 BRT (apenas exemplo)
            "guid": "guid-news-123",
            "queryId": 2003603181,
            "queryName": "OPERAÇÃO BB :: MONITORAMENTO",
            "url": "https://www.agazeta.com.br/brasil/lei-magnitsky-quem-tem-conta-no-banco-do-brasil-nao-corre-risco-de-perder-dinheiro-1025",
            "originalUrl": None,
            "expandedUrls": [],
            "displayUrls": [],
            "shortUrls": [],
            "mediaUrls": [],
            "categories": [24130283, 333],
            "categoryDetails": [
                {"id": "24130283", "name": "Banco do Brasil", "parentName": "Marcas"},
                {"id": "333", "name": "Economia", "parentName": "Caderno"},
            ],
            "categoryMetrics": {"count": 1},
        },
        {
            "resourceType": "forum",
            "pageType": "forum",
            "date": "2025-10-06T13:10:00.000+0000",
            "guid": "guid-random-999",
            "queryId": 2003603181,
            "queryName": "OPERAÇÃO BB :: MONITORAMENTO",
            "url": "https://example.com/sem-relacao",
            "originalUrl": None,
            "expandedUrls": [],
            "displayUrls": [],
            "shortUrls": [],
            "mediaUrls": [],
            "categories": [],
            "categoryDetails": [],
            "categoryMetrics": {},
        },
    ]


@pytest.fixture(autouse=True)
def _env_defaults(monkeypatch):
    monkeypatch.setenv("BW_EMAIL", "test@brandwatch.local")
    monkeypatch.setenv("BW_PASSWORD", "secret")
    monkeypatch.setenv("BW_PROJECT", "project-id")
    monkeypatch.setenv("BW_QUERY_NAME", "OPERAÇÃO BB :: MONITORAMENTO")


@pytest.fixture
def _patch_client(monkeypatch):
    """
    Evita conexão real (neutraliza __init__) e injeta iter_mentions fake.
    """
    def _noop_init(self):
        return

    monkeypatch.setattr(BrandwatchClient, "__init__", _noop_init)

    fake_payload = _fake_mentions_payload()

    def _fake_iter(self, query_name, start_utc, end_utc, pagesize=5000):
        for m in fake_payload:
            yield m

    monkeypatch.setattr(BrandwatchClient, "iter_mentions", _fake_iter)

    return


# -------------------- Teste: usa SÓ horário + links --------------------

def test_lookup_by_time_and_links_only(_patch_client, capsys):
    """
    Você fornece:
      - hora_str (ex.: '14:04')
      - end_local (ex.: 14:45 do mesmo dia, vindo do scheduler)
      - links (lista)
    Calculamos a janela: [hora_str - 45min, end_local] e tentamos casar cada link.
    """
    hora_str = "14:04"

    end_local = datetime(2025, 10, 6, 14, 45, tzinfo=ZoneInfo("America/Sao_Paulo"))

    links = [
        "https://contrafcut.com.br/noticias/bb-mais-um-golpe-nos-funcionarios-do-varejo/",
        "https://www.agazeta.com.br/brasil/lei-magnitsky-quem-tem-conta-no-banco-do-brasil-nao-corre-risco-de-perder-dinheiro-1025",
        "https://nao-bate.com/path",
    ]

    start_utc, end_utc = _window_utc_by_time_only(hora_str, end_local)

    print("==== Janela de busca (UTC) ====")
    print("start_utc:", start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("end_utc  :", end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))

    bw = BrandwatchClient()
    found_any = False

    for link in links:
        mention = bw.get_first_match_in_window(
            query_name=os.getenv("BW_QUERY_NAME"),
            link=link,
            start_utc=start_utc,
            end_utc=end_utc,
        )

        print("\n--- LINK ---------------------------------------")
        print(link)

        if not mention:
            print("found      : False")
            continue

        found_any = True

        cats = BrandwatchClient.extract_categories(mention)
        names = _category_names(cats.get("categoryDetails"))

        print("found      : True")
        print("guid       :", mention.get("guid"))
        print("resource   :", mention.get("resourceType"))
        print("pageType   :", mention.get("pageType"))
        print("date       :", mention.get("date"))
        print("queryId    :", mention.get("queryId"))
        print("queryName  :", mention.get("queryName"))
        print("has_link?  :", _mention_has_link(mention, link))
        print("categories :", cats.get("categories"))
        print("cat_names  :", names)
        print("cat_metrics:", cats.get("categoryMetrics"))

    assert found_any is True, "Nenhuma menção localizada para os links informados na janela calculada."

    capsys.readouterr()
