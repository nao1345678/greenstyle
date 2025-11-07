import os
import csv
import json
import time
import re
import argparse
from typing import Dict, Any, List, Optional

import requests
from dotenv import load_dotenv


load_dotenv()
SERP_API_KEY = os.getenv("SERPAPI_API_KEY")
SERP_ENDPOINT = "https://serpapi.com/search.json"

if not SERP_API_KEY:
    raise RuntimeError(" SERPAPI_API_KEY manquant. Ajoute-le dans .env")

def sleep_backoff(i: int):
    time.sleep(1 + min(i, 5) * 0.5)


def serp_search(q: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    base_params = {
        "engine": "google",
        "q": q,
        "api_key": SERP_API_KEY,
        "hl": "en",
        "gl": "us",
    }
    if params:
        base_params.update(params)
    resp = requests.get(SERP_ENDPOINT, params=base_params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def parse_knowledge_graph(j: Dict[str, Any]) -> Dict[str, Any]:
    kg = j.get("knowledge_graph") or {}
    return {
        "brand_name": kg.get("title"),
        "logo": kg.get("image") or kg.get("logo"),
        "website": kg.get("website"),
        "categories": kg.get("type") if isinstance(kg.get("type"), list) else [kg.get("type")] if kg.get("type") else [],
    }


def parse_organic_links(j: Dict[str, Any], domain_filters: Optional[List[str]] = None, limit: int = 5) -> List[str]:
    results = []
    for item in j.get("organic_results", []):
        link = item.get("link")
        if not link:
            continue
        if domain_filters:
            if any(df in link for df in domain_filters):
                results.append(link)
        else:
            results.append(link)
        if len(results) >= limit:
            break
    return results


COUNTRY_RE = re.compile(r"\b(USA|United States|United Kingdom|UK|France|Germany|Italy|Spain|Portugal|China|Vietnam|Bangladesh|India|Turkey|Cambodia|Tunisia|Morocco|Netherlands|Sweden|Norway|Denmark|Canada|Australia|New Zealand)\b", re.I)

def extract_country_from_snippets(j: Dict[str, Any]) -> Optional[str]:
    for k in ("answer_box", "knowledge_graph"):
        block = j.get(k)
        if isinstance(block, dict):
            text = " ".join(str(v) for v in block.values() if isinstance(v, (str, list, dict)))
            m = COUNTRY_RE.search(text)
            if m:
                return m.group(0)

    for item in j.get("organic_results", []):
        snippet = item.get("snippet") or ""
        m = COUNTRY_RE.search(snippet)
        if m:
            return m.group(0)
    return None


def extract_price_range_from_snippets(j: Dict[str, Any]) -> Optional[str]:
    """
    Essaie de repérer "$", "€", "£", ou des mentions type "price range", "€€", etc.
    On renvoie une chaîne courte (ex: "$$ - $$$" / "€€")
    """
    text_blobs = []

    for k in ("answer_box", "knowledge_graph"):
        block = j.get(k)
        if isinstance(block, dict):
            text_blobs.append(" ".join(str(v) for v in block.values() if isinstance(v, (str, list, dict))))

    for item in j.get("organic_results", []):
        for key in ("title", "snippet"):
            if item.get(key):
                text_blobs.append(item[key])

    big = " \n".join(text_blobs)
    if "€€€" in big or "$$$" in big:
        return "$$$"
    if "€€" in big or "$$" in big:
        return "$$"
    if "€" in big or "$" in big or "£" in big:
        return "$"

    m = re.search(r"(price range|prix|range)\s*[:\-]?\s*([$\£€]+.*?)(?=\.|,|;|\n|$)", big, re.I)
    if m:
        return m.group(2).strip()

    return None


def fetch_brand_overview(brand: str) -> Dict[str, Any]:
    """
    - logo, website, name, categories via Knowledge Graph (si dispo)
    """
    out = {
        "brand": brand,
        "brand_name": None,
        "logo": None,
        "website": None,
        "categories": [],
    }
    try:
        j = serp_search(brand)
        kg = parse_knowledge_graph(j)
        out.update({k: v for k, v in kg.items() if v})
    except Exception as e:
        out["error_overview"] = str(e)
    return out


def fetch_brand_extras(brand: str) -> Dict[str, Any]:
    """
    - price_range
    - country_origin (query dédiée)
    - country_production (query dédiée)
    - ngo_links (GoodOnYou, FairWear, B-Corp)
    """
    extras: Dict[str, Any] = {
        "price_range": None,
        "country_origin": None,
        "country_production": None,
        "ngo_links": [],
    }

    try:
        j_price = serp_search(f"{brand} price range")
        extras["price_range"] = extract_price_range_from_snippets(j_price)
        sleep_backoff(0)
    except Exception as e:
        extras["error_price"] = str(e)

    try:
        j_origin = serp_search(f"{brand} country of origin")
        extras["country_origin"] = extract_country_from_snippets(j_origin)
        sleep_backoff(1)
    except Exception as e:
        extras["error_origin"] = str(e)

    try:
        j_prod = serp_search(f"Where are {brand} products made")
        extras["country_production"] = extract_country_from_snippets(j_prod)
        sleep_backoff(2)
    except Exception as e:
        extras["error_production"] = str(e)

    try:
        domains = ["goodonyou.eco", "fairwear.org", "bcorporation.net", "cleanclothes.org"]
        j_ngo = serp_search(f'{brand} site:goodonyou.eco OR site:fairwear.org OR site:bcorporation.net OR site:cleanclothes.org')
        extras["ngo_links"] = parse_organic_links(j_ngo, domain_filters=domains, limit=10)
        sleep_backoff(3)
    except Exception as e:
        extras["error_ngo"] = str(e)

    return extras


def scrape_brand(brand: str) -> Dict[str, Any]:
    base = fetch_brand_overview(brand)
    extra = fetch_brand_extras(brand)
    base.update(extra)
    return base


def export_json(rows: List[Dict[str, Any]], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def export_csv(rows: List[Dict[str, Any]], path: str):
    fields = [
        "brand",
        "brand_name",
        "logo",
        "website",
        "categories",
        "price_range",
        "country_origin",
        "country_production",
        "ngo_links",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            row = {k: r.get(k) for k in fields}
            if isinstance(row.get("categories"), list):
                row["categories"] = ", ".join([str(x) for x in row["categories"]])
            if isinstance(row.get("ngo_links"), list):
                row["ngo_links"] = ", ".join([str(x) for x in row["ngo_links"]])
            w.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Scrape brand info via SerpAPI")
    parser.add_argument("--brands", nargs="*", help="Noms de marques à scraper")
    parser.add_argument("--brands-file", help="Chemin vers un fichier texte (une marque par ligne)")
    parser.add_argument("--out-json", default="brands.json", help="Fichier JSON de sortie")
    parser.add_argument("--out-csv", default="brands.csv", help="Fichier CSV de sortie")
    args = parser.parse_args()

    brands: List[str] = []
    if args.brands:
        brands.extend(args.brands)
    if args.brands_file:
        with open(args.brands_file, "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if name:
                    brands.append(name)

    if not brands:
        print("  Aucune marque fournie. Utilise --brands Nike Patagonia ou --brands-file brands.txt")
        return

    rows: List[Dict[str, Any]] = []
    for i, b in enumerate(brands):
        print(f"[{i+1}/{len(brands)}] Scraping: {b} ...")
        try:
            rows.append(scrape_brand(b))
        except Exception as e:
            rows.append({"brand": b, "error": str(e)})
        sleep_backoff(i)

    export_json(rows, args.out_json)
    export_csv(rows, args.out_csv)
    print(f" Terminé. JSON -> {args.out_json} | CSV -> {args.out_csv}")


if __name__ == "__main__":
    main()
