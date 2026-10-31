"""Algorithme décisionnel de la fiche NE-04 : thrombolyse, thrombectomie ou les deux (AHA/ASA 2026). Lancer : python3 src/gen/algo.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import T, save, INK, MUT, LINE, NOTE, R5, DR, DO, G1, DG, B, P

GREY = '#f4f6f8'; BORD = '#d5dae1'; BLU = '#1F4E8C'; GRN = '#1C6B3E'


def box(x, y, w, h, fill, stroke=BORD, r=5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="0.8"/>'


def chip(x, y, w, bg, fg, label):
    return f'<rect x="{x}" y="{y}" width="{w}" height="15" rx="3" fill="{bg}"/>' + T(x + w / 2, y + 11.2, label, 7, 700, fg)


def varr(x, y1, y2):
    return (f'<path d="M{x},{y1} L{x},{y2 - 3.5}" stroke="{LINE}" stroke-width="1" fill="none"/>'
            f'<path d="M{x - 2.8},{y2 - 4.5} L{x},{y2} L{x + 2.8},{y2 - 4.5}Z" fill="{LINE}"/>')


def harr(x1, y, x2):
    return (f'<path d="M{x1},{y} L{x2 - 3.5},{y}" stroke="{LINE}" stroke-width="1" fill="none"/>'
            f'<path d="M{x2 - 4.5},{y - 2.8} L{x2},{y} L{x2 - 4.5},{y + 2.8}Z" fill="{LINE}"/>')


def build():
    s = '<svg viewBox="0 0 520 452" role="img" style="width:100%;height:auto"><title>Algorithme : thrombolyse, thrombectomie ou les deux</title>'
    s += T(0, 11, "Décision : thrombolyse, thrombectomie ou les deux · AHA/ASA 2026", 9, 700, INK, 'start')
    # Porte d'entrée : scanner sans injection
    s += box(20, 20, 250, 30, GREY)
    s += T(145, 32, "Scanner sans injection", 7, 700, INK) + T(145, 42, "hémorragie ? · ASPECTS · dans les 25 minutes", 6.2, 400, MUT)
    s += harr(272, 35, 294) + T(283, 30, "oui", 6, 400, MUT)
    s += box(296, 20, 204, 30, R5, DR)
    s += T(398, 32, "Hémorragie", 7, 700, DR) + T(398, 42, "ni thrombolyse ni thrombectomie", 6.2, 400, DR)
    s += varr(145, 50, 61) + T(152, 58, "non", 6, 400, MUT, 'start')
    # Données communes aux deux voies
    s += box(20, 62, 480, 32, GREY)
    s += T(260, 74, "Angioscanner · NIHSS · âge · mRS préalable · heure du dernier contact normal", 7.2, 700, INK)
    s += T(260, 86, "les deux voies s'évaluent en parallèle — aucune ne retarde l'autre", 6.4, 400, MUT)
    s += varr(145, 94, 103) + varr(392, 94, 103)
    # Colonne gauche : thrombectomie
    s += box(20, 104, 205, 14, G1) + T(122, 114, "VOIE THROMBECTOMIE · cible : ACI / M1", 6.6, 700, DG)
    s += box(20, 124, 245, 30, GREY)
    s += T(28, 136, "Occlusion proximale (ACI terminale ou M1) ?", 6.9, 700, INK, 'start')
    s += T(28, 148, "distale ou absente : pas d'EVT systématique", 6.2, 400, MUT, 'start')
    # 0-6 h : EVT sans CTP
    s += box(20, 160, 245, 34, G1)
    s += T(28, 171, "0–6 h · ASPECTS 3–10 · NIHSS ≥ 6 · mRS 0–1", 6.8, 700, DG, 'start')
    s += T(28, 182, "thrombectomie recommandée (classe 1 A)", 6.2, 400, MUT, 'start')
    s += T(28, 192, "CTP inutile — ne pas retarder l'EVT", 6.2, 700, DO, 'start')
    s += chip(206, 168, 51, GRN, '#fff', "EVT ✓")
    # 6-24 h : EVT sélectionné par CTP
    s += box(20, 200, 245, 34, G1)
    s += T(28, 211, "6–24 h · ASPECTS ≥ 6 · classe 1 A", 6.8, 700, DG, 'start')
    s += T(28, 223, "CTP ou IRM requise · seuils DAWN / DEFUSE 3", 6.2, 400, MUT, 'start')
    s += T(28, 233, "→ valeurs ci-dessous", 6.2, 400, MUT, 'start')
    s += chip(206, 203, 51, GRN, '#fff', "EVT ✓") + chip(206, 219, 51, P, '#4B2A8A', "CTP ✓")
    # 6-24 h cœur étendu
    s += box(20, 240, 245, 34, G1)
    s += T(28, 251, "6–24 h · ASPECTS 3–5 · &lt; 80 ans · sélectionnés", 6.8, 700, DG, 'start')
    s += T(28, 263, "sans effet de masse · un cœur &gt; 70 mL n'exclut plus seul", 6.2, 400, MUT, 'start')
    s += T(28, 273, "CTP ou IRM pour guider la décision", 6.2, 700, DO, 'start')
    s += chip(206, 243, 51, GRN, '#fff', "EVT ✓") + chip(206, 259, 51, P, '#4B2A8A', "CTP ✓")
    # hors cases
    s += box(20, 280, 245, 26, GREY)
    s += T(28, 291, "hors cases : CTP (logiciel validé) ou IRM", 6.6, 700, INK, 'start')
    s += T(28, 302, "profil DAWN / DEFUSE 3 → EVT ✓ · sinon pas d'EVT", 6.2, 400, INK, 'start')
    # Colonne droite : thrombolyse
    s += box(285, 104, 150, 14, B) + T(360, 114, "VOIE THROMBOLYSE", 6.6, 700, BLU)
    s += box(285, 124, 215, 46, B)
    s += T(293, 136, "dernier contact normal &lt; 4,5 h", 6.8, 700, BLU, 'start')
    s += T(293, 147, "IVT immédiate · TNK 0,25 mg/kg · max 25 mg", 6.3, 400, INK, 'start')
    s += T(293, 158, "CTP inutile — ne pas attendre l'imagerie avancée", 6.2, 700, DO, 'start')
    s += chip(452, 139, 42, BLU, '#fff', "IVT ✓")
    s += box(285, 176, 215, 46, GREY)
    s += T(293, 188, "4,5–9 h ou réveil", 6.8, 700, BLU, 'start')
    s += T(293, 199, "EXTEND : cœur &lt; 70 mL · ratio &gt; 1,2", 6.1, 400, INK, 'start')
    s += T(293, 209, "mismatch &gt; 10 mL (ou FLAIR–DWI à l'IRM)", 6.1, 400, INK, 'start')
    s += T(293, 219, "CTP ou IRM requise → valeurs ci-dessous", 6.2, 700, DO, 'start')
    s += chip(452, 183, 42, BLU, '#fff', "IVT ✓") + chip(452, 199, 42, P, '#4B2A8A', "CTP ✓")
    s += box(285, 228, 215, 34, GREY)
    s += T(293, 240, "4,5–24 h · classe 2b", 6.8, 700, BLU, 'start')
    s += T(293, 251, "LVO + tissu sauvable, sans option d'EVT", 6.3, 400, INK, 'start')
    s += T(293, 261, "(transfert impossible, cas marginal)", 6.2, 400, MUT, 'start')
    s += chip(452, 235, 42, MUT, '#fff', "IVT ?")
    s += box(285, 268, 215, 16, GREY) + T(392, 279, "contre-indications de l'IVT → fiche NE-01", 6.2, 400, MUT)
    # Bandeau : quand faire la CTP
    s += box(20, 300, 480, 26, P)
    s += T(260, 313, "Quand faire la perfusion ?", 7, 700, '#4B2A8A')
    s += T(260, 323, "inutile si la décision est claire (IVT &lt; 4,5 h · EVT 0–6 h avec ASPECTS fiable) · indispensable pour la décision à 4,5–9 h (réveil) et 6–24 h", 6.3, 700, '#4B2A8A')
    # Bandeau bridging
    s += box(20, 332, 480, 24, G1)
    s += T(260, 348, "Éligible aux deux = les deux (bridging) · l'IVT part sans attendre et ne retarde jamais l'EVT", 7, 700, DG)
    # Panneau des seuils à transmettre au neurologue
    s += box(20, 362, 480, 74, '#fff', '#4B2A8A')
    s += T(28, 373, "CTP · valeurs seuils à transmettre au neurologue", 7.2, 700, '#4B2A8A', 'start')
    s += T(28, 383, "format des essais (logiciel RAPID : cœur = rCBF &lt; 30 % · hypoperfusion = Tmax &gt; 6 s) — défaut ISP : voir fiche", 6, 400, MUT, 'start')
    # DEFUSE 3
    s += T(28, 396, "DEFUSE 3 · 6–16 h", 6.6, 700, INK, 'start')
    s += T(28, 406, "cœur &lt; 70 mL", 6.3, 400, INK, 'start')
    s += T(28, 415, "ratio ≥ 1,8 · pénombre ≥ 15 mL", 6.3, 400, INK, 'start')
    s += T(28, 426, "→ EVT ✓", 6.4, 700, DG, 'start')
    # DAWN
    s += T(190, 396, "DAWN · 6–24 h", 6.6, 700, INK, 'start')
    s += T(190, 406, "≥ 80 ans : NIHSS ≥ 10 · cœur &lt; 21 mL", 6.3, 400, INK, 'start')
    s += T(190, 415, "&lt; 80 ans : NIHSS ≥ 10 · cœur &lt; 31 mL", 6.3, 400, INK, 'start')
    s += T(190, 426, "&lt; 80 ans : NIHSS ≥ 20 · cœur 31–51 mL → EVT ✓", 6.3, 400, INK, 'start')
    # EXTEND
    s += T(355, 396, "EXTEND · IVT 4,5–9 h / réveil", 6.6, 700, INK, 'start')
    s += T(355, 406, "cœur &lt; 70 mL", 6.3, 400, INK, 'start')
    s += T(355, 415, "ratio &gt; 1,2 · mismatch &gt; 10 mL", 6.3, 400, INK, 'start')
    s += T(355, 426, "→ IVT ✓", 6.4, 700, BLU, 'start')
    s += T(0, 447, NOTE + " · adulte, circulation antérieure · cohérence finale avec l'occlusion, l'ASPECTS et la clinique", 6, 400, MUT, 'start')
    save('ne04b.svg', s + '</svg>')

if __name__ == '__main__':
    build(); print('ok')
