#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_brief.py ÃÂ¢ÃÂÃÂ GÃÂÃÂ©nÃÂÃÂ©ration automatique du Brief IA quotidien
Tourne dans le cloud (GitHub Actions) ÃÂ¢ÃÂÃÂ aucun ordinateur requis.

Variables d'environnement nÃÂÃÂ©cessaires (GitHub Secrets) :
  GEMINI_API_KEY      ÃÂ¢ÃÂÃÂ clÃÂÃÂ© API Google AI Studio (gratuite)
  GMAIL_USER          ÃÂ¢ÃÂÃÂ ton adresse Gmail (ex. bryan.faruch@gmail.com)
  GMAIL_APP_PASSWORD  ÃÂ¢ÃÂÃÂ mot de passe d'application Gmail (16 caractÃÂÃÂ¨res)
"""

import os
import time, sys, json, smtplib, feedparser
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import google.generativeai as genai

# ÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂ Import du moteur de rendu premium
sys.path.insert(0, os.path.dirname(__file__))
from brief_template_v3 import generate_brief_pdf, make_li

# ÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂ
# CONFIG
# ÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂ

GEMINI_API_KEY     = os.environ["GEMINI_API_KEY"]
GMAIL_USER         = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]

DESTINATAIRES = {
    "bryan": {
        "email":  "bryan.faruch@gmail.com",
        "prenom": "Bryan",
        "metier": "ÃÂÃÂ©tudiant en orthodontie (DES Nice)",
        "analogies": "orthodontie, dentisterie, ÃÂÃÂ©tudes DES, pratique clinique, radiographies dentaires",
    },
    "shana": {
        "email":  "shana.charbit@orange.fr",
        "prenom": "Shana",
        "metier": "mÃÂÃÂªme que Bryan (orthodontie)",
        "analogies": "orthodontie, dentisterie, ÃÂÃÂ©tudes DES, pratique clinique",
    },
    "aaron": {
        "email":  "faruchaaron14@gmail.com",
        "prenom": "Aaron",
        "metier": "ÃÂÃÂ©tudiant visant ÃÂÃÂ  devenir expert-comptable",
        "analogies": "comptabilitÃÂÃÂ©, gestion financiÃÂÃÂ¨re, cabinets comptables, normes IFRS/PCG, droit fiscal",
    },
}

DATE_DEBUT = datetime(2026, 5, 18)
OUTDIR     = "/tmp/briefs"
os.makedirs(OUTDIR, exist_ok=True)

_MOIS = ["janvier","fÃÂÃÂ©vrier","mars","avril","mai","juin",
         "juillet","aoÃÂÃÂ»t","septembre","octobre","novembre","dÃÂÃÂ©cembre"]

# ÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂ
# ÃÂÃÂTAPE 1 ÃÂ¢ÃÂÃÂ RÃÂÃÂ©cupÃÂÃÂ©rer les actualitÃÂÃÂ©s IA via RSS (gratuit)
# ÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂÃÂ¢ÃÂÃÂ

def fetch_ai_news() -> list[dict]:
    """RÃÂÃÂ©cupÃÂÃÂ¨re les 5 derniÃÂÃÂ¨res actualitÃÂÃÂ©s IA depuis Google News RSS."""
    print("ÃÂ°ÃÂÃÂÃÂ° RÃÂÃÂ©cupÃÂÃÂ©ration des actualitÃÂÃÂ©s IA...")
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
    # DÃÂÃÂ©dupliquer et garder les 6 meilleures
    seen = set()
    unique = []
    for a in articles:
        if a["titre"] not in seen:
            seen.add(a["titre"])
            unique.append(a)
        if len(unique) >= 6:
            break
    print(f"   ÃÂ¢ÃÂÃÂ {len(unique)} articles trouvÃÂÃÂ©s")
    return unique


def generate_content_with_gemini(jour: int, articles: list[dict]) -> dict:
    """Appelle Gemini pour gÃÂÃÂ©nÃÂÃÂ©rer tout le contenu du brief en JSON."""
    print("ÃÂ°ÃÂÃÂ¤ÃÂ GÃÂÃÂ©nÃÂÃÂ©ration du contenu avec Gemini...")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        generation_config={"response_mime_type": "application/json"},
    )

    articles_txt = "\n".join([
        f"- {a['titre']} ({a['source']})"
        for a in articles[:6]
    ])

    prompt = f"""
Tu es un expert en IA qui crÃÂÃÂ©e des briefs ÃÂÃÂ©ducatifs quotidiens pour des dÃÂÃÂ©butants complets.

CONTEXTE :
- Jour {jour} de la formation (sur une formation longue, illimitÃÂÃÂ©e)
- Date : aujourd'hui
- Les semaines prÃÂÃÂ©cÃÂÃÂ©dentes ont couvert les bases (Jours 1-7: fondamentaux IA, 8-14: prompting, 15-21: outils, 22-30: cas pratiques). Continue naturellement la progression.

ACTUALITÃÂÃÂS IA DU JOUR (trouvÃÂÃÂ©es sur le web) :
{articles_txt}
"""

    # Retry jusqu'à 3 fois si quota dépassé
    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            break
        except Exception as e:
            if 'quota' in str(e).lower() or 'resource' in str(e).lower() or '429' in str(e):
                if attempt < 2:
                    print(f"⏳ Quota Gemini dépassé, attente 70s... (tentative {attempt+1}/3)")
                    time.sleep(70)
                else:
                    raise
            else:
                raise
    data = json.loads(response.text)
    print("   ÃÂ¢ÃÂÃÂ Contenu gÃÂÃÂ©nÃÂÃÂ©rÃÂÃÂ© avec succÃÂÃÂ¨s")
    return data


def build_content_dicts(data: dict, version: str) -> dict:
    """Construit le dict de contenu pour brief_template_v3.py."""
    v = data[version]
    emoji_outil = "ÃÂ°ÃÂÃÂ¦ÃÂ·" if version == "bryan" else "ÃÂ°ÃÂÃÂÃÂ¼"

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
        f"Semaine {(jour_global-1)//7 + 1} ÃÂÃÂ· Formation IA"
        if version == "bryan"
        else f"ÃÂÃÂdition Aaron ÃÂÃÂ· Expert-Comptable ÃÂÃÂ· Jour {jour_global}"
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
            ("ÃÂ°ÃÂÃÂ¤ÃÂ", "NOM",          data["outil_nom"]),
            ("ÃÂ°ÃÂÃÂÃÂ", "TYPE",         data["outil_type"]),
            ("ÃÂ¢ÃÂÃÂ", "SERT ÃÂÃÂ",       data["outil_sert_a"]),
            (emoji_outil, "USAGES", make_li(v["outil_usages"])),
            ("ÃÂ°ÃÂÃÂÃÂ°", "PRIX",         data["outil_prix"]),
            ("ÃÂ°ÃÂÃÂÃÂ", "ACCÃÂÃÂS",        data["outil_acces"]),
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
        "motto":        "ÃÂ°ÃÂÃÂÃÂ Chaque jour compte ÃÂ¢ÃÂÃÂ tu construis ton avantage.",
    }


if __name__ == "__main__":
    today    = datetime.now()
    jour     = max(1, (today - DATE_DEBUT).days + 1)
    jour_global = jour
    date_str = f"{today.day} {_MOIS[today.month - 1]} {today.year}"

    print(f"\n{'='*55}")
    print(f"  ÃÂ°ÃÂÃÂ¤ÃÂ Brief IA Quotidien ÃÂ¢ÃÂÃÂ Jour {jour} ÃÂ¢ÃÂÃÂ {date_str}")
    print(f"{'='*55}\n")

    articles = fetch_ai_news()
    data = generate_content_with_gemini(jour, articles)

    print("ÃÂ°ÃÂÃÂÃÂ GÃÂÃÂ©nÃÂÃÂ©ration des PDFs premium...")
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

    print("\nÃÂ°ÃÂÃÂÃÂ¬ Envoi des emails...")
    send_email(DESTINATAIRES["bryan"]["email"], "Bryan", path_bryan, jour, date_str)
    send_email(DESTINATAIRES["shana"]["email"], "Shana", path_bryan, jour, date_str)
    send_email(DESTINATAIRES["aaron"]["email"], "Aaron", path_aaron, jour, date_str)

    print(f"\nÃÂ¢ÃÂÃÂ Brief Jour {jour} envoyÃÂÃÂ© avec succÃÂÃÂ¨s ÃÂÃÂ  tous les destinataires !")
