"""Algorithme décisionnel de la fiche NE-04 : thrombolyse, thrombectomie ou les deux (AHA/ASA 2026). Lancer : python3 src/gen/algo.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import T, save, INK, MUT, LINE, NOTE, R5, DR, G1, DG, B

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
    s = '<svg viewBox="0 0 520 344" role="img" style="width:100%;height:auto"><title>Algorithme : thrombolyse et thrombectomie</title>'
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
    s += box(20, 160, 245, 34, G1)
    s += T(28, 173, "0–6 h · ASPECTS 3–10 · NIHSS ≥ 6 · mRS 0–1", 6.8, 700, DG, 'start')
    s += T(28, 185, "classe 1 A · thrombectomie recommandée", 6.2, 400, MUT, 'start')
    s += chip(208, 169, 49, GRN, '#fff', "EVT ✓")
    s += box(20, 200, 245, 22, G1)
    s += T(28, 214, "6–24 h · ASPECTS ≥ 6 · classe 1 A", 6.8, 700, DG, 'start')
    s += chip(208, 203, 49, GRN, '#fff', "EVT ✓")
    s += box(20, 228, 245, 34, G1)
    s += T(28, 241, "6–24 h · ASPECTS 3–5 · &lt; 80 ans", 6.8, 700, DG, 'start')
    s += T(28, 253, "sans effet de masse · patients sélectionnés", 6.2, 400, MUT, 'start')
    s += chip(208, 237, 49, GRN, '#fff', "EVT ✓")
    s += box(20, 268, 245, 34, GREY)
    s += T(28, 280, "hors cases → CTP validé ou IRM de diffusion", 6.8, 700, INK, 'start')
    s += T(28, 292, "profils DAWN / DEFUSE 3 → EVT ✓ · sinon pas d'EVT", 6.3, 400, INK, 'start')
    # Colonne droite : thrombolyse
    s += box(285, 104, 150, 14, B) + T(360, 114, "VOIE THROMBOLYSE", 6.6, 700, BLU)
    s += box(285, 124, 215, 46, B)
    s += T(293, 138, "dernier contact normal &lt; 4,5 h", 6.8, 700, BLU, 'start')
    s += T(293, 149, "IVT immédiate · TNK 0,25 mg/kg · max 25 mg", 6.3, 400, INK, 'start')
    s += T(293, 160, "sans attendre l'imagerie avancée", 6.2, 400, MUT, 'start')
    s += chip(452, 139, 42, BLU, '#fff', "IVT ✓")
    s += box(285, 176, 215, 46, GREY)
    s += T(293, 190, "4,5–9 h ou réveil", 6.8, 700, BLU, 'start')
    s += T(293, 201, "cœur &lt; 70 mL · ratio &gt; 1,2 · mismatch &gt; 10 mL", 6.1, 400, INK, 'start')
    s += T(293, 212, "ou mismatch FLAIR–DWI à l'IRM (EXTEND)", 6.2, 400, MUT, 'start')
    s += chip(452, 191, 42, BLU, '#fff', "IVT ✓")
    s += box(285, 228, 215, 46, GREY)
    s += T(293, 242, "4,5–24 h · classe 2b", 6.8, 700, BLU, 'start')
    s += T(293, 253, "LVO + tissu sauvable, sans option d'EVT", 6.3, 400, INK, 'start')
    s += T(293, 264, "(transfert impossible, cas marginal)", 6.2, 400, MUT, 'start')
    s += chip(452, 243, 42, MUT, '#fff', "IVT ?")
    s += box(285, 282, 215, 16, GREY) + T(392, 293, "contre-indications de l'IVT → fiche NE-01", 6.2, 400, MUT)
    # Bandeau bridging
    s += box(20, 308, 480, 26, G1)
    s += T(260, 325, "Éligible aux deux = les deux (bridging) · l'IVT part sans attendre et ne retarde jamais l'EVT", 7, 700, DG)
    s += T(0, 341, NOTE + " · adulte, circulation antérieure · cohérence finale avec l'occlusion, l'ASPECTS et la clinique", 6, 400, MUT, 'start')
    save('ne04b.svg', s + '</svg>')


if __name__ == '__main__':
    build(); print('ok')
