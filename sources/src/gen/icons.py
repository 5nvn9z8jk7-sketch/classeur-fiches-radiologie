"""Bibliothèque de schémas simplifiés (SVG) pour les pages « Atlas visuel » du classeur."""
import math, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
INK = '#1d2430'; MUT = '#7a8492'; LINE = '#4a5462'; BG = '#f8f9fb'; GR = '#e6e9ee'
Y3 = '#FCEFC7'; O4 = '#FBD9BD'; R5 = '#F6C1C1'; G1 = '#D4F0DF'; B = '#DCE8F8'; P = '#E5DCF7'
DR = '#8B1A1A'; DO = '#8A3A0F'; DY = '#7A5200'; DG = '#1C6B3E'

def T(x, y, s, size=9, w=400, fill=INK, anchor='middle'):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{w}" fill="{fill}" font-family="IS">{s}</text>'

def tiles(items, cols, tw=118, th=96, gap=10, cap=24, title=None, note=None):
    """items: list of (svg_inner_drawn_in_0..tw x 0..th, caption, subcaption, chipclass)"""
    rows = math.ceil(len(items) / cols)
    W = cols * tw + (cols - 1) * gap
    top = 16 if title else 0
    H = top + rows * (th + cap + gap) + (14 if note else 0)
    s = f'<svg viewBox="0 0 {W} {H}" role="img" style="width:100%;height:auto"><title>{title or "schéma"}</title>'
    if title: s += T(0, 11, title, 9.5, 700, INK, 'start')
    for i, it in enumerate(items):
        inner, c1, c2 = it[0], it[1], it[2] if len(it) > 2 else ''
        col = it[3] if len(it) > 3 else None
        x = (i % cols) * (tw + gap); y = top + (i // cols) * (th + cap + gap)
        s += f'<g transform="translate({x},{y})"><rect x="0" y="0" width="{tw}" height="{th}" rx="6" fill="#fff" stroke="#d5dae1" stroke-width="0.8"/>{inner}'
        n1 = len(c1.replace('&lt;','<').replace('&gt;','>')); n2 = len(c2.replace('&lt;','<').replace('&gt;','>'))
        f1 = min(9, (tw - 14) / (n1 * 0.6)); f2 = min(7.5, (tw - 4) / (max(n2, 1) * 0.52))
        cwid = min(tw - 2, n1 * f1 * 0.62 + 12)
        if col:
            s += f'<rect x="{tw/2-cwid/2:.1f}" y="{th+3}" width="{cwid:.1f}" height="13" rx="3" fill="{col[0]}"/>' + T(tw/2, th + 13, c1, f1, 700, col[1])
        else:
            s += T(tw/2, th + 13, c1, f1, 700)
        if c2: s += T(tw/2, th + 23, c2, f2, 400, MUT)
        s += '</g>'
    if note: s += T(0, H - 3, note, 7.2, 400, MUT, 'start')
    return s + '</svg>'

NOTE = 'Schémas simplifiés, non à l\'échelle'
CHIP = {1: (G1, DG), 2: ('#E3F3D2', '#3D6B12'), 3: (Y3, DY), 4: (O4, DO), 5: (R5, DR), 0: ('#E4E7EC', '#3A4250'), 'b': (B, '#1F4E8C'), 'p': (P, '#4B2A8A')}

def save(name, svg):
    open(os.path.join(OUT, name), 'w').write(svg)

# ---------------- Neuro : SEP ----------------
def sep():
    it = []
    # périventriculaire : ventricule + ovoïdes perpendiculaires (doigts de Dawson)
    v = f'<path d="M30,48 C30,30 88,30 88,48 C88,58 70,60 59,52 C48,60 30,58 30,48Z" fill="#cfd8e3"/>'
    for a, x in [(-60, 40), (-80, 54), (-100, 66), (-120, 78)]:
        v += f'<ellipse cx="{x}" cy="26" rx="4" ry="9" transform="rotate({a+90} {x} 26)" fill="#fff" stroke="{INK}" stroke-width="0" />'
    v += ''.join(f'<ellipse cx="{x}" cy="25" rx="3.5" ry="9" fill="#f2f2f2" stroke="{LINE}" stroke-width="0.6" transform="rotate({r} {x} 25)"/>' for x, r in [(40, -25), (53, -8), (66, 8), (79, 25)])
    v += T(59, 80, 'contact ventriculaire', 7.5, 400, MUT)
    it.append((v, 'Périventriculaire', 'ovoïdes ⟂ ventricules'))
    # juxtacortical
    v = f'<path d="M10,30 Q59,0 108,30 L108,40 Q59,12 10,40Z" fill="#d9dee5"/><ellipse cx="59" cy="31" rx="7" ry="5" fill="#f2f2f2" stroke="{LINE}" stroke-width="0.6"/>' + T(59, 60, 'au contact du cortex', 7.5, 400, MUT) + T(59, 72, 'ou dans le cortex', 7.5, 400, MUT)
    it.append((v, 'Cortical / juxtacortical', ''))
    # sous-tentoriel
    v = f'<ellipse cx="59" cy="34" rx="14" ry="18" fill="#d9dee5"/><path d="M20,70 Q59,44 98,70 Q59,90 20,70Z" fill="#e6e9ee"/><circle cx="64" cy="32" r="4" fill="#f2f2f2" stroke="{LINE}" stroke-width="0.6"/><circle cx="40" cy="70" r="3.5" fill="#f2f2f2" stroke="{LINE}" stroke-width="0.6"/>' + T(59, 92, 'tronc · cervelet', 7.5, 400, MUT)
    it.append((v, 'Sous-tentoriel', ''))
    # moelle
    v = f'<rect x="50" y="8" width="18" height="80" rx="9" fill="#d9dee5"/><ellipse cx="59" cy="44" rx="5" ry="10" fill="#f2f2f2" stroke="{LINE}" stroke-width="0.6"/>' + T(92, 46, '≤ 2 étages', 7.5, 400, MUT)
    it.append((v, 'Moelle', 'lésion courte, périphérique'))
    # nerf optique
    v = f'<circle cx="30" cy="48" r="16" fill="#e6e9ee" stroke="{LINE}" stroke-width="0.6"/><path d="M46,46 L104,40 L104,52 L46,50Z" fill="#d9dee5"/><rect x="62" y="44" width="18" height="6" rx="2" fill="#f2f2f2" stroke="{LINE}" stroke-width="0.6"/>' + T(70, 72, 'T2/STIR, OCT, PEV', 7.5, 400, MUT)
    it.append((v, 'Nerf optique', 'nouvelle 5ᵉ région', CHIP['p']))
    # veine centrale
    v = f'<ellipse cx="59" cy="44" rx="20" ry="28" fill="#f2f2f2" stroke="{LINE}" stroke-width="0.8"/><line x1="59" y1="18" x2="59" y2="70" stroke="{INK}" stroke-width="2.2"/>' + T(59, 88, 'T2* / SWI', 7.5, 400, MUT)
    it.append((v, 'Veine centrale', '≥ 6 lésions positives'))
    # PRL
    v = f'<ellipse cx="59" cy="44" rx="24" ry="28" fill="none" stroke="{INK}" stroke-width="3"/><ellipse cx="59" cy="44" rx="20" ry="24" fill="#f2f2f2"/>' + T(59, 88, 'liseré hypo-intense', 7.5, 400, MUT)
    it.append((v, 'Bord paramagnétique', '≥ 1 PRL'))
    # microvasculaire (piège)
    v = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f2f2f2" stroke="{LINE}" stroke-width="0.6"/>' for x, y, r in [(30, 30, 3), (52, 50, 4), (78, 28, 3), (90, 60, 3.5), (40, 68, 3)]) + T(59, 88, 'ponctuées, sous-corticales', 7.5, 400, MUT)
    it.append((v, 'Microvasculaire', 'pas de veine centrale', CHIP[4]))
    save('ne02.svg', tiles(it, 4, title='Topographie des lésions et biomarqueurs', note=NOTE))

# ---------------- Neuro : trauma ----------------
def trauma():
    def skull(extra):
        return f'<ellipse cx="59" cy="48" rx="44" ry="40" fill="#e6e9ee" stroke="{INK}" stroke-width="3"/>' + extra
    it = []
    it.append((skull(f'<path d="M28,22 Q14,48 28,74 Q40,48 28,22Z" fill="#9aa5b3"/>'), 'Extradural', 'biconvexe, ne franchit pas les sutures'))
    it.append((skull(f'<path d="M40,12 Q12,24 14,52 Q16,76 40,86 Q24,70 24,50 Q24,28 40,12Z" fill="#9aa5b3"/>'), 'Sous-dural', 'croissant, franchit les sutures'))
    it.append((skull(f'<path d="M59,14 L59,82" stroke="#9aa5b3" stroke-width="3"/><path d="M34,30 Q59,40 84,30" stroke="#9aa5b3" stroke-width="2.5" fill="none"/><path d="M30,60 Q44,54 50,66" stroke="#9aa5b3" stroke-width="2.5" fill="none"/>'), 'Sous-arachnoïdienne', 'sillons, citernes, scissures'))
    it.append((skull(f'<circle cx="44" cy="40" r="3" fill="#7a8492"/><circle cx="62" cy="58" r="2.5" fill="#7a8492"/><circle cx="72" cy="36" r="2.5" fill="#7a8492"/><circle cx="56" cy="30" r="2" fill="#7a8492"/>'), 'Lésions axonales diffuses', 'pétéchies jonctionnelles · IRM (SWI)'))
    save('ne03.svg', tiles(it, 4, title='Collections et lésions post-traumatiques', note=NOTE))

# ---------------- Cou : thyroïde ----------------
def thyroid():
    it = []
    it.append((f'<ellipse cx="59" cy="48" rx="34" ry="20" fill="#cfd5dd" stroke="{LINE}"/>' + T(59, 86, 'axe horizontal &gt; vertical', 7.5, 400, MUT), 'Plus large que haut', '0 point', CHIP[1]))
    it.append((f'<ellipse cx="59" cy="46" rx="18" ry="32" fill="#7d8794" stroke="{LINE}"/>' + T(59, 90, 'vertical &gt; horizontal', 7.5, 400, MUT), 'Plus haut que large', '+3 · signe EU-TIRADS 5', CHIP[5]))
    it.append((f'<path d="M30,48 C30,24 54,30 62,24 C76,20 90,34 86,46 C96,58 80,74 66,70 C54,78 30,72 34,60 C24,56 26,50 30,48Z" fill="#7d8794" stroke="{LINE}"/>' + T(59, 90, 'lobulés ou irréguliers', 7.5, 400, MUT), 'Contours irréguliers', '+2 · EU-TIRADS 5', CHIP[5]))
    it.append((f'<ellipse cx="59" cy="46" rx="32" ry="24" fill="#9aa3ae" stroke="{LINE}"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#fff"/>' for x, y in [(48, 40), (60, 34), (70, 48), (54, 54), (66, 58), (44, 50)]) + T(59, 88, 'foyers ponctiformes', 7.5, 400, MUT), 'Microcalcifications', '+3 · EU-TIRADS 5', CHIP[5]))
    it.append((f'<ellipse cx="59" cy="46" rx="32" ry="24" fill="#dfe4ea" stroke="{LINE}"/>' + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="4" fill="#fff" stroke="#b8c0ca" stroke-width="0.5"/>' for x, y in [(44, 40), (56, 36), (68, 40), (78, 48), (48, 52), (60, 50), (72, 56), (56, 60)]) + T(59, 88, 'microkystes &gt; 50 %', 7.5, 400, MUT), 'Spongiforme', 'bénin · 0 point', CHIP[1]))
    it.append((f'<ellipse cx="59" cy="46" rx="32" ry="24" fill="#111827"/><path d="M50,34 l3,0 m-1.5,-1.5 l0,3" stroke="#fff"/><path d="M50,34 L50,46" stroke="#fff" stroke-width="2"/><path d="M50,46 L52,54 L48,54Z" fill="#fff"/>' + T(59, 88, 'artefact en queue de comète', 7.5, 400, MUT), 'Queue de comète', 'colloïde · 0 point', CHIP[1]))
    save('co01.svg', tiles(it, 3, tw=166, th=94, gap=10, title='Signes échographiques clés', note=NOTE))

# ---------------- Sein ----------------
def breast():
    it = []
    def box(inner, sub=''):
        return f'<rect x="10" y="10" width="98" height="64" rx="4" fill="#3b4250"/>' + inner + (T(59, 88, sub, 7.5, 400, MUT) if sub else '')
    rnd = ''.join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="#fff"/>' for x, y in [(40, 30), (52, 36), (64, 30), (58, 48), (44, 50), (70, 44)])
    it.append((box(rnd, 'arrondies, régulières'), 'Rondes', 'souvent bénignes', CHIP[1]))
    pop = '<path d="M44,30 q6,-6 12,0 q6,-6 12,2 q2,10 -8,12 q-12,4 -16,-6Z" fill="#fff"/>'
    it.append((box(pop, 'pop-corn, dystrophiques'), 'Grossières', 'bénignes', CHIP[1]))
    am = ''.join(f'<circle cx="{x}" cy="{y}" r="0.9" fill="#e7e9ee"/>' for x, y in [(44, 32), (48, 38), (52, 30), (58, 40), (62, 34), (66, 42), (54, 46), (46, 44), (60, 50), (70, 36)])
    it.append((box(am, 'petites, floues'), 'Amorphes', 'suspectes (4B)', CHIP[4]))
    fp = ''.join(f'<path d="M{x},{y} l{a},{b}" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>' for x, y, a, b in [(42, 30, 3, 1), (50, 36, 1, 3), (58, 30, 4, 2), (64, 40, 2, -2), (48, 48, 3, 2), (60, 50, 1, 1), (70, 34, 2, 3)])
    it.append((box(fp, 'tailles et formes variées'), 'Fines pléomorphes', 'suspectes (4C)', CHIP[5]))
    fl = '<path d="M30,60 L50,46 L62,38 L80,22 M50,46 L56,58 M62,38 L72,44" stroke="#fff" stroke-width="1.2" fill="none" stroke-dasharray="3 2"/>'
    it.append((box(fl, 'suivent un canal'), 'Fines linéaires branchées', 'très suspectes', CHIP[5]))
    sp = '<circle cx="59" cy="42" r="12" fill="#cfd5dd"/>' + ''.join(f'<line x1="{59+12*math.cos(math.radians(a)):.1f}" y1="{42+12*math.sin(math.radians(a)):.1f}" x2="{59+26*math.cos(math.radians(a)):.1f}" y2="{42+26*math.sin(math.radians(a)):.1f}" stroke="#cfd5dd" stroke-width="1"/>' for a in range(0, 360, 24))
    it.append((box(sp, 'lignes radiaires'), 'Masse spiculée', 'BI-RADS 5', CHIP[5]))
    cir = '<ellipse cx="59" cy="42" rx="20" ry="13" fill="#cfd5dd"/>'
    it.append((box(cir, 'ovale, circonscrite'), 'Masse circonscrite', 'souvent BI-RADS 3', CHIP[3]))
    us = f'<rect x="10" y="10" width="98" height="64" rx="4" fill="#2a2f38"/><ellipse cx="59" cy="34" rx="12" ry="16" fill="#151820"/><rect x="47" y="50" width="24" height="24" fill="#0d0f14"/>' + T(59, 88, 'plus haute que large, ombre', 7.5, 400, MUT)
    it.append((us, 'Échographie', 'non parallèle, atténuation', CHIP[5]))
    save('se01.svg', tiles(it, 4, title='Calcifications et masses : aspects types', note=NOTE + ' · mammographie (fond sombre) et échographie'))

# ---------------- Thorax : nodules ----------------
def nodules():
    lung = '<rect x="8" y="8" width="102" height="72" rx="4" fill="#1f242c"/>'
    it = []
    it.append((lung + '<circle cx="59" cy="44" r="13" fill="#e6e9ee"/>', 'Solide', 'masque le parenchyme'))
    it.append((lung + '<circle cx="59" cy="44" r="18" fill="#6b7480" opacity="0.9"/><circle cx="62" cy="46" r="7" fill="#e6e9ee"/>', 'Partiellement solide', 'mesurer la composante solide', CHIP[4]))
    it.append((lung + '<circle cx="59" cy="44" r="18" fill="#6b7480" opacity="0.8"/><path d="M48,40 L70,48 M52,52 L66,36" stroke="#3a414c" stroke-width="1.5"/>', 'Verre dépoli pur', 'vaisseaux visibles au travers', CHIP[3]))
    it.append((lung + '<line x1="8" y1="30" x2="110" y2="58" stroke="#8b939e" stroke-width="1.2"/><path d="M46,40 L64,45 L54,50Z" fill="#e6e9ee"/>', 'Périscissural', 'triangulaire, &lt; 10 mm : bénin', CHIP[1]))
    meas = lung + '<ellipse cx="59" cy="44" rx="20" ry="12" fill="#e6e9ee" transform="rotate(-20 59 44)"/><line x1="40" y1="51" x2="78" y2="37" stroke="#c2410c" stroke-width="1.2"/><line x1="55" y1="33" x2="63" y2="55" stroke="#1f5fa8" stroke-width="1.2"/>'
    it.append((meas, 'Mesure', '(grand + petit axe) / 2'))
    sp = lung + '<circle cx="59" cy="44" r="11" fill="#e6e9ee"/>' + ''.join(f'<line x1="{59+11*math.cos(math.radians(a)):.1f}" y1="{44+11*math.sin(math.radians(a)):.1f}" x2="{59+22*math.cos(math.radians(a)):.1f}" y2="{44+22*math.sin(math.radians(a)):.1f}" stroke="#e6e9ee" stroke-width="0.9"/>' for a in range(0, 360, 30))
    it.append((sp, 'Spiculé', 'haut risque', CHIP[5]))
    cal = lung + '<circle cx="59" cy="44" r="13" fill="#9aa3ae"/><circle cx="59" cy="44" r="5" fill="#fff"/>'
    it.append((cal, 'Calcification centrale', 'bénin (granulome)', CHIP[1]))
    cy = lung + '<circle cx="59" cy="44" r="16" fill="none" stroke="#e6e9ee" stroke-width="3"/><path d="M48,52 Q56,40 70,48" stroke="#e6e9ee" stroke-width="2" fill="none"/>'
    it.append((cy, 'Kyste atypique', 'paroi épaisse ou cloisons (Lung-RADS)', CHIP[4]))
    save('th01.svg', tiles(it, 4, title='Types de nodules et mesure', note=NOTE + ' · fenêtre parenchymateuse'))

def pe():
    it = []
    a = '<rect x="8" y="8" width="102" height="76" rx="4" fill="#2a2f38"/>'
    it.append((a + '<circle cx="59" cy="44" r="22" fill="#f2f2f2"/><circle cx="59" cy="44" r="10" fill="#6b7480"/>', 'Défect central', '« polo mint » (coupe axiale)', CHIP[5]))
    it.append((a + '<rect x="14" y="32" width="90" height="24" fill="#f2f2f2"/><rect x="14" y="39" width="90" height="10" rx="5" fill="#6b7480"/>', 'Rail de chemin de fer', 'embole aigu en coupe longitudinale', CHIP[5]))
    it.append((a + '<rect x="14" y="30" width="90" height="28" fill="#f2f2f2"/><path d="M40,30 Q60,48 80,30Z" fill="#6b7480"/>', 'Angle aigu', 'embole aigu, vaisseau élargi', CHIP[5]))
    it.append((a + '<rect x="14" y="34" width="90" height="20" fill="#f2f2f2"/><path d="M30,34 L90,34 L84,40 L36,40Z" fill="#6b7480"/><line x1="50" y1="34" x2="60" y2="54" stroke="#6b7480" stroke-width="2"/>', 'Angle obtus, bande', 'séquelle chronique', CHIP[3]))
    rv = a + '<ellipse cx="40" cy="46" rx="26" ry="22" fill="#d9dee5"/><ellipse cx="82" cy="46" rx="16" ry="18" fill="#bfc6cf"/><path d="M62,30 Q70,46 62,62" stroke="#4a5462" stroke-width="1.5" fill="none"/>' + T(40, 49, 'VD', 9, 700) + T(82, 49, 'VG', 9, 700)
    it.append((rv, 'VD/VG ≥ 1,0', 'septum bombant vers le VG', CHIP[4]))
    it.append((a + '<rect x="40" y="12" width="20" height="70" fill="#d9dee5"/><path d="M60,40 L88,30 L88,46 L60,52Z" fill="#f2f2f2"/>' + T(50, 92, '', 7, 400, MUT), 'Reflux cave et sus-hépatique', 'dysfonction du VD', CHIP[4]))
    save('th03.svg', tiles(it, 3, tw=160, th=94, title='Signes à l\'angioscanner', note=NOTE))

# ---------------- Cœur ----------------
def cad():
    W = 520
    s = f'<svg viewBox="0 0 {W} 210" role="img" style="width:100%;height:auto"><title>CAD-RADS</title>' + T(0, 11, 'Échelle de sténose et catégories', 9.5, 700, INK, 'start')
    segs = [(0, 1, '0', G1, DG), (1, 25, '1', G1, DG), (25, 50, '2', '#E3F3D2', '#3D6B12'), (50, 70, '3', Y3, DY), (70, 100, '4A', O4, DO), (100, 101, '5', R5, DR)]
    x0, w = 10, 480
    for a, b, lab_, f, k in segs:
        xa = x0 + a / 101 * w; xb = x0 + b / 101 * w
        s += f'<rect x="{xa:.1f}" y="20" width="{xb-xa:.1f}" height="22" fill="{f}" stroke="#fff"/>' + T((xa + xb) / 2, 35, lab_, 9, 700, k)
    for v in [0, 25, 50, 70, 100]:
        s += T(x0 + v / 101 * w, 54, f'{v} %', 7.5, 400, MUT)
    s += T(10, 70, '4B : tronc commun ≥ 50 % ou tritronculaire ≥ 70 % · 5 : occlusion totale', 7.8, 400, MUT, 'start')
    # HRP icons
    icons = [
        ('Faible densité', '&lt; 30 UH', '<circle cx="45" cy="45" r="26" fill="#f2f2f2" stroke="#4a5462"/><path d="M45,19 A26,26 0 0,1 71,45 L58,45 A13,13 0 0,0 45,32Z" fill="#6b7480"/><circle cx="45" cy="45" r="11" fill="#c9302c" opacity="0.25"/>'),
        ('Remodelage positif', '≥ 10 % du diamètre', '<path d="M5,35 L30,35 Q45,20 60,35 L85,35 M5,55 L30,55 Q45,70 60,55 L85,55" stroke="#4a5462" stroke-width="2" fill="none"/>'),
        ('Calcifications ponctuées', '&lt; 3 mm', '<rect x="5" y="32" width="80" height="26" rx="13" fill="#f2f2f2" stroke="#4a5462"/><circle cx="35" cy="38" r="2.5" fill="#1d2430"/><circle cx="55" cy="52" r="2" fill="#1d2430"/>'),
        ('Signe de l\'anneau', 'napkin-ring', '<circle cx="45" cy="45" r="26" fill="none" stroke="#4a5462" stroke-width="5"/><circle cx="45" cy="45" r="21" fill="#9aa3ae"/><circle cx="45" cy="45" r="8" fill="#f2f2f2"/>'),
    ]
    for i, (a, b, d) in enumerate(icons):
        x = 10 + i * 128
        s += f'<g transform="translate({x},90)"><rect width="118" height="96" rx="6" fill="#fff" stroke="#d5dae1"/><g transform="translate(14,4)">{d}</g>' + T(59, 108, a, 9, 700) + T(59, 118, b, 7.5, 400, MUT) + '</g>'
    s += T(10, 82, 'Plaque à haut risque (modificateur HRP) : au moins 2 signes', 9, 700, INK, 'start')
    return save('cv01.svg', s + '</svg>')

# ---------------- Foie ----------------
def phases(rows, title, note=NOTE, labels=('Sans', 'Artérielle', 'Portale', 'Tardive / PHB')):
    cw, rh = 78, 62
    W = 150 + cw * len(labels)
    H = 22 + rh * len(rows) + 14
    s = f'<svg viewBox="0 0 {W} {H}" role="img" style="width:100%;height:auto"><title>{title}</title>' + T(0, 11, title, 9.5, 700, INK, 'start')
    for j, l in enumerate(labels): s += T(150 + cw * j + cw / 2, 20, l, 8, 600, MUT)
    for i, (name, sub, cells) in enumerate(rows):
        y = 26 + rh * i
        s += T(0, y + 26, name, 9, 700, INK, 'start') + T(0, y + 38, sub, 7.4, 400, MUT, 'start')
        for j, c in enumerate(cells):
            x = 150 + cw * j + cw / 2
            s += f'<rect x="{x-34}" y="{y+2}" width="68" height="54" rx="4" fill="#9aa3ae"/>' + c.replace('CX', str(x)).replace('CY', str(y + 29))
    s += T(0, H - 3, note, 7.2, 400, MUT, 'start')
    return s + '</svg>'

def C(fill, r=17, extra='', stroke='none'):
    return f'<circle cx="CX" cy="CY" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>' + extra

def lirads():
    H, L, I = '#e9edf2', '#5b6573', '#9aa3ae'
    rows = [
        ('APHE non périphérique', 'critère majeur', [C(I), C(H), C(I), C(I)]),
        ('Wash-out + capsule', 'critères majeurs', [C(I), C(H), C(L, stroke='#f2f2f2'), C(L, stroke='#ffffff')]),
        ('APHE en anneau', 'aspect en cible → LR-M', [C(L), C(L, extra='<circle cx="CX" cy="CY" r="17" fill="none" stroke="#e9edf2" stroke-width="4"/>'), C(L, extra='<circle cx="CX" cy="CY" r="17" fill="none" stroke="#c4cad3" stroke-width="3"/>'), C('#c4cad3', extra='<circle cx="CX" cy="CY" r="8" fill="#e9edf2"/>')]),
    ]
    save('fo01.svg', phases(rows, 'Critères majeurs : évolution du signal selon la phase', NOTE + ' · gris = foie ; plus clair = plus rehaussé', ('Sans injection', 'Artérielle tardive', 'Portale', 'Tardive / transitionnelle')))

def ceus():
    W = 520
    s = f'<svg viewBox="0 0 {W} 150" role="img" style="width:100%;height:auto"><title>Chronologie CEUS</title>' + T(0, 11, 'Chronologie du wash-out en CEUS', 9.5, 700, INK, 'start')
    x0, w = 20, 470
    def X(t): return x0 + t / 300 * w
    s += f'<line x1="{x0}" y1="60" x2="{x0+w}" y2="60" stroke="{LINE}" stroke-width="1.2"/>'
    for t in [0, 30, 60, 120, 180, 240, 300]:
        s += f'<line x1="{X(t):.1f}" y1="56" x2="{X(t):.1f}" y2="64" stroke="{LINE}"/>' + T(X(t), 76, f'{t} s' if t < 60 else f'{t//60} min', 7.8, 400, MUT)
    s += f'<rect x="{X(10):.1f}" y="26" width="{X(45)-X(10):.1f}" height="18" rx="3" fill="{O4}"/>' + T((X(10) + X(45)) / 2, 38, 'phase artérielle : APHE', 8, 700, DO)
    s += f'<rect x="{X(0):.1f}" y="88" width="{X(60)-X(0):.1f}" height="18" rx="3" fill="{B}"/>' + T(X(30), 100, 'précoce : LR-M', 8, 700, '#1F4E8C')
    s += f'<rect x="{X(60):.1f}" y="88" width="{X(300)-X(60):.1f}" height="18" rx="3" fill="{R5}"/>' + T((X(60) + X(300)) / 2, 100, 'wash-out tardif (≥ 60 s) et modéré : critère de CHC', 8, 700, DR)
    s += f'<rect x="{X(0):.1f}" y="112" width="{X(120)-X(0):.1f}" height="16" rx="3" fill="none" stroke="#1F4E8C" stroke-dasharray="3 2"/>' + T(X(60), 123, 'wash-out marqué (« vide ») en &lt; 2 min : LR-M', 7.6, 600, '#1F4E8C')
    s += T(0, 145, 'Observer au moins 5 minutes (SonoVue) · ' + NOTE, 7.2, 400, MUT, 'start')
    save('fo02.svg', s + '</svg>')

def focal():
    H, L, I, W_ = '#e9edf2', '#5b6573', '#9aa3ae', '#ffffff'
    hem_a = C(L, extra=''.join(f'<circle cx="CX" cy="CY" r="3.5" fill="{W_}" transform="rotate({a} CX CY) translate(0,-13)"/>' for a in range(0, 360, 60)))
    rows = [
        ('Hémangiome', 'nodulaire périphérique → centripète', [C(L), hem_a, C(H, extra=f'<circle cx="CX" cy="CY" r="7" fill="{L}"/>'), C(H)]),
        ('HNF', 'homogène, cicatrice tardive', [C(I), C(H, extra=f'<path d="M CX CY m-10,0 l20,0 m-10,-10 l0,20" stroke="{L}" stroke-width="2.5"/>'), C(I, extra=f'<path d="M CX CY m-10,0 l20,0 m-10,-10 l0,20" stroke="{L}" stroke-width="2.5"/>'), C(I, extra=f'<path d="M CX CY m-10,0 l20,0 m-10,-10 l0,20" stroke="{H}" stroke-width="2.5"/>')]),
        ('Adénome', 'APHE, hypo en PHB', [C(I), C(H), C(I), C(L)]),
        ('Métastase hypovasculaire', 'anneau périphérique', [C(L), C(L, extra=f'<circle cx="CX" cy="CY" r="16" fill="none" stroke="{H}" stroke-width="3"/>'), C(L, extra=f'<circle cx="CX" cy="CY" r="16" fill="none" stroke="#c4cad3" stroke-width="3"/>'), C(L)]),
    ]
    save('fo03.svg', phases(rows, 'Dynamique de rehaussement des lésions fréquentes', NOTE + ' · PHB = phase hépatobiliaire (gadoxétate)'))

# ---------------- Rein / surrénale ----------------
def bosniak():
    def cyst(extra='', wall=1.2):
        return f'<circle cx="59" cy="46" r="32" fill="#2a2f38" stroke="#e6e9ee" stroke-width="{wall}"/>' + extra
    it = [
        (cyst(), 'I', 'paroi fine ≤ 2 mm, liquide', CHIP[1]),
        (cyst('<line x1="38" y1="30" x2="82" y2="58" stroke="#e6e9ee" stroke-width="1"/><line x1="44" y1="66" x2="74" y2="24" stroke="#e6e9ee" stroke-width="1"/>'), 'II', '1–3 cloisons fines', CHIP[1]),
        (cyst(''.join(f'<line x1="{30+i*12}" y1="22" x2="{36+i*10}" y2="70" stroke="#e6e9ee" stroke-width="1"/>' for i in range(4)), 3), 'IIF', '≥ 4 cloisons ou paroi 3 mm', CHIP[3]),
        (cyst('<path d="M40,26 Q50,46 42,66" stroke="#e6e9ee" stroke-width="4.5" fill="none"/>', 4.5), 'III', 'paroi ou cloison ≥ 4 mm, irrégulière', CHIP[4]),
        (cyst('<path d="M78,30 Q66,44 80,60" fill="#e6e9ee"/>'), 'IV', 'nodule rehaussé', CHIP[5]),
    ]
    save('rs01.svg', tiles(it, 5, tw=100, th=94, gap=5, title='Classes de Bosniak v2019 (après injection)', note=NOTE))

def adrenal():
    W = 520
    s = f'<svg viewBox="0 0 {W} 112" role="img" style="width:100%;height:auto"><title>Densité spontanée</title>' + T(0, 11, 'Densité au scanner sans injection (UH)', 9.5, 700, INK, 'start')
    x0, w = 10, 490
    def X(v): return x0 + (v + 40) / 90 * w
    s += f'<rect x="{X(-40):.1f}" y="22" width="{X(-30)-X(-40):.1f}" height="22" fill="{G1}"/><rect x="{X(-30):.1f}" y="22" width="{X(10)-X(-30):.1f}" height="22" fill="#E3F3D2"/><rect x="{X(10):.1f}" y="22" width="{X(20)-X(10):.1f}" height="22" fill="{Y3}"/><rect x="{X(20):.1f}" y="22" width="{X(50)-X(20):.1f}" height="22" fill="{R5}"/>'
    s += T((X(-40) + X(-30)) / 2, 37, '&lt; −30', 7.5, 700, DG) + T((X(-30) + X(10)) / 2, 37, 'adénome riche en lipides (≤ 10)', 8, 700, '#3D6B12') + T((X(10) + X(20)) / 2, 37, '11–20', 8, 700, DY) + T((X(20) + X(50)) / 2, 37, '&gt; 20 : indéterminé → RCP', 8, 700, DR)
    for v in [-30, 10, 20]:
        s += f'<line x1="{X(v):.1f}" y1="18" x2="{X(v):.1f}" y2="48" stroke="{INK}" stroke-width="1"/>' + T(X(v), 60, str(v), 8, 700)
    s += T(X(-35), 74, 'graisse : myélolipome', 7.5, 400, MUT) + T((X(10) + X(20)) / 2, 74, 'homogène &lt; 4 cm : contrôle', 7.5, 400, MUT)
    s += T(10, 92, 'IRM : chute de signal en opposition de phase = graisse intracellulaire (adénome)', 8, 400, INK, 'start')
    s += T(10, 106, NOTE, 7.2, 400, MUT, 'start')
    save('rs02.svg', s + '</svg>')

# ---------------- Pelvis ----------------
def prostate():
    s = '<svg viewBox="0 0 520 200" role="img" style="width:100%;height:auto"><title>Anatomie zonale de la prostate</title>' + T(0, 11, 'Anatomie zonale (coupe axiale, partie moyenne)', 9.5, 700, INK, 'start')
    cx, cy = 130, 105
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="95" ry="70" fill="#F6C1C1"/>'  # PZ
    s += f'<ellipse cx="{cx}" cy="{cy-14}" rx="64" ry="44" fill="#FCEFC7"/>'  # TZ
    s += f'<path d="M{cx-60},{cy-42} Q{cx},{cy-90} {cx+60},{cy-42} Q{cx},{cy-60} {cx-60},{cy-42}Z" fill="#cfd5dd"/>'  # AFS
    s += f'<circle cx="{cx}" cy="{cy-10}" r="6" fill="#fff" stroke="{LINE}"/>'
    s += f'<path d="M{cx-60},{cy+80} Q{cx},{cy+60} {cx+60},{cy+80}" stroke="#9aa3ae" stroke-width="8" fill="none"/>'
    s += T(cx, cy + 50, 'ZP', 11, 700, DR) + T(cx - 28, cy - 8, 'ZT', 11, 700, DY) + T(cx + 28, cy - 8, 'ZT', 11, 700, DY) + T(cx, cy - 58, 'SFMA', 8.5, 700, '#3A4250') + T(cx, cy + 2, 'urètre', 7, 400, MUT) + T(cx, cy + 94, 'rectum', 7.5, 400, MUT) + T(cx, 22, 'avant', 7.5, 400, MUT)
    x = 270
    rows = [('#F6C1C1', DR, 'Zone périphérique (ZP)', '≈ 70 % des cancers · score par la DIFFUSION'), ('#FCEFC7', DY, 'Zone de transition (ZT)', 'hypertrophie bénigne · score par le T2'), ('#cfd5dd', '#3A4250', 'Stroma fibromusculaire antérieur', 'normalement hypo T2 et ADC bas'), ('#ffffff', INK, 'Zone centrale (base)', 'hypo T2 symétrique : piège')]
    for i, (f, k, a, b) in enumerate(rows):
        y = 40 + i * 36
        s += f'<rect x="{x}" y="{y}" width="14" height="14" rx="3" fill="{f}" stroke="{LINE}" stroke-width="0.5"/>' + T(x + 22, y + 10, a, 9, 700, INK, 'start') + T(x + 22, y + 22, b, 7.6, 400, MUT, 'start')
    s += T(0, 196, NOTE + ' · SFMA = stroma fibromusculaire antérieur', 7.2, 400, MUT, 'start')
    save('pe01.svg', s + '</svg>')

def orads():
    def ov(extra):
        return '<rect x="8" y="8" width="102" height="76" rx="4" fill="#2a2f38"/>' + extra
    E = '#111318'; Wt = '#d9dee5'
    it = [
        (ov(f'<ellipse cx="59" cy="46" rx="30" ry="24" fill="{E}" stroke="{Wt}" stroke-width="1"/>'), 'Kyste simple', 'anéchogène, paroi fine', CHIP[1]),
        (ov(f'<ellipse cx="59" cy="46" rx="30" ry="24" fill="#4b525e" stroke="{Wt}"/>'), 'Endométriome', 'échos homogènes', CHIP[1]),
        (ov(f'<ellipse cx="59" cy="46" rx="30" ry="24" fill="{E}" stroke="{Wt}"/><path d="M36,40 Q48,52 40,62 M52,28 Q62,46 56,66 M70,30 Q66,52 80,58" stroke="#6b7480" stroke-width="0.8" fill="none"/>'), 'Kyste hémorragique', 'réticulaire, sans flux', CHIP[1]),
        (ov(f'<ellipse cx="59" cy="46" rx="30" ry="24" fill="#3b4250" stroke="{Wt}"/><circle cx="52" cy="42" r="10" fill="#e9edf2"/><rect x="58" y="44" width="20" height="24" fill="#15181e"/>'), 'Kyste dermoïde', 'hyperéchogène + cône d\'ombre', CHIP[1]),
        (ov(f'<ellipse cx="59" cy="46" rx="32" ry="26" fill="{E}" stroke="{Wt}"/><line x1="46" y1="22" x2="50" y2="70" stroke="{Wt}"/><line x1="70" y1="22" x2="66" y2="70" stroke="{Wt}"/>'), 'Multiloculaire lisse', 'O-RADS 3 (&lt; 10 cm, CS 1–3)', CHIP[3]),
        (ov(f'<ellipse cx="59" cy="46" rx="30" ry="24" fill="{E}" stroke="{Wt}"/><path d="M40,58 q4,-12 8,0Z" fill="{Wt}"/>'), '1–3 végétations', 'O-RADS 4', CHIP[4]),
        (ov(f'<ellipse cx="59" cy="46" rx="30" ry="24" fill="{E}" stroke="{Wt}"/>' + ''.join(f'<path d="M{x},{y} q4,-11 8,0Z" fill="{Wt}"/>' for x, y in [(38, 58), (54, 68), (70, 60), (60, 26)])), '≥ 4 végétations', 'O-RADS 5', CHIP[5]),
        (ov(f'<path d="M34,40 C30,20 60,18 70,26 C90,22 92,52 82,60 C76,74 46,74 40,64 C26,60 30,48 34,40Z" fill="#6b7480"/><circle cx="56" cy="44" r="3" fill="#c9302c"/><circle cx="68" cy="52" r="3" fill="#c9302c"/><circle cx="48" cy="56" r="2.5" fill="#c9302c"/>'), 'Solide irrégulier', 'O-RADS 5 (tout CS)', CHIP[5]),
    ]
    save('pe02.svg', tiles(it, 4, title='Lésions types en échographie et score O-RADS', note=NOTE + ' · CS = score couleur (rouge = flux)'))

def endo():
    s = '<svg viewBox="0 0 520 210" role="img" style="width:100%;height:auto"><title>Compartiments dPEI</title>' + T(0, 11, 'Compartiments du pelvis (dPEI) · vue schématique', 9.5, 700, INK, 'start')
    x0, y0, cw, rh = 20, 24, 96, 46
    cols = ['Latéral droit', 'Médian', 'Latéral gauche']
    rowsN = [('Antérieur', 'vessie, cul-de-sac vésico-utérin, uretère distal', '#DCE8F8'), ('Central', 'utérus, col, vagin, torus, LUS proximaux', '#E5DCF7'), ('Postérieur', 'rectum, charnière recto-sigmoïdienne', '#FBD9BD')]
    for j, c in enumerate(cols): s += T(x0 + cw * j + cw / 2, y0 - 2, c, 8, 600, MUT)
    for i, (n, d, f) in enumerate(rowsN):
        for j in range(3):
            lat = j != 1
            s += f'<rect x="{x0+cw*j}" y="{y0+4+rh*i}" width="{cw-4}" height="{rh-4}" rx="4" fill="{f if not lat else "#f1f3f6"}" stroke="#aab2bd" stroke-width="0.6"/>'
            s += T(x0 + cw * j + cw / 2 - 2, y0 + 4 + rh * i + 22, n if not lat else 'paramètre / LUS distal' if i == 1 else 'latéral', 8.5 if not lat else 7.3, 700 if not lat else 400, INK if not lat else MUT)
        s += T(x0 + 3 * cw + 8, y0 + 4 + rh * i + 18, n, 9, 700, INK, 'start') + T(x0 + 3 * cw + 8, y0 + 4 + rh * i + 30, d, 7.5, 400, MUT, 'start')
    s += f'<rect x="{x0}" y="{y0+4+rh*3}" width="{cw*3-4}" height="22" rx="4" fill="#f1f3f6" stroke="#aab2bd" stroke-dasharray="3 2" stroke-width="0.6"/>' + T(x0 + cw * 1.5, y0 + 4 + rh * 3 + 15, 'Extra-pelvien (côlon, intestin grêle, appendice, diaphragme)', 8, 600, INK)
    s += T(0, 206, 'Sévérité : ≤ 2 compartiments légère · 3–4 modérée · ≥ 5 sévère · LUS = ligaments utéro-sacrés · ' + NOTE, 7.2, 400, MUT, 'start')
    save('pe03.svg', s + '</svg>')

# ---------------- Digestif ----------------
def rectum():
    s = '<svg viewBox="0 0 520 254" role="img" style="width:100%;height:auto"><title>Stade T du cancer du rectum</title>' + T(0, 11, 'Paroi rectale, mésorectum et stade T (coupe perpendiculaire)', 9.5, 700, INK, 'start')
    x0, y = 20, 30
    layers = [('Lumière', 30, '#2a2f38', '#fff'), ('Muqueuse / sous-muqueuse', 22, '#e9edf2', INK), ('Musculeuse propre', 22, '#5b6573', '#fff'), ('Graisse mésorectale', 92, '#FCEFC7', DY)]
    yy = y
    for n, h, f, k in layers:
        s += f'<rect x="{x0}" y="{yy}" width="480" height="{h}" fill="{f}"/>' + T(x0 + 6, yy + h / 2 + 3, n, 8, 600, k, 'start')
        yy += h
    s += f'<line x1="{x0}" y1="{yy}" x2="{x0+480}" y2="{yy}" stroke="#7a3b8f" stroke-width="2.5"/>' + T(x0 + 6, yy + 12, 'Fascia mésorectal (MRF) : envahi si marge ≤ 1 mm', 8, 700, '#7a3b8f', 'start')
    mp_bottom = y + 30 + 22 + 22
    tum = [('T1', 30 + 22, '#c2410c'), ('T2', 30 + 44, '#c2410c'), ('T3a', 74 + 1, '#c2410c'), ('T3b', 74 + 5 * 3, '#c2410c'), ('T3c', 74 + 15 * 3, '#c2410c'), ('T3d', 74 + 26 * 3, '#c2410c')]
    for i, (n, d, f) in enumerate(tum):
        x = x0 + 170 + i * 52
        s += f'<path d="M{x},{y+30} L{x+34},{y+30} L{x+30},{y+d} Q{x+17},{y+d+6} {x+4},{y+d}Z" fill="{f}" opacity="0.85"/>' + T(x + 17, y + 22, n, 8.5, 700, '#fff')
    s += T(x0 + 170 + 4 * 52 + 17, y + 30 + 22 + 22 + 92 - 10, '', 7, 400, MUT)
    s += T(x0, 224, 'T3 : a &lt; 1 mm · b 1–5 mm · c 5–15 mm · d &gt; 15 mm au-delà de la musculeuse', 7.8, 400, INK, 'start')
    s += T(x0, 236, 'T4a : péritoine viscéral · T4b : organe voisin, sphincter externe, releveurs', 7.8, 400, INK, 'start')
    s += T(x0, 249, NOTE, 7.2, 400, MUT, 'start')
    save('di01.svg', s + '</svg>')

def divert():
    def col(extra):
        return '<rect x="8" y="8" width="102" height="76" rx="4" fill="#3b4250"/><path d="M14,50 Q40,30 60,44 Q80,58 104,40" stroke="#c9cfd8" stroke-width="12" fill="none"/>' + extra
    it = [
        (col('<path d="M14,50 Q40,30 60,44 Q80,58 104,40" stroke="#e9edf2" stroke-width="4" fill="none"/><circle cx="46" cy="30" r="4" fill="#e9edf2"/><circle cx="76" cy="62" r="4" fill="#e9edf2"/>'), '0', 'épaississement, densification', CHIP[1]),
        (col('<circle cx="56" cy="30" r="2.5" fill="#000"/><circle cx="64" cy="28" r="2" fill="#000"/>'), '1A', 'bulles péricoliques', CHIP[2]),
        (col('<ellipse cx="60" cy="68" rx="10" ry="7" fill="#7a8492" stroke="#e9edf2"/>'), '1B', 'abcès ≤ 4 cm', CHIP[3]),
        (col('<ellipse cx="62" cy="68" rx="22" ry="12" fill="#7a8492" stroke="#e9edf2"/>'), '2A', 'abcès &gt; 4 cm → drainage', CHIP[4]),
        (col('<circle cx="20" cy="18" r="3" fill="#000"/><circle cx="96" cy="18" r="2.5" fill="#000"/>'), '2B', 'air à distance', CHIP[4]),
        (col('<path d="M10,78 Q59,66 108,78 L108,84 L10,84Z" fill="#7a8492"/><path d="M10,14 Q30,22 20,30" stroke="#7a8492" stroke-width="5" fill="none"/>'), '3', 'liquide diffus', CHIP[5]),
        (col('<path d="M10,78 Q59,66 108,78 L108,84 L10,84Z" fill="#7a8492"/><path d="M40,12 L80,12 L76,18 L44,18Z" fill="#000"/>'), '4', 'liquide + air libre', CHIP[5]),
    ]
    save('di02.svg', tiles(it, 4, tw=122, th=90, gap=10, title='Stades scanographiques WSES', note=NOTE + ' · noir = air'))

def pancreas():
    def pan(extra):
        return '<rect x="6" y="8" width="150" height="76" rx="4" fill="#fff"/><path d="M14,58 Q40,30 90,40 Q130,46 150,30 L150,46 Q130,62 90,56 Q44,48 22,70Z" fill="#f1e6c8" stroke="#b5850b" stroke-width="0.8"/>' + extra
    it = [
        (pan('<path d="M22,62 Q48,42 90,48 Q128,54 148,38" stroke="#b5850b" stroke-width="1.5" fill="none"/><circle cx="60" cy="40" r="7" fill="#dbeafe" stroke="#1f5fa8"/><circle cx="104" cy="58" r="5" fill="#dbeafe" stroke="#1f5fa8"/><line x1="60" y1="47" x2="62" y2="46" stroke="#1f5fa8"/>'), 'Canaux secondaires', 'kystes communiquant avec le CPP', CHIP['b']),
        (pan('<path d="M22,62 Q48,42 90,48 Q128,54 148,38" stroke="#1f5fa8" stroke-width="7" fill="none" opacity="0.6"/>'), 'Canal principal', 'CPP &gt; 5 mm · ≥ 10 mm = haut risque', CHIP[4]),
        (pan('<circle cx="80" cy="44" r="16" fill="#dbeafe" stroke="#1f5fa8"/><path d="M70,54 q6,-12 12,0Z" fill="#b5850b"/>'), 'Nodule mural', '≥ 5 mm rehaussé = haut risque', CHIP[5]),
    ]
    save('pa01.svg', tiles(it, 3, tw=162, th=92, title='Types de TIPMP et signe de haut risque', note=NOTE + ' · CPP = canal pancréatique principal'))

# ---------------- Ostéo ----------------
def bone():
    def b(extra):
        return '<rect x="8" y="8" width="102" height="76" rx="4" fill="#2a2f38"/><rect x="34" y="8" width="50" height="76" fill="#9aa3ae"/><rect x="38" y="8" width="42" height="76" fill="#c4cad3"/>' + extra
    it = [
        (b('<ellipse cx="59" cy="46" rx="12" ry="18" fill="#3b4250" stroke="#ffffff" stroke-width="3"/>'), 'IA', 'géographique, bord scléreux · 1 pt', CHIP[1]),
        (b('<ellipse cx="59" cy="46" rx="12" ry="18" fill="#3b4250" stroke="#3b4250"/>'), 'IB', 'bien limitée, sans sclérose · 3 pts', CHIP[3]),
        (b('<path d="M48,30 Q60,24 70,32 Q74,46 68,62 Q56,70 48,60 Q44,46 48,30Z" fill="#3b4250"/><path d="M48,30 l-4,-4 M70,62 l5,4 M45,48 l-5,1" stroke="#3b4250" stroke-width="2"/>'), 'II', 'géographique mal limitée · 5 pts', CHIP[4]),
        (b(''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#3b4250"/>' for x, y, r in [(46, 24, 2), (54, 30, 2.5), (64, 26, 1.8), (50, 40, 2.2), (62, 44, 2.6), (70, 38, 1.6), (46, 56, 2), (58, 60, 2.4), (68, 66, 1.8), (54, 72, 2)])), 'III', 'mitée ou perméative · 7 pts', CHIP[5]),
        (b('<line x1="34" y1="20" x2="34" y2="72" stroke="#e9edf2" stroke-width="2.5"/><line x1="30" y1="20" x2="30" y2="72" stroke="#e9edf2" stroke-width="1.2"/>'), 'Périostée solide', 'non agressive · 2 pts', CHIP[3]),
        (b(''.join(f'<line x1="{34-i*3}" y1="20" x2="{34-i*3}" y2="72" stroke="#e9edf2" stroke-width="0.9"/>' for i in range(1, 5))), 'Lamellée', '« bulbe d\'oignon » · 4 pts', CHIP[5]),
        (b(''.join(f'<line x1="34" y1="{y}" x2="16" y2="{y-2}" stroke="#e9edf2" stroke-width="0.9"/>' for y in range(22, 72, 5))), 'Spiculée', '« feu d\'herbe » · 4 pts', CHIP[5]),
        (b('<path d="M34,22 L22,30 L34,30" stroke="#e9edf2" stroke-width="1.5" fill="none"/><path d="M34,72 L22,64 L34,64" stroke="#e9edf2" stroke-width="1.5" fill="none"/><rect x="18" y="34" width="16" height="26" fill="#6b7480"/>'), 'Éperon de Codman', 'agressive · 4 pts', CHIP[5]),
    ]
    save('os01.svg', tiles(it, 4, title='Marges (Lodwick) et réactions périostées', note=NOTE + ' · os long en radiographie'))

def salter():
    def phys(extra):
        return ('<rect x="8" y="8" width="102" height="76" rx="4" fill="#fff"/>'
                '<path d="M30,10 L88,10 L84,36 L34,36Z" fill="#dfe4ea" stroke="#4a5462"/>'
                '<rect x="32" y="37" width="54" height="5" fill="#9fb6cf"/>'
                '<path d="M34,43 L84,43 L76,84 L42,84Z" fill="#dfe4ea" stroke="#4a5462"/>' + extra)
    R = '#c2410c'
    it = [
        (phys(f'<line x1="32" y1="39.5" x2="86" y2="39.5" stroke="{R}" stroke-width="2.5"/>'), 'I · S', 'physe seule', CHIP[1]),
        (phys(f'<path d="M32,39.5 L66,39.5 L80,60" stroke="{R}" stroke-width="2.5" fill="none"/>'), 'II · A', 'physe + métaphyse (75 %)', CHIP[1]),
        (phys(f'<path d="M86,39.5 L60,39.5 L56,10" stroke="{R}" stroke-width="2.5" fill="none"/>'), 'III · L', 'physe + épiphyse', CHIP[3]),
        (phys(f'<path d="M54,10 L62,84" stroke="{R}" stroke-width="2.5" fill="none"/>'), 'IV · T', 'traverse les trois', CHIP[4]),
        (phys(f'<rect x="32" y="37" width="54" height="5" fill="{R}"/><path d="M59,2 L59,8 M55,5 L59,9 L63,5" stroke="{INK}" stroke-width="1.2" fill="none"/>'), 'V · R', 'écrasement de la physe', CHIP[5]),
    ]
    save('os02.svg', tiles(it, 5, tw=96, th=92, gap=8, title='Salter-Harris (moyen mnémotechnique SALTR)', note=NOTE + ' · bleu = cartilage de croissance, rouge = trait'))

def disc():
    def ax(extra):
        return '<rect x="8" y="8" width="102" height="76" rx="4" fill="#fff"/><ellipse cx="59" cy="40" rx="34" ry="22" fill="#dfe4ea" stroke="#4a5462"/>' + extra
    D = '#c2410c'
    it = [
        (ax(f'<path d="M25,46 Q59,72 93,46" stroke="{D}" stroke-width="5" fill="none"/>'), 'Bombement', '&gt; 25 % de la circonférence', CHIP[0]),
        (ax(f'<path d="M48,60 Q59,72 70,60Z" fill="{D}"/>'), 'Protrusion', 'base &gt; débord', CHIP[3]),
        (ax(f'<path d="M54,60 L54,64 Q46,80 59,80 Q72,80 64,64 L64,60Z" fill="{D}"/>'), 'Extrusion', 'débord &gt; base (collet)', CHIP[4]),
        (ax(f'<ellipse cx="62" cy="76" rx="8" ry="5" fill="{D}"/>'), 'Séquestration', 'fragment libre', CHIP[5]),
    ]
    zones = ('<rect x="8" y="8" width="102" height="76" rx="4" fill="#fff"/><ellipse cx="59" cy="28" rx="30" ry="16" fill="#dfe4ea" stroke="#4a5462"/>'
             '<rect x="49" y="46" width="20" height="16" fill="#f1e6c8"/><rect x="34" y="46" width="15" height="16" fill="#dbeafe"/><rect x="69" y="46" width="15" height="16" fill="#dbeafe"/>'
             '<rect x="22" y="46" width="12" height="16" fill="#E5DCF7"/><rect x="84" y="46" width="12" height="16" fill="#E5DCF7"/>'
             + T(59, 57, 'C', 8, 700) + T(41, 57, 'SA', 6.5, 700) + T(77, 57, 'SA', 6.5, 700) + T(28, 57, 'F', 7, 700) + T(90, 57, 'F', 7, 700) + T(59, 76, 'C central · SA subarticulaire · F foraminal', 6.4, 400, MUT))
    it.append((zones, 'Zones axiales', 'extraforaminal au-delà', CHIP['b']))
    save('os03.svg', tiles(it, 5, tw=96, th=92, gap=8, title='Types de hernie discale (coupe axiale) et zones', note=NOTE))

def nodes():
    def n(extra):
        return '<rect x="8" y="8" width="102" height="76" rx="4" fill="#3b4250"/>' + extra
    L = '#c4cad3'
    it = [
        (n(f'<path d="M34,46 C34,26 84,26 84,46 C84,66 34,66 34,46Z" fill="{L}"/><path d="M76,40 Q66,46 76,52Z" fill="#3b4250"/><path d="M84,46 L76,46" stroke="#3b4250" stroke-width="3"/>'), 'Hile graisseux', 'réniforme · 0 point', CHIP[1]),
        (n(f'<circle cx="59" cy="46" r="22" fill="{L}"/>'), 'Sphérique', 'sans hile · 1 point', CHIP[3]),
        (n(f'<circle cx="59" cy="46" r="22" fill="{L}"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="#8f98a5"/>' for x, y in [(50, 38), (66, 50), (56, 56), (68, 36)])), 'Hétérogène', '1 point', CHIP[3]),
        (n(f'<circle cx="59" cy="46" r="22" fill="{L}"/><ellipse cx="62" cy="44" rx="8" ry="6" fill="#4b525e"/>'), 'Nécrose focale', '2 points', CHIP[4]),
        (n(f'<circle cx="59" cy="46" r="22" fill="none" stroke="{L}" stroke-width="5"/><circle cx="59" cy="46" r="18" fill="#4b525e"/>'), 'Nécrose étendue', '3 points', CHIP[5]),
        (n(f'<path d="M38,44 L44,30 L56,34 L64,24 L72,36 L84,38 L78,50 L84,62 L68,64 L60,72 L50,62 L36,58Z" fill="{L}"/>'), 'Contours irréguliers', '1 point', CHIP[4]),
    ]
    save('tr03.svg', tiles(it, 3, tw=166, th=92, gap=10, title='Configuration ganglionnaire (Node-RADS)', note=NOTE))

def dose():
    s = '<svg viewBox="0 0 520 150" role="img" style="width:100%;height:auto"><title>Doses fœtales</title>' + T(0, 11, 'Dose fœtale selon l\'examen (échelle logarithmique, mGy)', 9.5, 700, INK, 'start')
    x0, w = 20, 480
    def X(v): return x0 + (math.log10(v) + 3) / 5.3 * w
    s += f'<rect x="{X(0.001):.1f}" y="24" width="{X(50)-X(0.001):.1f}" height="16" fill="{G1}"/><rect x="{X(50):.1f}" y="24" width="{X(100)-X(50):.1f}" height="16" fill="{Y3}"/><rect x="{X(100):.1f}" y="24" width="{X(200)-X(100):.1f}" height="16" fill="{R5}"/>'
    s += T((X(0.001) + X(50)) / 2, 35, 'aucun effet déterministe démontré', 8, 700, DG) + T((X(50) + X(100)) / 2, 35, '50–100', 7.5, 700, DY) + T((X(100) + X(200)) / 2, 35, '&gt; 100', 7.5, 700, DR)
    for v, l in [(0.001, '0,001'), (0.01, '0,01'), (0.1, '0,1'), (1, '1'), (10, '10'), (100, '100')]:
        s += f'<line x1="{X(v):.1f}" y1="42" x2="{X(v):.1f}" y2="48" stroke="{LINE}"/>' + T(X(v), 58, l, 7.5, 400, MUT)
    ex = [(0.005, 0.01, 'Radio thorax'), (0.001, 0.01, 'Scanner tête'), (0.01, 0.66, 'Angioscanner thoracique'), (0.1, 3, 'Radio abdomen'), (10, 50, 'Scanner abdomen-pelvis')]
    for i, (a, b, l) in enumerate(ex):
        y = 68 + i * 14
        s += f'<rect x="{X(a):.1f}" y="{y}" width="{max(X(b)-X(a),3):.1f}" height="8" rx="2" fill="#4a5462"/>' + T(X(b) + 6, y + 7, l, 7.8, 600, INK, 'start')
    s += T(0, 146, NOTE + ' · ordres de grandeur', 7.2, 400, MUT, 'start')
    save('tr02.svg', s + '</svg>')

def appendix():
    def bg(extra):
        return '<rect x="8" y="8" width="102" height="76" rx="4" fill="#3b4250"/><ellipse cx="34" cy="34" rx="22" ry="18" fill="#9aa3af"/>' + extra
    it = [
        (bg('<path d="M44,46 Q60,60 86,66" stroke="#c9cfd8" stroke-width="5" fill="none" stroke-linecap="round"/>') + T(80, 30, '≤ 6 mm', 7.5, 600, '#e9edf2'), 'Normale', 'air ou contenu, paroi fine', CHIP[1]),
        (bg('<path d="M44,46 Q60,60 86,66" stroke="#e9edf2" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M44,46 Q60,60 86,66" stroke="#6b7480" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M50,64 l6,-4 M64,72 l6,-4 M74,56 l6,-4 M58,50 l6,-4" stroke="#c9cfd8" stroke-width="1"/>') + T(84, 30, '&gt; 6 mm', 7.5, 600, '#e9edf2'), 'Non compliquée', 'distension, densification', CHIP[3]),
        (bg('<path d="M44,46 Q60,60 86,66" stroke="#e9edf2" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M44,46 Q60,60 86,66" stroke="#6b7480" stroke-width="6" fill="none" stroke-linecap="round"/><circle cx="52" cy="52" r="4" fill="#fff"/>'), 'Stercolithe', 'facteur de risque, non suffisant', CHIP['b']),
        (bg('<path d="M44,46 Q60,60 70,62" stroke="#e9edf2" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M78,64 Q82,65 86,66" stroke="#e9edf2" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="76" cy="54" r="2.5" fill="#000"/><circle cx="84" cy="50" r="2" fill="#000"/>'), 'Perforation', 'défect pariétal, air extraluminal', CHIP[5]),
        (bg('<path d="M44,46 Q56,56 64,60" stroke="#e9edf2" stroke-width="10" fill="none" stroke-linecap="round"/><ellipse cx="84" cy="64" rx="18" ry="12" fill="#7a8492" stroke="#e9edf2" stroke-width="1.6"/><path d="M76,58 h14" stroke="#000" stroke-width="3"/>'), 'Abcès', 'collection à paroi rehaussée', CHIP[5]),
        (bg('<path d="M10,80 Q59,66 108,80 L108,84 L10,84Z" fill="#7a8492"/><path d="M44,46 Q60,60 86,66" stroke="#e9edf2" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M60,14 h30 l-4,5 h-22z" fill="#000"/>'), 'Péritonite', 'liquide diffus ± pneumopéritoine', CHIP[5]),
    ]
    save('di03.svg', tiles(it, 6, tw=118, th=92, gap=8, title='Appendice au scanner : du normal au compliqué', note=NOTE + ' · gris clair = paroi rehaussée, noir = air'))

def sbo():
    def bg(extra):
        return '<rect x="8" y="8" width="102" height="76" rx="4" fill="#3b4250"/>' + extra
    loop = lambda x, y, r: f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9aa3af" stroke="#e9edf2" stroke-width="1.4"/>'
    it = [
        (bg(loop(30, 30, 11) + loop(56, 28, 11) + loop(40, 56, 11) + '<path d="M66,56 Q80,58 94,60" stroke="#c9cfd8" stroke-width="3" fill="none"/>' + '<path d="M56,52 L66,56" stroke="#e9edf2" stroke-width="5"/>') + T(80, 74, 'grêle plat', 7, 400, '#e9edf2'), 'Zone de transition', 'grêle &gt; 2,5 cm en amont', CHIP[3]),
        (bg(loop(40, 44, 20) + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="#000"/>' for x, y in [(32, 38), (44, 34), (48, 50), (36, 52), (40, 44), (28, 46)])), 'Signe des fèces', 'stase, oriente la transition', CHIP['b']),
        (bg('<path d="M30,70 Q20,20 59,20 Q98,20 88,70" stroke="#e9edf2" stroke-width="14" fill="none"/><path d="M30,70 Q20,20 59,20 Q98,20 88,70" stroke="#9aa3af" stroke-width="10" fill="none"/><path d="M28,74 l6,-6 M90,74 l-6,-6" stroke="#fff" stroke-width="2"/>'), 'Anse fermée', 'en U ou en C, double bec', CHIP[5]),
        (bg('<circle cx="59" cy="46" r="20" fill="none" stroke="#c9cfd8" stroke-width="1.5"/><path d="M59,46 m-14,0 a14,14 0 1,1 14,14 a9,9 0 1,1 -9,-9 a4,4 0 1,1 4,4" fill="none" stroke="#e9edf2" stroke-width="2.4"/>'), 'Tourbillon', 'mésentère et vaisseaux enroulés', CHIP[5]),
        (bg(loop(40, 40, 16).replace('#e9edf2', '#5b6370') + '<path d="M70,30 Q90,40 70,60" fill="none" stroke="#7a8492" stroke-width="6"/>' + '<path d="M10,80 Q59,70 108,80 L108,84 L10,84Z" fill="#7a8492"/>'), 'Ischémie', 'paroi hypo-rehaussée, liquide', CHIP[5]),
        (bg(loop(44, 42, 18) + ''.join(f'<circle cx="{44+16*math.cos(a/6*math.pi):.1f}" cy="{42+16*math.sin(a/6*math.pi):.1f}" r="1.6" fill="#000"/>' for a in range(12)) + '<path d="M80,20 l4,12 l6,-8 l2,14" stroke="#000" stroke-width="2" fill="none"/>'), 'Pneumatose', '± aéroportie : nécrose', CHIP[5]),
    ]
    save('di04.svg', tiles(it, 6, tw=118, th=92, gap=8, title='Occlusion du grêle : signes à chercher au scanner', note=NOTE + ' · gris = anses, noir = air'))

if __name__ == '__main__':
    for f in [sep, trauma, thyroid, breast, nodules, pe, cad, lirads, ceus, focal, bosniak, adrenal, prostate, orads, endo, rectum, divert, pancreas, bone, salter, disc, nodes, dose, appendix, sbo]:
        f()
    print('ok')
