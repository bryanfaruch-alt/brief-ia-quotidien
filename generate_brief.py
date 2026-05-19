#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_brief.py - Generation automatique du Brief IA quotidien
Variables d'environnement:
  GROQ_API_KEY        - cle API Groq
  GMAIL_USER          - adresse Gmail
  GMAIL_APP_PASSWORD  - mot de passe application Gmail
"""

import os, time, sys, json, smtplib, feedparser
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from groq import Groq

sys.path.insert(0, os.path.dirname(__file__))
from brief_template_v3 import generate_brief_pdf

GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")
GMAIL_USER     = os.environ.get("GMAIL_USER", "")
GMAIL_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

DESTINATAIRES = {
    "bryan": {"email": "bryan.faruch@gmail.com",    "prenom": "Bryan"},
    "shana": {"email": "shana.charbit@orange.fr",   "prenom": "Shana"},
    "aaron": {"email": "faruchaaron14@gmail.com",   "prenom": "Aaron"},
}

FLUX_RSS = [
    "https://feeds.feedburner.com/oreilly/radar",
    "https://www.artificialintelligence-news.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
]


def fetch_articles():
    print("Recuperation des actualites IA...")
    articles = []
    for url in FLUX_RSS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                articles.append({
                    "titre":  entry.get("title", "Sans titre")[:120],
                    "source": feed.feed.get("title", url)[:50],
                    "lien":   entry.get("link", ""),
                    "resume": entry.get("summary", "")[:300],
                })
        except Exception:
            pass
    articles = articles[:6]
    print(f"  -> {len(articles)} articles trouves")
    return articles


def generate_content_with_groq(jour, articles):
    print("Generation du contenu avec Groq (llama-3.3-70b)...")

    articles_txt = "\n".join([
        f"- {a['titre']} ({a['source']})" for a in articles
    ])

    nb_news = min(len(articles), 3)

    prompt = f"""Tu es un expert IA creant des briefs educatifs quotidiens en JSON.

Contexte: Jour {jour} de formation IA, date: {datetime.now().strftime('%d %B %Y')}

Actualites IA du jour:
{articles_txt}

Reponds UNIQUEMENT avec ce JSON valide (respecte exactement les cles):

{{
  "s1_titre": "Titre du concept IA du jour (ex: Les Reseaux de Neurones)",
  "s1_simple": "Explication simple en 2-3 phrases pour debutant absolu",
  "s2_mot": "Terme technique a connaitre aujourd'hui (1-3 mots)",
  "s2_def": "Definition claire du terme en 2 phrases",
  "news": [
    {{
      "emoji": "emoji",
      "color": "#3b82f6",
      "tag": "categorie (Tech/Sante/Business)",
      "title": "Titre de l'actualite",
      "what": "Ce qui s'est passe en 2 phrases simples",
      "what_bryan": "Explication pour etudiant en orthodontie",
      "what_aaron": "Explication pour futur expert-comptable"
    }}
  ],
  "bryan": {{
    "s1_analogy": "Analogie du concept avec l'orthodontie (2-3 phrases)",
    "s1_exemple": "Exemple concret d'utilisation de ce concept en medecine",
    "s1_important": "Pourquoi ce concept est important pour Bryan",
    "s2_exemple": "Exemple du terme technique dans le contexte medical",
    "s4_nom": "Nom d'un outil IA utile pour les etudiants en medecine",
    "s4_lien": "https://example.com",
    "s4_description": "A quoi sert cet outil (1 phrase)",
    "s4_usage": "Comment Bryan peut l'utiliser (1 phrase)",
    "s4_gratuit": "Gratuit / Freemium / Payant",
    "s5_objectif": "Objectif du mini-exercice pour Bryan (1 phrase)",
    "s5_step1": "Etape 1 de l'exercice (1 phrase)",
    "s5_step2": "Etape 2 de l'exercice (1 phrase)",
    "s5_step3": "Etape 3 de l'exercice (1 phrase)",
    "s5_resultat": "Ce que Bryan obtiendra apres l'exercice (1 phrase)",
    "s6_desc": "Ce que fait le prompt pour Bryan (1 phrase)",
    "s6_usage": "Quand utiliser ce prompt (1 phrase)",
    "s6_prompt": "Prompt complet pret a copier pour Bryan (3-5 lignes)",
    "s7_bad": "Exemple de mauvais prompt a eviter",
    "s7_good": "Exemple de bon prompt ameliore",
    "recap": ["Point 1 a retenir", "Point 2 a retenir", "Point 3 a retenir"]
  }},
  "aaron": {{
    "s1_analogy": "Analogie du concept avec la comptabilite (2-3 phrases)",
    "s1_exemple": "Exemple concret d'utilisation de ce concept en comptabilite",
    "s1_important": "Pourquoi ce concept est important pour Aaron",
    "s2_exemple": "Exemple du terme technique dans le contexte comptable",
    "s4_nom": "Nom d'un outil IA utile pour les comptables",
    "s4_lien": "https://example.com",
    "s4_description": "A quoi sert cet outil (1 phrase)",
    "s4_usage": "Comment Aaron peut l'utiliser (1 phrase)",
    "s4_gratuit": "Gratuit / Freemium / Payant",
    "s5_objectif": "Objectif du mini-exercice pour Aaron (1 phrase)",
    "s5_step1": "Etape 1 de l'exercice (1 phrase)",
    "s5_step2": "Etape 2 de l'exercice (1 phrase)",
    "s5_step3": "Etape 3 de l'exercice (1 phrase)",
    "s5_resultat": "Ce qu'Aaron obtiendra apres l'exercice (1 phrase)",
    "s6_desc": "Ce que fait le prompt pour Aaron (1 phrase)",
    "s6_usage": "Quand utiliser ce prompt (1 phrase)",
    "s6_prompt": "Prompt complet pret a copier pour Aaron (3-5 lignes)",
    "s7_bad": "Exemple de mauvais prompt a eviter",
    "s7_good": "Exemple de bon prompt ameliore",
    "recap": ["Point 1 a retenir", "Point 2 a retenir", "Point 3 a retenir"]
  }}
}}

Genere exactement {nb_news} elements dans le tableau "news".
IMPORTANT: reponds uniquement avec le JSON, sans texte avant ou apres."""

    client = Groq(api_key=GROQ_API_KEY)

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Tu es un assistant qui repond toujours en JSON valide uniquement, sans aucun texte avant ou apres le JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=4000,
            )
            content = response.choices[0].message.content
            data = json.loads(content)
            print("  -> Contenu genere avec succes")
            return data
        except Exception as e:
            err = str(e)
            if ("quota" in err.lower() or "429" in err or "rate" in err.lower()) and attempt < 2:
                print(f"  -> Quota depasse, attente 70s... (tentative {attempt+1}/3)")
                time.sleep(70)
            else:
                raise


def build_content(data, version, jour):
    """Construit le dict complet requis par brief_template_v3.generate_brief_pdf"""
    v = data.get(version, {})
    g = data  # global fields

    # News items
    colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]
    news = []
    for i, n in enumerate(g.get("news", [])):
        news.append({
            "emoji": n.get("emoji", "\U0001f4f0"),
            "color": n.get("color", colors[i % len(colors)]),
            "tag":   n.get("tag", "Actu"),
            "title": n.get("title", ""),
            "what":  n.get("what", ""),
            "pour":  n.get(f"what_{version}", n.get("what", "")),
        })

    # Tool rows
    s4_rows = [
        ("\U0001f4e6", "NOM",         v.get("s4_nom", "ChatGPT")),
        ("\U0001f517", "LIEN",        v.get("s4_lien", "https://chat.openai.com")),
        ("\U0001f4dd", "DESCRIPTION", v.get("s4_description", "Assistant IA generaliste")),
        ("\U0001f3af", "USAGE",       v.get("s4_usage", "Poser des questions, rediger du contenu")),
        ("\U0001f4b0", "GRATUIT ?",   v.get("s4_gratuit", "Freemium")),
    ]

    # Exercise steps
    s5_steps = [
        (1, "\U0001f3af", v.get("s5_step1", "Ouvre ChatGPT ou un autre outil IA")),
        (2, "✏️",  v.get("s5_step2", "Tape le prompt fourni dans la section 6")),
        (3, "✅",  v.get("s5_step3", "Analyse la reponse et note ce que tu as appris")),
    ]

    if version == "bryan":
        edition = f"Semaine {(jour-1)//7 + 1} - Formation IA - Jour {jour}"
    else:
        edition = f"Edition Aaron - Expert-Comptable - Jour {jour}"

    return {
        "edition":      edition,
        "s1_titre":     g.get("s1_titre", "Concept IA du jour"),
        "s1_simple":    g.get("s1_simple", ""),
        "s1_analogy":   v.get("s1_analogy", ""),
        "s1_exemple":   v.get("s1_exemple", ""),
        "s1_important": v.get("s1_important", ""),
        "s2_mot":       g.get("s2_mot", ""),
        "s2_def":       g.get("s2_def", ""),
        "s2_exemple":   v.get("s2_exemple", ""),
        "news":         news,
        "s4_rows":      s4_rows,
        "s5_objectif":  v.get("s5_objectif", ""),
        "s5_steps":     s5_steps,
        "s5_resultat":  v.get("s5_resultat", ""),
        "s6_desc":      v.get("s6_desc", ""),
        "s6_usage":     v.get("s6_usage", ""),
        "s6_prompt":    v.get("s6_prompt", ""),
        "s7_bad":       v.get("s7_bad", ""),
        "s7_good":      v.get("s7_good", ""),
        "recap":        v.get("recap", ["Notion vue aujourd'hui", "Pratique quotidienne", "Continuer demain"]),
        "quote":        "La connaissance s'acquiert par l'experience, tout le reste n'est qu'information.",
        "quote_author": "- Albert Einstein",
        "motto":        "\U0001f680 Une brique par jour - dans 30 jours tu seras meconnaissable.",
    }


def send_email(destinataire, pdf_path, prenom, jour):
    print(f"  -> Envoi a {destinataire['email']}...")
    msg = MIMEMultipart()
    msg["From"]    = GMAIL_USER
    msg["To"]      = destinataire["email"]
    msg["Subject"] = f"[Brief IA] Jour {jour} - {datetime.now().strftime('%d %B %Y')}"

    body = f"Bonjour {prenom},\n\nVoici ton brief IA quotidien pour aujourd'hui !\n\nBonne lecture,\nTon assistant IA automatique\n"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with open(pdf_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename=brief_ia_jour{jour}.pdf")
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
    print("     Email envoye !")


if __name__ == "__main__":
    print("=" * 55)
    print("  Brief IA Quotidien - Generation automatique")
    print("=" * 55)

    from datetime import date as _date
    _mois = ["janvier","fevrier","mars","avril","mai","juin",
             "juillet","aout","septembre","octobre","novembre","decembre"]
    _today = _date.today()
    _start = _date(2026, 5, 19)
    jour     = max(1, (_today - _start).days + 1)
    date_str = f"{_today.day} {_mois[_today.month-1]} {_today.year}"

    # 1. Actus
    articles = fetch_articles()

    # 2. Contenu IA
    data = generate_content_with_groq(jour, articles)

    # 3. Generation des PDFs
    print("Generation des PDFs...")
    content_bryan = build_content(data, "bryan", jour)
    content_aaron = build_content(data, "aaron", jour)

    pdf_bryan, pdf_aaron = generate_brief_pdf(
        content_bryan, content_aaron,
        jour, date_str,
        output_dir="/tmp",
        prefix="brief_ia"
    )
    print(f"  -> PDF bryan : {pdf_bryan}")
    print(f"  -> PDF aaron : {pdf_aaron}")

    # 4. Envoi des emails
    print("Envoi des emails...")
    send_email(DESTINATAIRES["bryan"], pdf_bryan, "Bryan", jour)
    send_email(DESTINATAIRES["shana"], pdf_bryan, "Shana", jour)
    send_email(DESTINATAIRES["aaron"], pdf_aaron, "Aaron", jour)

    print("=" * 55)
    print("  SUCCES ! Tous les emails ont ete envoyes.")
    print("=" * 55)
