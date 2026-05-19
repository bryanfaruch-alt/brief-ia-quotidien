#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_brief.py â GÃ©nÃ©ration automatique du Brief IA quotidien
Tourne dans le cloud (GitHub Actions) â aucun ordinateur requis.

Variables d'environnement nÃ©cessaires (GitHub Secrets) :
  GEMINI_API_KEY      â clÃ© API Google AI Studio (gratuite)
  GMAIL_USER          â ton adresse Gmail (ex. bryan.faruch@gmail.com)
  GMAIL_APP_PASSWORD  â mot de passe d'application Gmail (16 caractÃ¨res)
"""

import os, sys, json, smtplib, feedparser
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import google.generativeai as genai

# ââ Import du moteur de rendu premium
sys.path.insert(0, os.path.dirname(__file__))
from brief_template_v3 import generate_brief_pdf, make_li

# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# CONFIG
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

GEMINI_API_KEY     = os.environ["GEMINI_API_KEY"]
GMAIL_USER         = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]

DESTINATAIRES = {
    "bryan": {
        "email":  "bryan.faruch@gmail.com",
        "prenom": "Bryan",
        "metier": "Ã©tudiant en orthodontie (DES Nice)",
        "analogies": "orthodontie, dentisterie, Ã©tudes DES, pratique clinique, radiographies dentaires",
    },
    "shana": {
        "email":  "shana.charbit@orange.fr",
        "prenom": "Shana",
        "metier": "mÃªme que Bryan (orthodontie)",
        "analogies": "orthodontie, dentisterie, Ã©tudes DES, pratique clinique",
    },
    "aaron": {
        "email":  "faruchaaron14@gmail.com",
        "prenom": "Aaron",
        "metier": "Ã©tudiant visant Ã  devenir expert-comptable",
        "analogies": "comptabilitÃ©, gestion financiÃ¨re, cabinets comptables, normes IFRS/PCG, droit fiscal",
    },
}

DATE_DEBUT = datetime(2026, 5, 18)
OUTDIR     = "/tmp/briefs"
os.makedirs(OUTDIR, exist_ok=True)

_MOIS = ["janvier","fÃ©vrier","mars","avril","mai","juin",
         "juillet","aoÃ»t","septembre","octobre","novembre","dÃ©cembre"]

# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# ÃTAPE 1 â RÃ©cupÃ©rer les actualitÃ©s IA via RSS (gratuit)
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

def fetch_ai_news() -> list[dict]:
    """RÃ©cupÃ¨re les 5 derniÃ¨res actualitÃ©s IA depuis Google News RSS."""
    print("ð° RÃ©cupÃ©ration des actualitÃ©s IA...")
    feeds = [
        "https://news.google.com/rss/search?q=intelligence+artificielle+IA&hl=fr&gl=FR&ceid=FR:fr",
        "https://news.google.com/rss/search?q=ChatGPT+Claude+Gemini+OpenAI&hl=fr&gl=FR&ceid=FR:fr",
    ]
    articles = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:4]:
            articles.append({
                "titre":  entry.get("title", ""),
                "source": entry.get("source", {}).get("title", ""),
                "lien":   entry.get("link", ""),
                "resume": entry.get("summary", "")[:300],
            })
    # DÃ©dupliquer et garder les 6 meilleures
    seen = set()
    unique = []
    for a in articles:
        if a["titre"] not in seen:
            seen.add(a["titre"])
            unique.append(a)
        if len(unique) >= 6:
            break
    print(f"   â {len(unique)} articles trouvÃ©s")
    return unique


def generate_content_with_gemini(jour: int, articles: list[dict]) -> dict:
    """Appelle Gemini pour gÃ©nÃ©rer tout le contenu du brief en JSON."""
    print("ð¤ GÃ©nÃ©ration du contenu avec Gemini...")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config={"response_mime_type": "application/json"},
    )

    articles_txt = "\n".join([
        f"- {a['titre']} ({a['source']})"
        for a in articles[:6]
    ])

    prompt = f"""
Tu es un expert en IA qui crÃ©e des briefs Ã©ducatifs quotidiens pour des dÃ©butants complets.

CONTEXTE :
- Jour {jour} de la formation (sur une formation longue, illimitÃ©e)
- Date : aujourd'hui
- Les semaines prÃ©cÃ©dentes ont couvert les bases (Jours 1-7: fondamentaux IA, 8-14: prompting, 15-21: outils, 22-30: cas pratiques). Continue naturellement la progression.

ACTUALITÃS IA DU JOUR (trouvÃ©es sur le web) :
{articles_txt}
"""

    response = model.generate_content(prompt)
    data = json.loads(response.text)
    print("   â Contenu gÃ©nÃ©rÃ© avec succÃ¨s")
    return data


def build_content_dicts(data: dict, version: str) -> dict:
    """Construit le dict de contenu pour brief_template_v3.py."""
    v = data[version]
    emoji_outil = "ð¦·" if version == "bryan" else "ð¼"

    news = []
    for n in data["news"]:
        news.append({
            "emoji": n["emoji"],
            "color": n["color"],
            "tag":   n["tag"],
            "title": n["title"],
            "what":  n["what"],
            "pour":  n.get(f"what_{version}", n["what"]),
        })

    edition = (
        f"Semaine {(jour_global-1)//7 + 1} Â· Formation IA"
        if version == "bryan"
        else f"Ãdition Aaron Â· Expert-Comptable Â· Jour {jour_global}"
    )

    return {
        "edition":      edition,
        "s1_titre":     data["concept_titre"],
        "s1_simple":    data["concept_simple"],
        "s1_analogy":   v["s1_analogy"],
        "s1_exemple":   v["s1_exemple"],
        "s1_important": v["s1_important"],
        "s2_mot":       data["mot_technique"],
        "s2_def":       data["mot_def"],
        "s2_exemple":   v["s2_exemple"],
        "news":         news,
        "s4_rows": [
            ("ð¤", "NOM",          data["outil_nom"]),
            ("ð", "TYPE",         data["outil_type"]),
            ("â", "SERT Ã",       data["outil_sert_a"]),
            (emoji_outil, "USAGES", make_li(v["outil_usages"])),
            ("ð°", "PRIX",         data["outil_prix"]),
            ("ð", "ACCÃS",        data["outil_acces"]),
        ],
        "s5_objectif":  v["exercice_objectif"],
        "s5_steps":     [tuple(s) for s in data["exercice_steps"]],
        "s5_resultat":  v["exercice_resultat"],
        "s6_desc":      v["s6_desc"],
        "s6_usage":     v["s6_usage"],
        "s6_prompt":    v["s6_prompt"],
        "s7_bad":       data["astuce_bad"],
        "s7_good":      data["astuce_good"],
        "recap":        v["recap"],
        "quote":        data["quote"],
        "quote_author": data["quote_author"],
        "motto":        "ð Chaque jour compte â tu construis ton avantage.",
    }


if __name__ == "__main__":
    today    = datetime.now()
    jour     = max(1, (today - DATE_DEBUT).days + 1)
    jour_global = jour
    date_str = f"{today.day} {_MOIS[today.month - 1]} {today.year}"

    print(f"\n{'='*55}")
    print(f"  ð¤ Brief IA Quotidien â Jour {jour} â {date_str}")
    print(f"{'='*55}\n")

    articles = fetch_ai_news()
    data = generate_content_with_gemini(jour, articles)

    print("ð GÃ©nÃ©ration des PDFs premium...")
    content_bryan = build_content_dicts(data, "bryan")
    content_aaron = build_content_dicts(data, "aaron")

    path_bryan, path_aaron = generate_brief_pdf(
        content_bryan = content_bryan,
        content_aaron = content_aaron,
        jour          = jour,
        date_str      = date_str,
        output_dir    = OUTDIR,
        prefix        = "brief-ia",
    )

    print("\nð¬ Envoi des emails...")
    send_email(DESTINATAIRES["bryan"]["email"], "Bryan", path_bryan, jour, date_str)
    send_email(DESTINATAIRES["shana"]["email"], "Shana", path_bryan, jour, date_str)
    send_email(DESTINATAIRES["aaron"]["email"], "Aaron", path_aaron, jour, date_str)

    print(f"\nâ Brief Jour {jour} envoyÃ© avec succÃ¨s Ã  tous les destinataires !")
