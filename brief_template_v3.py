#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║         BRIEF IA — TEMPLATE PREMIUM v3                          ║
║         Design : Bleu Corporate · SVG · WeasyPrint              ║
║                                                                  ║
║  Usage :                                                         ║
║    from brief_template_v3 import generate_brief_pdf             ║
║    generate_brief_pdf(content_bryan, content_aaron,             ║
║                       jour=1, date_str="18 mai 2026",           ║
║                       output_dir="/path/to/output")             ║
║                                                                  ║
║  Structure du dict content (voir CONTENT_SCHEMA ci-dessous)     ║
╚══════════════════════════════════════════════════════════════════╝

CONTENT_SCHEMA = {
    "edition":       str,   # ex. "Semaine 1 · Découverte de l'IA"

    # ── Section 1 : Concept du jour ──
    "s1_titre":      str,   # titre du concept
    "s1_simple":     str,   # explication simple (HTML autorisé)
    "s1_analogy":    str,   # analogie métier (HTML autorisé)
    "s1_exemple":    str,   # exemple concret (HTML autorisé)
    "s1_important":  str,   # pourquoi c'est important (HTML autorisé)

    # ── Section 2 : Mot technique ──
    "s2_mot":        str,   # ex. "ALGORITHME"
    "s2_def":        str,   # définition simple (HTML autorisé)
    "s2_exemple":    str,   # exemple concret (HTML autorisé)

    # ── Section 3 : Actualités (liste de 3 dicts) ──
    "news": [
        {
            "emoji": str,   # ex. "🔵"
            "color": str,   # ex. "#1d4ed8"
            "tag":   str,   # ex. "VALORISATION"
            "title": str,
            "what":  str,   # ce qui s'est passé
            "pour":  str,   # pourquoi c'est important pour toi
        },
    ],

    # ── Section 4 : Outil (lignes du tableau) ──
    "s4_rows": [
        ("emoji", "LABEL", "valeur"),
        # Pour la ligne USAGES, utiliser make_li([...]) pour des items élégants
    ],

    # ── Section 5 : Exercice ──
    "s5_objectif":  str,
    "s5_steps": [
        ("1", "🌐", "texte de l'étape"),
    ],
    "s5_resultat":  str,

    # ── Section 6 : Prompt ──
    "s6_desc":      str,
    "s6_usage":     str,
    "s6_prompt":    str,   # texte brut du prompt

    # ── Section 7 : Astuce ──����ؘY�������������������8� 8� �X�[ۈ���X�\
\�HH���[���S
H8� 8� ���X�\���������K���8� 8� ���\�8� 8� ��][�H������][�W�]]܈������[�Ȏ����B������[\ܝ���X����\���\��\�M���Y��\

�
N���X����\�˜�[���\˙^X�]X�K�[H��\��[��[�
���KX��XZ�\�\�[K\X��Y�\ȋ�\H�K�\\�W��]]U�YJB��\
��X\�\�[��B����H�X\�\�[�[\ܝS����8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d��ST�P�P�8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d��Y�XZ�W�J][\Έ\�
HO���������۝�\�][�H\�HH��[���[�][\�S0�[0�Y�[��
�[��X�\�ܛ���p��\�K������]\�������[���]��\��I�KZ][IϞ�][_O�]����܈][H[�][\�B���Y��ݙ�؍�
ݙ�������HO������]\���]N�[XY�K�ݙ��[ؘ\�M��
��\�M����[���J�ݙ�������\

K�[���J
JK�X��J
B����8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d��Ց�ST��USӔ�
[�[�K]X�[�H0�\[�[��H^\��JB��8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d���Ց�ӑUT�SH���ݙ�[��H������˝�˛ܙ�̌�ݙȈ�Y]Л�H�
L���YH��ZY�H�L����Y�Ϗ�YX[ܘYY[�YH��Ȉ�H�L	H��OH�L	H��H�L	H�����ٙ��]H�	H���X��܏H��؎������[�X�]OH���H�ς���ٙ��]H�L	H���X��܏H��X��H���[�X�]OH��ς�ܘYX[ܘYY[���Y�ς��X��YH��ZY�H�L���[H�\�
ۙ�H�ς������OH��؎��������K[�X�]OH��Ȉ����K]�YH�����[�HOH��LOH����H�L��L�H���Ϗ[�HOH��LOH����H�L��L�H��H�ς�[�HOH��LOH��H��H�L��L�H���Ϗ[�HOH��LOH��H��H�L��L�H��H�ς�[�HOH��LOH��H��H�L��L�H�LL�Ϗ[�HOH��LOH�L��H�L��L�H��H�ς�[�HOH��LOH�L��H�L��L�H�LL�ς�[�HOH�L��LOH����H����L�H��H�Ϗ[�HOH�L��LOH����H����L�H��H�ς�[�HOH�L��LOH��H��H����L�H��H�Ϗ[�HOH�L��LOH��H��H����L�H��H�ς�[�HOH�L��LOH��H��H����L�H�LMH�Ϗ[�HOH�L��LOH�LL��H����L�H��H�ς�[�HOH�L��LOH�LL��H����L�H�LMH�ς�[�HOH����LOH��H��H��L�L�H���Ϗ[�HOH����LOH��H��H��L�L�H��H�ς�[�HOH����LOH��H��H��L�L�H���Ϗ[�HOH����LOH��H��H��L�L�H��H�ς�[�HOH����LOH��H��H��L�L�H�LL�Ϗ[�HOH����LOH�LMH��H��L�L�H��H�ς�[�HOH����LOH�LMH��H��L�L�H�LL�ς�[�HOH��L�LOH����H����L�H�L�Ϗ[�HOH��L�LOH��H��H����L�H�L�ς�[�HOH��L�LOH��H��H����L�H�L�Ϗ[�HOH��L�LOH�LL��H����L�H�L�ς��ς���[H�͌MY�H��[[�X�]OH��ȏ���\��H�H���OH����H�H�Ϗ�\��H�H���OH��H��H�H�Ϗ�\��H�H���OH�L��H�H�ς��\��H�H�L���OH����H���Ϗ�\��H�H�L���OH��H��H�ȋϏ�\��H�H�L���OH�LL��H���ς��\��H�H�����OH��H��H���Ϗ�\��H�H�����OH��H��H��Ϗ�\��H�H�����OH�LMH��H���ς��\��H�H��L��OH����H���Ϗ�\��H�H��L��OH��H��H�ȋϏ�\��H�H��L��OH�LL��H���ς��\��H�H�����OH�L��H�H�Ϗ�\��H�H�����OH�L��H�H�ς��ς���[H�ٍNYL����\��H�H�L���OH��H��H��Ϗ�\��H�H�����OH��H��H�H�Ϗ�ς��ݙψ������Ց�ԓГ�H���ݙ�[��H������˝�˛ܙ�̌�ݙȈ�Y]Л�H�
�
���YH���ZY�H������X�H�L�OH�N��YH��ZY�H�̈��H����[H��Y
Y��X�]OH��H�ς��X�H�M��OH����YH�L�ZY�H���H�Ȉ�[H���٘ȋς��X�H���OH����YH�L�ZY�H���H�Ȉ�[H���٘ȋς��X�H�NH�OH����YH����ZY�H�H��H����[H��L��Y���X�]OH����ς��X�H���OH�L��YH�L��ZY�H�L��H�Ȉ�[H��؎����ς��\��H�H����OH�L��H�Ȉ�[H�ٍNYL��ς��X�H��OH����YH���ZY�H�M��H�Ȉ�[H��YMY��ς��X�H�L�OH����YH���ZY�H�M��H�Ȉ�[H��YMY��ς��X�H�N�OH�L��YH��ZY�H���H����[H��YMY��ς��X�H���OH�L��YH��ZY�H���H����[H��YMY��ς��ݙψ������Ց�Д�RS�H���ݙ�[��H������˝�˛ܙ�̌�ݙȈ�Y]Л�H�
���YH��ZY�H�����[\�H�H����OH����H�����OH�N��[H��Y
Y��X�]OH��MH�ς�[\�H�H�L��OH����H�����OH�N��[H��؎�����X�]OH��MH�ς�]H�L�M�LNM�M���LL��M͈LM

�

L�

�̈

L�
�

�M

�

�M
�



MN


N͈M��
M���MMM�
�M�L�L��ML̈L��M�����[H��ۙH�����OH��؎��������K]�YH����X�]OH��ȋς�[�HOH��LOH�M���H��L�H�
�����OH�͌MY�H�����K]�YH�K�H��X�]OH��H�ς�]H�L��L��̈�L͈�
���[H��ۙH�����OH�͌MY�H�����K]�YH�K�H��X�]OH����ς�]H�M�M
�
�ML��
M����[H��ۙH�����OH�͌MY�H�����K]�YH�K�H��X�]OH����ς�]H�L��L���̈���[H��ۙH�����OH�͌MY�H�����K]�YH�K�H��X�]OH����ς�]H�M�ML��
N���[H��ۙH�����OH�͌MY�H�����K]�YH�K�H��X�]OH����ς��\��H�H�����OH����H����[H�ٍNYL��ς��\��H�H�N��OH����H����[H�ٍNYL��ς��\��H�H���OH�����H����[H��L�NH�ς��ݙψ������Ց��Q��S�H���ݙ�[��H������˝�˛ܙ�̌�ݙȈ�Y]Л�H�̈̈��YH����ZY�H�������\��H�H�M���OH�LȈ�H�Ȉ�[H�ٙM�H�ς��X�H�LȈOH����YH���ZY�H����H�H��[H�ٙM�H�ς��X�H�LˍH�OH��Ȉ�YH�H�ZY�H����H�H��[H�ٙM�H�ς�[�HOH�M��LOH���H�M��L�H�������OH�٘���������K]�YH�K�H�����K[[�X�\H���[��ς�[�HOH��ȈLOH�Ȉ�H��H�L�H�H�����OH�٘���������K]�YH�K�H�����K[[�X�\H���[��ς�[�HOH�H�LOH�Ȉ�H�ȈL�H�H�����OH�٘���������K]�YH�K�H�����K[[�X�\H���[��ς�[�HOH����LOH�LȈ�H���L�H�LȈ����OH�٘���������K]�YH�K�H�����K[[�X�\H���[��ς�[�HOH���LOH�LȈ�H��L�H�LȈ����OH�٘���������K]�YH�K�H�����K[[�X�\H���[��ς��ݙψ������Ց���T�H���ݙ�[��H������˝�˛ܙ�̌�ݙȈ�Y]Л�H�
L��YH��ZY�H�L����X�H�H�OH����YH�L��ZY�H�MH��H����[H��؎�����X�]OH���ς��X�H����OH����YH�L��ZY�H��H��H����[H��؎�����X�]OH��H�ς��X�H��H�OH�L��YH�L��ZY�H��H��H����[H��Y
Y�ς��X�H�M��OH�H��YH�L��ZY�H���H����[H��YMY��ς�[�HOH�H�LOH�
H��H��H�L�H�
H�����OH��L��Y������K]�YH�H�ς��[[�H�[��H�LK���

KL
��
H��[H��ۙH�����OH�ٍNYL������K]�YH�K�H�����KY\�\��^OH����ς��\��H�H�LH��OH����H���H��[H�ٍNYL��ς��\��H�H����OH����H���H��[H�ٍNYL��ς��\��H�H�
H��OH�L��H���H��[H�ٍNYL��ς��\��H�H�����OH�H��H���H��[H�ٍNYL��ς��ݙψ������Ց����TH���ݙ�[��H������˝�˛ܙ�̌�ݙȈ�Y]Л�H�
L
��YH�L�ZY�H�����X�H���OH����YH�
��ZY�H�͈��H����[H��YL�L؈�ς��X�H���OH����YH�
��ZY�H�L��H����[H����MMH�ς��\��H�H�L��OH�Ȉ�H����[H��Y�


�ς��\��H�H�MȈ�OH�Ȉ�H����[H�٘�����ς��\��H�H����OH�Ȉ�H����[H�̌��MYH�ς�^H�ȈOH��Ȉ�۝Y�[Z[OH�[ۛ��X�H��۝\�^�OH�Ȉ�[H���٘ȏ������^���X�H�M��OH�NH��YH���ZY�H����H�H��[H��
�MM�H�ς��X�H�ȈOH��Ȉ�YH���ZY�H����H�H��[H����MMH�ς��X�H�ȈOH�̈��YH���ZY�H����H�H��[H����MMH�ς��ݙψ������Ց���T�H���ݙ�[��H������˝�˛ܙ�̌�ݙȈ�Y]Л�H�����YH���ZY�H������Y�ۈ�[��H�L��MK�K�����K���M�M�MN�N�K��L�Mˍ��
K���K��
�M�M�K����LK������[H�ٍNYL������OH��M��
������K]�YH��H�ς��ݙψ������d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d�����
��[][�0��]\�\��\��[ۜ�B��8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d8�d������H����Y�H��^�N�M�X\��[��L�[HM[[HL�[HM[[N�B�����\�^�[�Θ�ܙ\�X���X\��[���Y[�Ό�B���^��۝Y�[Z[N���Y��HRI�\�X[	�[�]X�H�]YI��[��\�\�Y���۝\�^�N�\�[�KZZY��K�MN���܎��YL�L�N��X��ܛ�[���]N�B������X��ܛ�[��[�X\�YܘYY[�
L�YY��LM��	K����MH

IK�XMNYHL	JN��ܙ\�\�Y]\ΌL��Y[�Ό�X\��[�X���N�M��ݙ\���ΚY[����][ێ��[]]�N�B���XX��[��ZY��\��X��ܛ�[��[�X\�YܘYY[�
LY�ٍNYL�	K�؎���
	K�L�NHL	JN�B���X��^�Y[�ΌN�N���][ێ��[]]�N�B���Y^YX������۝\�^�N�ˍ\��۝]�ZY����]\�\�X�[�Ό��\�^]�[�ٛܛN�\\��\�N���܎��L��Y��^X[Yێ��[�\��X\��[�X���N���B���]]^��۝\�^�N��\��۝]�ZY��L�^X[Yێ��[�\����܎��]N�]\�\�X�[�΋L�\�[�KZZY��K�MN�X\��[�X���N�\�B���Z��\���۝\�^�N�L\��۝]�ZY����^X[Yێ��[�\����܎�ٙM�N�X\��[�X���N��]\�\�X�[�Ό\�B���\�X���۝\�^�N�K�\�^X[Yێ��[�\����܎�ؙ���N�X\��[�X���N�M�B���X�Y�\��\�^N��^��\�Y�KX�۝[���[�\���\��X\��[�X���N�M�B���X�Y�^��X��ܛ�[���ؘJ�MK�MK�MK�JN��ܙ\��\��Y�ؘJ�MK�MK�MK��N���܎��]N��۝\�^�N�ˍ\��۝]�ZY����Y[�΍L���ܙ\�\�Y]\Ό��B�����]ܘ\��X��ܛ�[���ؘJ��N��ܙ\�\�Y]\ΌL�ZY���X\��[��
�B�����[X�[�^X[Yێ��Y��X\��[���
��۝\�^�N�����܎��L��Y��B�����\�^N��^�[YۋZ][\Θ�[�\���\��Y[�ΎM��ܙ\�\�Y]\Ύ���܎��]N��۝\�^�N�L��۝]�ZY���X\��[�]��M�X\��[�X���N�L�Y�KX��XZ�XY�\��]��Y�B���[Y���Y���ZY����B���^��X��ܛ�[��[�X\�YܘYY[�
LY��Y
Y�؎���N�B��̞��X��ܛ�[��[�X\�YܘYY[�
LY��MN�̌��MYJN�B������X��ܛ�[��[�X\�YܘYY[�
LY�؎LX�X��Y�



N�B�����X��ܛ�[��[�X\�YܘYY[�
LY�͙�K��Xٍ�N�B���^��X��ܛ�[��[�X\�YܘYY[�
LY��M�L�
���

N�B��͞��X��ܛ�[��[�X\�YܘYY[�
LY����MLK͘�̎
N�B������X��ܛ�[��[�X\�YܘYY[�
LY�؍
L�KٍNYL�N�B�����X��ܛ�[��[�X\�YܘYY[�
LY��LM���YL�M�JN�B����\���X��ܛ�[��َ�Y����ܙ\��\��Y�L�N���ܙ\�\�Y]\Ύ�Y[�ΌL�M�X\��[�X���N��Y�KX��XZ�Z[��YN�]��Y�B���[�]��ܙ\�[Y����Y�؎�����X��ܛ�[���Y���ff6ff; padding:9px 12px; border-radius:0 7px 7px 0; margin-bottom:8px; page-break-inside:avoid; }
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


# ══════════════════════════════════════════════════════════════
# HTML BUILDER (interne)
# ══════════════════════════════════════════════════════════════

def _build_html(c: dict, jour: int, date_str: str) -> str:
    pct = min(100.0, round(jour / 30 * 100, 1))
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
          <div class="micro-label">📌 CE QU'IL S'EST PASSÉ</div>
          <p style="margin-bottom:8px;font-size:8.5pt;">{n['what']}</p>
          <div class="news-pour" style="border-color:{n['color']};background:{n['color']}18;">
            <div class="micro-label" style="color:{n['color']};">🎯 POUR TOI</div>
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

    edition      = c.get("edition", f"Jour {jour} · Formation IA")
    quote        = c.get("quote", "La connaissance s'acquiert par l'expérience, tout le reste n'est qu'information.")
    quote_author = c.get("quote_author", "— Albert Einstein")
    motto        = c.get("motto", "🚀 Une brique par jour — dans 30 jours tu seras méconnaissable.")

    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><style>{_CSS}</style></head>
<body>

<div class="hdr">
  <div class="hdr-accent"></div>
  <div class="hdr-body">
    <img src="{neural_b64}" style="width:380px;height:auto;position:absolute;right:0;top:0;opacity:0.35;"/>
    <div class="hdr-eyebrow">🤖 &nbsp;Brief IA Quotidien &nbsp;·&nbsp; Formation Accélérée</div>
    <div class="hdr-jour">✦ JOUR {jour} / 30 ✦</div>
    <div class="hdr-title">{c['s1_titre']}</div>
    <div class="hdr-sub">{date_str} &nbsp;·&nbsp; {edition}</div>
    <div class="hdr-badges">
      <span class="hdr-badge">⏱️ ~8 min de lecture</span>
      <span class="hdr-badge">🎯 Niveau Débutant</span>
      <span class="hdr-badge">📅 Jour {jour} · IA Fondamentaux</span>
    </div>
    <div class="prog-wrap"><div style="{prog_bar}"></div></div>
    <div class="prog-label">Progression : Jour {jour} sur 30 &nbsp;·&nbsp; {pct}% accompli 🚀</div>
  </div>
</div>

<div class="sh c1"><img src="{bulb_b64}"/> 💡 &nbsp;1. Le concept IA du jour</div>
<div class="section-title">{c['s1_titre']}</div>
<div class="micro-label" style="color:#1d4ed8;">📖 EN VERSION SIMPLE</div>
<div class="callout" style="margin-bottom:9px;">{c['s1_simple']}</div>
<div class="micro-label" style="color:#b45309;">🔍 ANALOGIE DU QUOTIDIEN</div>
<div class="callout amber" style="margin-bottom:9px;">{c['s1_analogy']}</div>
<div style="display:flex;gap:9px;margin-bottom:8px;">
  <div class="card" style="flex:1;border-color:#bfdbfe;">
    <div class="micro-label" style="color:#1d4ed8;">💬 EXEMPLE CONCRET</div>
    <div style="margin-top:4px;">{c['s1_exemple']}</div>
  </div>
  <div class="card" style="flex:1;border-color:#bfdbfe;">
    <div class="micro-label" style="color:#15803d;">⚡ POURQUOI C'EST IMPORTANT</div>
    <div style="margin-top:4px;">{c['s1_important']}</div>
  </div>
</div>

<div class="sh c2">📖 &nbsp;2. Le mot technique à connaître</div>
{ro-label" style="color:#b45309;">🔍 ANALOGIE DU QUOTIDIEN</div>
<div class="callout amber" style="margin-bottom:9px;">{c['s1_analogy']}</div>
<div style="display:flex;gap:9px;margin-bottom:8px;">
  <div class="card" style="flex:1;border-color:#bfdbfe;">
    <div class="micro-label" style="color:#1d4ed8;">💬 EXEMPLE CONCRET</div>
    <div style="margin-top:4px;">{c['s1_exemple']}</div>
  </div>
  <div class="card" style="flex:1;border-color:#bfdbfe;">
    <div class="micro-label" style="color:#15803d;">⚡ POURQUOI C'EST IMPORTANT</div>
    <div style="margin-top:4px;">{c['s1_important']}</div>
  </div>
</div>

<div class="sh c2">📖 &nbsp;2. Le mot technique à connaître</div>
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
    <div style="font-size:7pt;color:#6b7280;margin-top:4px;">Données → Résultat</div>
  </div>
</div>

<div class="sh c3">📰 &nbsp;3. L'actualité IA importante du jour</div>
{news_html}

<div class="sh c4">🛠️ &nbsp;4. L'outil IA du jour</div>
<div style="display:flex;gap:12px;align-items:flex-start;">
  <div style="text-align:center;padding-top:4px;">
    <img src="{robot_b64}" style="width:65px;height:auto;"/>
    <div style="font-size:7.5pt;color:#7c3aed;font-weight:700;margin-top:4px;">IA Tool</div>
  </div>
  <div style="flex:1;"><table class="tool-tbl">{tool_html}</table></div>
</div>

<div class="sh c5">✏️ &nbsp;5. Mini exercice pratique (5 minutes max)</div>
<div class="card" style="background:#f0fdfd;border-color:#a5f3fc;">
  <p style="margin-bottom:10px;"><strong>🎯 Objectif :</strong> {c['s5_objectif']}</p>
  {steps_html}
  <div style="background:#ccfbf1;border:1px solid #5eead4;border-radius:7px;padding:9px 12px;margin-top:8px;color:#0f766e;">
    ✅ &nbsp;<strong>Résultat attendu :</strong> {c['s5_resultat']}
  </div>
</div>

<div class="sh c6"><img src="{prompt_b64}"/> 📋 &nbsp;6. Prompt prêt à copier</div>
<div class="card" style="border-color:#d1d5db;background:#f9fafb;margin-bottom:8px;">
  <p><strong>🎯 Ce que fait ce prompt :</strong> {c['s6_desc']}</p>
  <p style="margin-top:5px;font-size:8.5pt;color:#4b5563;">{c['s6_usage']}</p>
</div>
<div class="prompt-hdr">
  <span class="prompt-dot" style="background:#ef4444;"></span>
  <span class="prompt-dot" style="background:#f59e0b;"></span>
  <span class="prompt-dot" style="background:#22c55e;"></span>
  <span style="font-size:7.5pt;color:#94a3b8;margin-left:4px;font-family:monospace;">prompt.txt &nbsp;·&nbsp; Copier-Coller dans ChatGPT</span>
</div>
<div class="prompt-box">{c['s6_prompt']}</div>

<div class="sh c7"><img src="{star_b64}"/> 💡 &nbsp;7. Astuce IA du jour</div>
<div class="astuce">
  <p style="font-weight:800;font-size:10pt;color:#78350f;margin-bottom:10px;">
    🎭 &nbsp;Donne toujours un <em>rôle</em> à l'IA avant de poser ta question.
  </p>
  <div class="bad-box">❌ &nbsp;<strong>Au lieu de :</strong> {c['s7_bad']}</div>
  <div class="good-box">✅ &nbsp;<strong>Dis plutôt :</strong> {c['s7_good']}</div>
  <div class="tip-note">
    💬 &nbsp;La réponse sera immédiatement plus précise, plus adaptée et plus utile.
    C'est la <strong>règle n°1 du prompting</strong> — retiens-la bien.
  </div>
</div>

<div class="sh c8"><img src="{brain_b64}"/> 🧠 &nbsp;8. Ce qu'il faut retenir aujourd'hui</div>
{recap_html}

<div class="footer">
  <div class="quote-mark">"</div>
  <div class="footer-quote">{quote}</div>
  <div class="footer-author">{quote_author}</div>
  <div class="footer-motto">{motto}</div>
  <div class="footer-meta">Brief IA Quotidien &nbsp;·&nbsp; {date_str} &nbsp;·&nbsp; Jour {jour} / 30</div>
</div>

</body></html>"""


# ══════════════════════════════════════════════════════════════
# FONCTION PRINCIPALE — API publique
# ══════════════════════════════════════════════════════════════

def generate_brief_pdf(
    content_bryan: dict,
    content_aaron: dict,
    jour: int,
    date_str: str,
    output_dir : str = ".",
    prefix: str = "brief-ia"
) -> tuple:
    """
    Génère deux PDFs premium (Bryan et Aaron) à partir des dicts de contenu.

    Paramètres :
        content_bryan   — dict avec tout le contenu de la version Bryan (orthodontie)
        content_aaron   └ dict avec tout le contenu de la version Aaron (expert-comptable)
        jour           — numéro du jour (1 à 30)
        date_str       — ex. "18 mai 2026"
        output_dir     — répertoire de sortie
        prefix         — préfixe du fichier (ex. "brief-ia")

    Retourne :
        (chemin_bryan, chemin_aaron)
    """
    os.makedirs(output_dir, exist_ok=True)
    paths = {}
    for version, content in [("bryan", content_bryan), ("aaron", content_aaron)]:
        html = _build_html(content, jour, date_str)
        out  = os.path.join(output_dir, f"{prefix}-jour{jour}-{version}.pdf")
        HTML(string=html).write_pdf(out)
        print(f"✅  {out}")
        paths[version] = out
    return paths["bryan"], paths["aaron"]
