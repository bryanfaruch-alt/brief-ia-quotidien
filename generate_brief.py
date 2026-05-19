#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_brief.py — Generation automatique du Brief IA quotidien
Tourne dans le cloud (GitHub Actions) — aucun ordinateur requis.

Variables d'environnement necessaires (GitHub Secrets) :
  GROQ_API_KEY        — cle API Groq (gratuite)
  GMAIL_USER          — ton adresse Gmail
  GMAIL_APP_PASSWORD  — mot de passe d'application Gmail (16 caracteres)
"""

import os
import time
import sys
import json
import smtplib
import feedparser
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from groq import Groq

sys.path.insert(0, os.path.dirname(__file__))
from brief_template_v3 import generate_brief_pdf, make_li

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

GROQ_API_KEY    = os.environ.get("GROQ_API_KEY", "")
GMAIL_USER      = os.environ.get("GMAIL_USER", "")
GMAIL_PASSWORD  = os.environ.get("GMAIL_APP_PASSWORD", "")

DESTINATAIRES = {
    "bryan": {
        "email":  "bryan.faruch@gmail.com",
        "prenom": "Bryan",
        "metier": "etudiant en orthodontie (DES Nice)",
        "analogies": "orthodontie, dentisterie, etudes DES, radiographies dentaires",
    },
    "shana": {
        "email":  "shana.charbit@orange.fr",
        "prenom": "Shana",
        "metier": "etudiante en orthodontie",
        "analogies": "orthodontie, dentisterie, etudes DES, pratique clinique",
    },
    "aaron": {
        "email":  "faruchaaron14@gmail.com",
        "prenom": "Aaron",
        "metier": "etudiant visant a devenir expert-comptable",
        "analogies": "comptabilite, gestion financiere, cabinets comptables, normes IFRS",
    },
}

FLUX_RSS = [
    "https://feeds.feedburner.com/oreilly/radar",
    "https://www.artificialintelligence-news.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
]

# ─────────────────────────────────────────────
# Etape 1 : Recuperation des actus
# ─────────────────────────────────────────────

def fetch_articles() -> list[dict]:
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

# ─────────────────────────────────────────────
# Etape 2 : Generation du contenu avec Groq
# ─────────────────────────────────────────────

def generate_content_with_groq(jour: int, articles: list[dict]) -> dict:
    print("Generation du contenu avec Groq (llama-3.3-70b)...")

    articles_txt = "\n".join([
        f"- {a['titre']} ({a['source']})"
        for a in articles
    ])

    prompt = f"""Tu es un expert en IA qui cree des briefs educatifs quotidiens pour des debutants.

CONTEXTE :
- Jour {jour} de la formation IA (progression continue)
- Date : {datetime.now().strftime('%d %B %Y')}

ACTUALITES IA DU JOUR :
{articles_txt}

INSTRUCTIONS IMPORTANTES :
Tu dois repondre UNIQUEMENT avec un objet JSON valide, sans aucun texte avant ou apres.
Le JSON doit avoir EXACTEMENT cette structure (respecte tous les noms de cles) :

{{
  "concept_titre": "Titre du concept IA du jour (ex: Les Reseaux de Neurones)",
  "concept_simple": "Explication simple du concept en 2-3 phrases pour un debutant absolu",
  "news": [
    {{
      "emoji": "emoji representatif",
      "color": "couleur hex (ex: #3b82f6)",
      "tag": "categorie courte (ex: Sante, Business, Tech)",
      "title": "Titre de l actualite",
      "what": "Explication courte de ce qui se passe (2 phrases)",
      "what_bryan": "Explication pour un etudiant en orthodontie (analogie dentaire si possible)",
      "what_aaron": "Explication pour un futur expert-comptable (analogie comptable si possible)"
    }}
  ],
  "bryan": {{
    "s1_analogy": "Analogie du concept avec l orthodontie ou la medecine dentaire (2-3 phrases)",
    "conseil_pratique": "1 conseil pratique pour Bryan pour utiliser l IA dans ses etudes d orthodontie",
    "outil_du_jour": "Un outil IA utile pour les etudiants en medecine/orthodontie",
    "outil_description": "Description courte de cet outil (1-2 phrases)",
    "quiz_question": "Une question de quiz sur le concept du jour",
    "quiz_reponse": "La reponse a la question de quiz",
    "defi": "Un petit defi pratique pour Bryan (5 minutes max)"
  }},
  "aaron": {{
    "s1_analogy": "Analogie du concept avec la comptabilite ou la gestion financiere (2-3 phrases)",
    "conseil_pratique": "1 conseil pratique pour Aaron pour utiliser l IA dans sa future carriere d expert-comptable",
    "outil_du_jour": "Un outil IA utile pour les comptables et financiers",
    "outil_description": "Description courte de cet outil (1-2 phrases)",
    "quiz_question": "Une question de quiz sur le concept du jour",
    "quiz_reponse": "La reponse a la question de quiz",
    "defi": "Un petit defi pratique pour Aaron (5 minutes max)"
  }}
}}

Genere exactement {min(len(articles), 3)} actualites dans le tableau "news".
RAPPEL : reponds uniquement avec le JSON, rien d autre."""

    client = Groq(api_key=GROQ_API_KEY)

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Tu es un assistant qui repond toujours en JSON valide uniquement, sans texte avant ou apres."},
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
            if ('quota' in err.lower() or '429' in err or 'rate' in err.lower()) and attempt < 2:
                print(f"  -> Quota depasse, attente 70s... (tentative {attempt+1}/3)")
                time.sleep(70)
            else:
                raise

# ─────────────────────────────────────────────
# Etape 3 : Construction du contenu pour le template
# ─────────────────────────────────────────────

def build_content_dicts(data: dict, version: str, jour: int) -> dict:
    """Construit le dict pour brief_template_v3.py"""
    v = data.get(version, {})

    news = []
    colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]
    for i, n in enumerate(data.get("news", [])):
        news.append({
            "emoji": n.get("emoji", "📰"),
            "color": n.get("color", colors[i % len(colors)]),
            "tag":   n.get("tag", "Actu"),
            "title": n.get("title", ""),
            "what":  n.get("what", ""),
            "pour":  n.get(f"what_{version}", n.get("what", "")),
        })

    if version == "bryan":
        edition = f"Semaine {(jour-1)//7 + 1} · Formation IA · Jour {jour}"
        emoji_outil = "🛠️"
    else:
        edition = f"Edition Aaron · Expert-Comptable · Jour {jour}"
        emoji_outil = "💼"

    return {
        "edition":      edition,
        "s1_titre":     data.get("concept_titre", "Concept IA du jour"),
        "s1_simple":    data.get("concept_simple", ""),
        "s1_analogy":   v.get("s1_analogy", ""),
        "news":         news,
        "s3_items":     [
            make_li("💡", v.get("conseil_pratique", "")),
            make_li(emoji_outil, f"<b>{v.get('outil_du_jour', '')}</b> — {v.get('outil_description', '')}"),
        ],
        "quiz_q":       v.get("quiz_question", ""),
        "quiz_a":       v.get("quiz_reponse", ""),
        "defi":         v.get("defi", ""),
        "prog_pct":     min(100, jour),
        "prog_label":   f"Jour {jour} / Formation continue",
    }

# ─────────────────────────────────────────────
# Etape 4 : Envoi par email
# ─────────────────────────────────────────────

def send_email(destinataire: dict, pdf_path: str, prenom: str, jour: int):
    print(f"  -> Envoi a {destinataire['email']}...")
    msg = MIMEMultipart()
    msg["From"]    = GMAIL_USER
    msg["To"]      = destinataire["email"]
    msg["Subject"] = f"[Brief IA] Jour {jour} — {datetime.now().strftime('%d %B %Y')}"

    body = f"""Bonjour {prenom},

Voici ton brief IA quotidien pour aujourd'hui !

Bonne lecture,
Ton assistant IA automatique
"""
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
    print(f"     Email envoye !")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  Brief IA Quotidien — Generation automatique")
    print("=" * 55)

    jour = int(datetime.now().strftime("%j"))  # Jour de l annee (1-365)

    # 1. Actus
    articles = fetch_articles()

    # 2. Contenu IA
    data = generate_content_with_groq(jour, articles)

    # 3. Generation des PDFs
    print("Generation des PDFs...")
    pdfs = {}
    for version in ["bryan", "aaron"]:
        content = build_content_dicts(data, version, jour)
        pdf_path = f"/tmp/brief_{version}_jour{jour}.pdf"
        generate_brief_pdf(content, pdf_path)
        pdfs[version] = pdf_path
        print(f"  -> PDF {version} genere : {pdf_path}")

    # 4. Envoi des emails
    print("Envoi des emails...")

    # Bryan et Shana recoivent la version "bryan"
    for key in ["bryan", "shana"]:
        dest = DESTINATAIRES[key]
        send_email(dest, pdfs["bryan"], dest["prenom"], jour)

    # Aaron recoit la version "aaron"
    send_email(DESTINATAIRES["aaron"], pdfs["aaron"], "Aaron", jour)

    print("=" * 55)
    print("  SUCCES ! Tous les emails ont ete envoyes.")
    print("=" * 55)
