#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
â         BRIEF IA â TEMPLATE PREMIUM v3                          â
â         Design : Bleu Corporate Â· SVG Â· WeasyPrint              â
â                                                                  â
â  Usage :                                                         â
â    from brief_template_v3 import generate_brief_pdf             â
â    generate_brief_pdf(content_bryan, content_aaron,             â
â                       jour=1, date_str="18 mai 2026",           â
â                       output_dir="/path/to/output")             â
â                                                                  â
â  Structure du dict content (voir CONTENT_SCHEMA ci-dessous)     â
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

CONTENT_SCHEMA = {
    "edition":       str,   # ex. "Semaine 1 Â· DÃ©couverte de l'IA"

    # ââ Section 1 : Concept du jour ââ
    "s1_titre":      str,   # titre du concept
    "s1_simple":     str,   # explication simple (HTML autorisÃ©)
    "s1_analogy":    str,   # analogie mÃ©tier (HTML autorisÃ©)
    "s1_exemple":    str,   # exemple concret (HTML autorisÃ©)
    "s1_important":  str,   # pourquoi c'est important (HTML autorisÃ©)

    # ââ Section 2 : Mot technique ââ
    "s2_mot":        str,   # ex. "ALGORITHME"
    "s2_def":        str,   # dÃ©finition simple (HTML autorisÃ©)
    "s2_exemple":    str,   # exemple concret (HTML autorisÃ©)

    # ââ Section 3 : ActualitÃ©s (liste de 3 dicts) ââ
    "news": [
        {
            "emoji": str,   # ex. "ðµ"
            "color": str,   # ex. "#1d4ed8"
            "tag":   str,   # ex. "VALORISATION"
            "title": str,
            "what":  str,   # ce qui s'est passÃ©
            "pour":  str,   # pourquoi c'est important pour toi
        },
    ],

    # ââ Section 4 : Outil (lignes du tableau) ââ
    "s4_rows": [
        ("emoji", "LABEL", "valeur"),
        # Pour la ligne USAGES, utiliser make_li([...]) pour des items Ã©lÃ©gants
    ],

    # ââ Section 5 : Exercice ââ
    "s5_objectif":  str,
    "s5_steps": [
        ("1", "ð", "texte de l'Ã©tape"),
    ],
    "s5_resultat":  str,

    # ââ Section 6 : Prompt ââ
    "s6_desc":      str,
    "s6_usage":     str,
    "s6_prompt":    str,   # texte brut du prompt

    # ââ Section 7 : Astuce ââ
    "s7_bad":       str,
    "s7_good":      str,

    # ââ Section 8 : RÃ©cap (liste de 3 strings HTML) ââ
    "recap": [str, str, str],

    # ââ Footer ââ
    "quote":        str,
    "quote_author": str,
    "motto":        str,
}
"""

import os, subprocess, sys, base64

def _pip(*p):
    subprocess.run([sys.executable, "-m", "pip", "install", *p,
                    "--break-system-packages", "-q"], capture_output=True)
_pip("weasyprint")
from weasyprint import HTML


# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# HELPER PUBLIC
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

def make_li(items: list) -> str:
    """Convertit une liste de strings en items HTML Ã©lÃ©gants (sans puces grossiÃ¨res)."""
    return "".join(f"<div class='li-item'>{item}</div>" for item in items)


def _svg_b64(svg_str: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(
        svg_str.strip().encode()).decode()


# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# SVG ILLUSTRATIONS (inline, aucune dÃ©pendance externe)
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

_SVG_NEURAL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 130" width="400" height="130">
  <defs><radialGradient id="ng" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.25"/>
    <stop offset="100%" stop-color="#0d1b2a" stop-opacity="0"/>
  </radialGradient></defs>
  <rect width="400" height="130" fill="url(#ng)"/>
  <g stroke="#3b82f6" stroke-opacity="0.3" stroke-width="0.8">
    <line x1="40" y1="30" x2="130" y2="20"/><line x1="40" y1="30" x2="130" y2="65"/>
    <line x1="40" y1="65" x2="130" y2="20"/><line x1="40" y1="65" x2="130" y2="65"/>
    <line x1="40" y1="65" x2="130" y2="110"/><line x1="40" y1="100" x2="130" y2="65"/>
    <line x1="40" y1="100" x2="130" y2="110"/>
    <line x1="130" y1="20" x2="220" y2="35"/><line x1="130" y1="20" x2="220" y2="75"/>
    <line x1="130" y1="65" x2="220" y2="35"/><line x1="130" y1="65" x2="220" y2="75"/>
    <line x1="130" y1="65" x2="220" y2="115"/><line x1="130" y1="110" x2="220" y2="75"/>
    <line x1="130" y1="110" x2="220" y2="115"/>
    <line x1="220" y1="35" x2="310" y2="20"/><line x1="220" y1="35" x2="310" y2="65"/>
    <line x1="220" y1="75" x2="310" y2="20"/><line x1="220" y1="75" x2="310" y2="65"/>
    <line x1="220" y1="75" x2="310" y2="110"/><line x1="220" y1="115" x2="310" y2="65"/>
    <line x1="220" y1="115" x2="310" y2="110"/>
    <line x1="310" y1="20" x2="370" y2="50"/><line x1="310" y1="65" x2="370" y2="50"/>
    <line x1="310" y1="65" x2="370" y2="90"/><line x1="310" y1="110" x2="370" y2="90"/>
  </g>
  <g fill="#60a5fa" fill-opacity="0.7">
    <circle cx="40" cy="30" r="5"/><circle cx="40" cy="65" r="5"/><circle cx="40" cy="100" r="5"/>
    <circle cx="130" cy="20" r="6"/><circle cx="130" cy="65" r="7"/><circle cx="130" cy="110" r="6"/>
    <circle cx="220" cy="35" r="6"/><circle cx="220" cy="75" r="8"/><circle cx="220" cy="115" r="6"/>
    <circle cx="310" cy="20" r="6"/><circle cx="310" cy="65" r="7"/><circle cx="310" cy="110" r="6"/>
    <circle cx="370" cy="50" r="5"/><circle cx="370" cy="90" r="5"/>
  </g>
  <g fill="#f59e0b"><circle cx="130" cy="65" r="4"/><circle cx="220" cy="75" r="5"/></g>
</svg>"""

_SVG_ROBOT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60" width="60" height="60">
  <rect x="10" y="18" width="40" height="32" rx="6" fill="#1d4ed8" opacity="0.9"/>
  <rect x="16" y="24" width="10" height="8" rx="3" fill="#7dd3fc"/>
  <rect x="34" y="24" width="10" height="8" rx="3" fill="#7dd3fc"/>
  <rect x="19" y="38" width="22" height="5" rx="2" fill="#93c5fd" opacity="0.6"/>
  <rect x="24" y="10" width="12" height="10" rx="3" fill="#3b82f6"/>
  <circle cx="30" cy="10" r="3" fill="#f59e0b"/>
  <rect x="4" y="28" width="6" height="14" rx="3" fill="#1e40af"/>
  <rect x="50" y="28" width="6" height="14" rx="3" fill="#1e40af"/>
  <rect x="18" y="50" width="8" height="8" rx="2" fill="#1e40af"/>
  <rect x="34" y="50" width="8" height="8" rx="2" fill="#1e40af"/>
</svg>"""

_SVG_BRAIN = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 60" width="80" height="60">
  <ellipse cx="30" cy="30" rx="22" ry="18" fill="#1d4ed8" opacity="0.15"/>
  <ellipse cx="50" cy="30" rx="22" ry="18" fill="#3b82f6" opacity="0.15"/>
  <path d="M30 16 Q18 16 16 26 Q12 28 14 36 Q14 44 24 44 Q28 46 32 44 Q34 48 38 46 Q40 48 42 46 Q46 48 48 44 Q58 44 58 36 Q60 28 56 26 Q54 16 42 16 Q38 12 34 14 Q32 12 30 16Z"
        fill="none" stroke="#3b82f6" stroke-width="2" opacity="0.7"/>
  <line x1="40" y1="16" x2="40" y2="44" stroke="#60a5fa" stroke-width="1.5" opacity="0.5"/>
  <path d="M24 28 Q28 24 32 28 Q36 24 40 28" fill="none" stroke="#60a5fa" stroke-width="1.5" opacity="0.6"/>
  <path d="M40 28 Q44 24 48 28 Q52 24 56 28" fill="none" stroke="#60a5fa" stroke-width="1.5" opacity="0.6"/>
  <path d="M20 34 Q26 38 32 34" fill="none" stroke="#60a5fa" stroke-width="1.5" opacity="0.6"/>
  <path d="M48 34 Q52 38 58 34" fill="none" stroke="#60a5fa" stroke-width="1.5" opacity="0.6"/>
  <circle cx="22" cy="30" r="2" fill="#f59e0b"/>
  <circle cx="58" cy="30" r="2" fill="#f59e0b"/>
  <circle cx="40" cy="22" r="2" fill="#10b981"/>
</svg>"""

_SVG_LIGHTBULB = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="22" height="22">
  <circle cx="16" cy="13" r="7" fill="#fde68a"/>
  <rect x="13" y="20" width="6" height="2" rx="1" fill="#fde68a"/>
  <rect x="13.5" y="23" width="5" height="2" rx="1" fill="#fde68a"/>
  <line x1="16" y1="4" x2="16" y2="2" stroke="#fbbf24" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="23" y1="7" x2="25" y2="5" stroke="#fbbf24" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="9" y1="7" x2="7" y2="5" stroke="#fbbf24" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="26" y1="13" x2="28" y2="13" stroke="#fbbf24" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="6" y1="13" x2="4" y2="13" stroke="#fbbf24" stroke-width="1.5" stroke-linecap="round"/>
</svg>"""

_SVG_CHART = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 50" width="80" height="50">
  <rect x="5" y="30" width="12" height="15" rx="2" fill="#3b82f6" opacity="0.8"/>
  <rect x="22" y="20" width="12" height="25" rx="2" fill="#3b82f6" opacity="0.9"/>
  <rect x="39" y="10" width="12" height="35" rx="2" fill="#1d4ed8"/>
  <rect x="56" y="5" width="12" height="40" rx="2" fill="#1e40af"/>
  <line x1="5" y1="45" x2="75" y2="45" stroke="#93c5fd" stroke-width="1"/>
  <polyline points="11,30 28,20 45,10 62,5" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="3,2"/>
  <circle cx="11" cy="30" r="2.5" fill="#f59e0b"/>
  <circle cx="28" cy="20" r="2.5" fill="#f59e0b"/>
  <circle cx="45" cy="10" r="2.5" fill="#f59e0b"/>
  <circle cx="62" cy="5" r="2.5" fill="#f59e0b"/>
</svg>"""

_SVG_PROMPT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 40" width="50" height="40">
  <rect x="2" y="2" width="46" height="36" rx="6" fill="#1e293b"/>
  <rect x="2" y="2" width="46" height="10" rx="6" fill="#334155"/>
  <circle cx="10" cy="7" r="2" fill="#ef4444"/>
  <circle cx="17" cy="7" r="2" fill="#fbbf24"/>
  <circle cx="24" cy="7" r="2" fill="#22c55e"/>
  <text x="7" y="23" font-family="monospace" font-size="7" fill="#7dd3fc">&gt;_ </text>
  <rect x="16" y="19" width="20" height="2" rx="1" fill="#475569"/>
  <rect x="7" y="27" width="30" height="2" rx="1" fill="#334155"/>
  <rect x="7" y="32" width="20" height="2" rx="1" fill="#334155"/>
</svg>"""

_SVG_STAR = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20">
  <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"
           fill="#f59e0b" stroke="#d97706" stroke-width="0.5"/>
</svg>"""


# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# CSS (commun Ã  toutes les versions)
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

_CSS = """
@page { size:A4; margin:12mm 15mm 12mm 15mm; }
*{ box-sizing:border-box; margin:0; padding:0; }
body{ font-family:'Segoe UI',Arial,'Helvetica Neue',sans-serif; font-size:9pt; line-height:1.55; color:#1e2a3a; background:white; }

.hdr{ background:linear-gradient(135deg,#0a1628 0%,#0f2755 45%,#1a4a9e 100%); border-radius:12px; padding:0; margin-bottom:16px; overflow:hidden; position:relative; }
.hdr-accent{ height:5px; background:linear-gradient(90deg,#f59e0b 0%,#3b82f6 40%,#10b981 100%); }
.hdr-body{ padding:18px 24px 18px; position:relative; }
.hdr-eyebrow{ font-size:7.5pt; font-weight:700; letter-spacing:2.5px; text-transform:uppercase; color:#93c5fd; text-align:center; margin-bottom:6px; }
.hdr-title{ font-size:21pt; font-weight:900; text-align:center; color:white; letter-spacing:-0.5px; line-height:1.15; margin-bottom:5px; }
.hdr-zour{ font-size:11pt; font-weight:700; text-align:center; color:#fde68a; margin-bottom:4px; letter-spacing:1px; }
.hdr-sub{ font-size:9.5pt; text-align:center; color:#bfdbfe; margin-bottom:14px; }
.hdr-badges{ display:flex; justify-content:center; gap:8px; margin-bottom:14px; }
.hdr-badge{ background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:white; font-size:7.5pt; font-weight:600; padding:4px 13px; border-radius:20px; }
.prog-wrap{ background:rgba(0,0,0,0.3); border-radius:10px; height:8px; margin:0 40px; }
.prog-label{ text-align:right; margin:3px 40px 0; font-size:7pt; color:#93c5fd; }

.sh{ display:flex; align-items:center; gap:8px; padding:8px 14px; border-radius:8px; color:white; font-size:10pt; font-weight:800; margin-top:14px; margin-bottom:10px; page-break-after:avoid; }
.sh img{ width:20px; height:20px; }
.c1{ background:linear-gradient(90deg,#1d4ed8,#3b82f6); }
.c2{ background:linear-gradient(90deg,#15803d,#22c55e); }
.c3{ background:linear-gradient(90deg,#b91c1c,#ef4444); }
.c4{ background:linear-gradient(90deg,#6d28d9,#8b5cf6); }
.c5{ background:linear-gradient(90deg,#0e7490,#06b6d4); }
.c6{ background:linear-gradient(90deg,#374151,#6b7280); }
.c7{ background:linear-gradient(90deg,#b45309,#f59e0b); }
.c8{ background:linear-gradient(90deg,#0a1628,#1e3a6e); }

.card{ background:#f8faff; border:1px solid #e2e8f0; border-radius:8px; padding:12px 14px; margin-bottom:8px; page-break-inside:avoid; }
.callout{ border-left:4px solid #3b82f6; background:#eff6ff; padding:9px 12px; border-radius:0 7px 7px 0; margin-bottom:8px; page-break-inside:avoid; }
.callout.amber{ border-color:#f59e0b; background:#fffbeb; }
.micro-label{ font-size:7pt; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#6b7280; margin-bottom:4px; }
.section-title{ font-size:13pt; font-weight:900; color:#0d1b2a; margin-bottom:10px; line-height:1.2; page-break-after:avoid; }
.big-word{ font-size:20pt; font-weight:900; color:#15803d; letter-spacing:-0.5px; margin-bottom:8px; }

.news-card{ background:white; border:1.5px solid #e2e8f0; border-radius:10px; padding:12px 14px; margin-bottom:9px; page-break-inside:avoid; }
.news-badge{ display:inline-block; color:white; font-size:7pt; font-weight:800; padding:2px 10px; border-radius:12px; letter-spacing:0.8px; }
.news-title{ font-size:10.5pt; font-weight:800; color:#0d1b2a; margin-bottom:8px; line-height:1.3; }
.news-pour{ border-left:3px solid; padding:7px 10px; border-radius:0 6px 6px 0; margin-top:5px; }

.tool-tbl{ width:100%; border-collapse:collapse; border-radius:10px; overflow:hidden; margin-bottom:8px; }
.tool-lbl{ background:#4c1d95; color:white; text-align:center; padding:9px 8px; width:18%; vertical-align:middle; font-weight:700; }
.tool-val{ background:#5b21b6; color:white; font-size:9pt; padding:9px 12px; vertical-align:middle; line-height:1.5; }
.tool-tbl tr+tr .tool-lbl, .tool-tbl tr+tr .tool-val{ border-top:0.5px solid #4c1d95; }

.li-item{ position:relative; padding:3px 0 3px 16px; font-size:8.8pt; line-height:1.5; color:#e9efff; }
.li-item::before{ content:""; position:absolute; left:2px; top:50%; transform:translateY(-50%); width:5px; height:1.5px; background:rgba(147,197,253,0.55); border-radius:2px; }

.step{ display:flex; gap:9px; align-items:flex-start; margin-bottom:7px; background:#f0fdfd; border:1px solid #a5f3fc; border-radius:7px; padding:8px 11px; page-break-inside:avoid; }
.step-num{ background:#0e7490; color:white; font-size:9pt; font-weight:900; min-width:22px; height:22px; border-radius:50%; text-align:center; line-height:22px; flex-shrink:0; }
.step-text{ flex:1; font-size:9pt; padding-top:2px; }

.prompt-hdr{ background:#1e293b; border-radius:10px 10px 0 0; padding:7px 16px; display:flex; align-items:center; gap:7px; }
.prompt-dot{ width:8px; height:8px; border-radius:50%; display:inline-block; }
.prompt-box{ background:#0d1b2a; border-radius:0 0 10px 10px; padding:14px 16px; font-family:'Courier New',monospace; font-size:8.5pt; color:#e2e8f0; line-height:1.75; white-space:pre-wrap; page-break-inside:avoid; border:1px solid #1e3a5f; }

.astuce{ background:#fffbeb; border:1.5px solid #fde68a; border-radius:10px; padding:13px 15px; page-break-inside:avoid; }
.bad-box{ background:#fef2f2; border-left:3px solid #dc2626; padding:8px 11px; border-radius:0 6px 6px 0; margin-bottom:8px; color:#7f1d1d; font-size:9pt; }
.good-box{ background:#f0fdf4; border-left:3px solid #16a34a; padding:8px 11px; border-radius:0 6px 6px 0; margin-bottom:8px; color:#14532d; font-size:9pt; }
.tip-note{ background:white; border:1px solid #fde68a; border-radius:6px; padding:8px 11px; color:#78350f; font-size:8.5pt; margin-top:6px; }

.recap-item{ display:flex; margin-bottom:8px; border-radius:8px; overflow:hidden; border:1.5px solid #1e3a5f; page-break-inside:avoid; }
.recap-num{ background:linear-gradient(180deg,#0f2755,#1a4a9e); color:white; font-size:16pt; font-weight:900; min-width:44px; display:flex; align-items:center; justify-content:center; }
.recap-text{ background:#f0f7ff; padding:10px 14px; flex:1; font-size:9pt; line-height:1.55; }

.footer{ margin-top:14px; padding-top:12px; border-top:2px solid #e2e8f0; text-align:center; page-break-inside:avoid; }
.quote-mark{ font-size:28pt; color:#dbeafe; font-family:Georgia,serif; line-height:0.8; }
.footer-quote{ font-size:9.5pt; font-style:italic; color:#4b5563; margin:4px 0; }
.footer-author{ font-size:8.5pt; color:#9ca3af; margin-bottom:10px; }
.footer-motto{ font-size:10.5pt; font-weight:800; color:#1d4ed8; margin-bottom:6px; }
.footer-meta{ font-size:7pt; color:#cbd5e1; letter-spacing:0.5px; }
"""


# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# HTML BUILDER (interne)
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

def _build_html(c: dict, jour: int, date_str: str) -> str:
    pct = round(jour / 30 * 100, 1)
    prog_bar = f"background:linear-gradient(90deg,#f59e0b,#3b82f6);height:8px;border-radius:10px;width:{pct}%;"

    neural_b64 = _svg_b64(_SVG_NEURAL)
    robot_b64  = _svg_b64(_SVG_ROBOT)
    brain_b64  = _svg_b64(_SVG_BRAIN)
    bulb_b64   = _svg_b64(_SVG_LIGHTBULB)
    chart_b64  = _svg_b64(_SVG_CHART)
    prompt_b64 = _svg_b64(_SVG_PROMPT)
    star_b64   = _svg_b64(_SVG_STAR)

    news_html = ""
    for n in c["news"]:
        news_html += f"""
        <div class="news-card">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
            <span style="font-size:16pt;">{n['emoji']}</span>
            <span class="news-badge" style="background:{n['color']};">{n['tag']}</span>
          </div>
          <div class="news-title">{n['title']}</div>
          <div class="micro-label">ð CE QU'IL S'EST PASSÃ</div>
          <p style="margin-bottom:8px;font-size:8.5pt;">{n['what']}</p>
          <div class="news-pour" style="border-color:{n['color']};background:{n['color']}18;">
            <div class="micro-label" style="color:{n['color']};">ð¯ POUR TOI</div>
            <p style="color:{n['color']};font-size:8.5pt;font-weight:600;">{n['pour']}</p>
          </div>
        </div>"""

    tool_html = ""
    for emo, label, val in c["s4_rows"]:
        tool_html += f"""
        <tr>
          <td class="tool-lbl"><span style="font-size:11pt;">{emo}</span><br>
          <span style="font-size:7pt;letter-spacing:0.5px;">{label}</span></td>
          <td class="tool-val">{val}</td>
        </tr>"""

    steps_html = ""
    for num, emo, text in c["s5_steps"]:
        steps_html += f"""
        <div class="step">
          <div class="step-num">{num}</div>
          <div style="font-size:14pt;line-height:1;">{emo}</div>
          <div class="step-text">{text}</div>
        </div>"""

    recap_html = ""
    for i, item in enumerate(c["recap"], 1):
        recap_html += f"""
        <div class="recap-item">
          <div class="recap-num">{i}</div>
          <div class="recap-text">{item}</div>
        </div>"""

    edition      = c.get("edition", f"Jour {jour} Â· Formation IA")
    quote        = c.get("quote", "La connaissance s'acquiert par l'expÃ©rience, tout le reste n'est qu'information.")
    quote_author = c.get("quote_author", "â Albert Einstein")
    motto        = c.get("motto", "ð Une brique par jour â dans 30 jours tu seras mÃ©connaissable.")

    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><style>{_CSS}</style></head>
<body>

<div class="hdr">
  <div class="hdr-accent"></div>
  <div class="hdr-body">
    <img src="{neural_b64}" style="width:380px;height:auto;position:absolute;right:0;top:0;opacity:0.35;"/>
    <div class="hdr-eyebrow">ð¤ &nbsp;Brief IA Quotidien &nbsp;Â·&nbsp; Formation AccÃ©lÃ©rÃ©e</div>
    <div class="hdr-jour">â¦ JOUR {jour} / 30 â¦</div>
    <div class="hdr-title">{c['s1_titre']}</div>
    <div class="hdr-sub">{date_str} &nbsp;Â·&nbsp; {edition}</div>
    <div class="hdr-badges">
      <span class="hdr-badge">â±ï¸ ~8 min de lecture</span>
      <span class="hdr-badge">ð¯ Niveau DÃ©butant</span>
      <span class="hdr-badge">ð Jour {jour} Â· IA Fondamentaux</span>
    </div>
    <div class="prog-wrap"><div style="{prog_bar}"></div></div>
    <div class="prog-label">Progression : Jour {jour} sur 30 &nbsp;Â·&nbsp; {pct}% accompli ð</div>
  </div>
</div>

<div class="sh c1"><img src="{bulb_b64}"/> ð¡ &nbsp;1. Le concept IA du jour</div>
<div class="section-title">{c['s1_titre']}</div>
<div class="micro-label" style="color:#1d4ed8;">ð EN VERSION SIMPLE</div>
<div class="callout" style="margin-bottom:9px;">{c['s1_simple']}</div>
<div class="micro-label" style="color:#b45309;">ð ANALOGIE DU QUOTIDIEN</div>
<div class="callout amber" style="margin-bottom:9px;">{c['s1_analogy']}</div>
<div style="display:flex;gap:9px;margin-bottom:8px;">
  <div class="card" style="flex:1;border-color:#bfdbfe;">
    <div class="micro-label" style="color:#1d4ed8;">ð¬ EXEMPLE CONCRET</div>
    <div style="margin-top:4px;">{c['s1_exemple']}</div>
  </div>
  <div class="card" style="flex:1;border-color:#bfdbfe;">
    <div class="micro-label" style="color:#15803d;">â¡ POURQUOI C'EST IMPORTANT</div>
    <div style="margin-top:4px;">{c['s1_important']}</div>
  </div>
</div>

<div class="sh c2">ð &nbsp;2. Le mot technique Ã  connaÃ®tre</div>
<div style="display:flex;gap:12px;align-items:flex-start;">
  <div style="flex:1;">
    <div class="big-word">{c['s2_mot']}</div>
    <div class="card" style="border-color:#bbf7d0;">
      {c['s2_def']}
      <div style="margin-top:8px;">{c['s2_exemple']}</div>
    </div>
  </div>
  <div style="text-align:center;padding-top:4px;">
    <img src="{chart_b64}" style="width:85px;height:auto;opacity:0.85;"/>
    <div style="font-size:7pt;color:#6b7280;margin-top:4px;">DonnÃ©es â RÃ©sultat</div>
  </div>
</div>

<div class="sh c3">ð° &nbsp;3. L'actualitÃ© IA importante du jour</div>
{news_html}

<div class="sh c4">ð ï¸ &nbsp;4. L'outil IA du jour</div>
<div style="display:flex;gap:12px;align-items:flex-start;">
  <div style="text-align:center;padding-top:4px;">
    <img src="{robot_b64}" style="width:65px;height:auto;"/>
    <div style="font-size:7.5pt;color:#7c3aed;font-weight:700;margin-top:4px;">IA Tool</div>
  </div>
  <div style="flex:1;"><table class="tool-tbl">{tool_html}</table></div>
</div>

<div class="sh c5">âï¸ &nbsp;5. Mini exercice pratique (5 minutes max)</div>
<div class="card" style="background:#f0fdfd;border-color:#a5f3fc;">
  <p style="margin-bottom:10px;"><strong>ð¯ Objectif :</strong> {c['s5_objectif']}</p>
  {steps_html}
  <div style="background:#ccfbf1;border:1px solid #5eead4;border-radius:7px;padding:9px 12px;margin-top:8px;color:#0f766e;">
    â &nbsp;<strong>RÃ©sultat attendu :</strong> {c['s5_resultat']}
  </div>
</div>

<div class="sh c6"><img src="{prompt_b64}"/> ð &nbsp;6. Prompt prÃªt Ã  copier</div>
<div class="card" style="border-color:#d1d5db;background:#f9fafb;margin-bottom:8px;">
  <p><strong>ð¯ Ce que fait ce prompt :</strong> {c['s6_desc']}</p>
  <p style="margin-top:5px;font-size:8.5pt;color:#4b5563;">{c['s6_usage']}</p>
</div>
<div class="prompt-hdr">
  <span class="prompt-dot" style="background:#ef4444;"></span>
  <span class="prompt-dot" style="background:#f59e0b;"></span>
  <span class="prompt-dot" style="background:#22c55e;"></span>
  <span style="font-size:7.5pt;color:#94a3b8;margin-left:4px;font-family:monospace;">prompt.txt &nbsp;Â·&nbsp; Copier-Coller dans ChatGPT</span>
</div>
<div class="prompt-box">{c['s6_prompt']}</div>

<div class="sh c7"><img src="{star_b64}"/> ð¡ &nbsp;7. Astuce IA du jour</div>
<div class="astuce">
  <p style="font-weight:800;font-size:10pt;color:#78350f;margin-bottom:10px;">
    ð­ &nbsp;Donne toujours un <em>rÃ´le</em> Ã  l'IA avant de poser ta question.
  </p>
  <div class="bad-box">â &nbsp;<strong>Au lieu de :</strong> {c['s7_bad']}</div>
  <div class="good-box">â &nbsp;<strong>Dis plutÃ´t :</strong> {c['s7_good']}</div>
  <div class="tip-note">
    ð¬ &nbsp;La rÃ©ponse sera immÃ©diatement plus prÃ©cise, plus adaptÃ©e et plus utile.
    C'est la <strong>rÃ¨gle nÂ°1 du prompting</strong> â retiens-la bien.
  </div>
</div>

<div class="sh c8"><img src="{brain_b64}"/> ð§  &nbsp;8. Ce qu'il faut retenir aujourd'hui</div>
{recap_html}

<div class="footer">
  <div class="quote-mark">"</div>
  <div class="footer-quote">{quote}</div>
  <div class="footer-author">{quote_author}</div>
  <div class="footer-motto">{motto}</div>
  <div class="footer-meta">Brief IA Quotidien &nbsp;Â·&nbsp; {date_str} &nbsp;Â·&nbsp; Jour {jour} / 30</div>
</div>

</body></html>"""


# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# FONCTION PRINCIPALE â API publique
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

def generate_brief_pdf(
    content_bryan: dict,
    content_aaron: dict,
    jour: int,
    date_str: str,
    output_dir: str = ".",
    prefix: str = "brief-ia"
) -> tuple:
    """
    GÃ©nÃ¨re deux PDFs premium (Bryan et Aaron) Ã  partir des dicts de contenu.

    ParamÃ¨tres :
        content_bryan  â dict avec tout le contenu de la version Bryan (orthodontie)
        content_aaron  â dict avec tout le contenu de la version Aaron (expert-comptable)
        jour           â numÃ©ro du jour (1 Ã  30)
        date_str       â ex. "18 mai 2026"
        output_dir     â rÃ©pertoire de sortie
        prefix         â prÃ©fixe du fichier (ex. "brief-ia")

    Retourne :
        (chemin_bryan, chemin_aaron)
    """
    os.makedirs(output_dir, exist_ok=True)
    paths = {}
    for version, content in [("bryan", content_bryan), ("aaron", content_aaron)]:
        html = _build_html(content, jour, date_str)
        out  = os.path.join(output_dir, f"{prefix}-jour{jour}-{version}.pdf")
        HTML(string=html).write_pdf(out)
        print(f"â  {out}")
        paths[version] = out
    return paths["bryan"], paths["aaron"]
