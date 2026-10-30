"""Schémas des fiches de mesures orthopédiques (OS-04 à OS-07). Lancer : python3 src/gen/ortho.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import T, tiles, save, CHIP, NOTE, INK, MUT, LINE

BONE = '#dfe4ea'; RED = '#c2410c'; BLUE = '#1f4e8c'


def bone(d, extra=''):
    return f'<path d="{d}" fill="{BONE}" stroke="{LINE}" stroke-width="0.8" {extra}/>'


def ln(x1, y1, x2, y2, c=RED, w=1.4, dash=False):
    da = ' stroke-dasharray="3 2"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{da} stroke-linecap="round"/>'


def dot(x, y, r=2.2, c=RED):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'


def circ(x, y, r, fill=BONE):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{LINE}" stroke-width="0.8"/>'


def arc(cx, cy, r, a1, a2, c=RED):
    """arc de a1 à a2 (degrés, 0 = vers la droite, sens horaire écran)"""
    x1 = cx + r * math.cos(math.radians(a1)); y1 = cy + r * math.sin(math.radians(a1))
    x2 = cx + r * math.cos(math.radians(a2)); y2 = cy + r * math.sin(math.radians(a2))
    large = 1 if abs(a2 - a1) > 180 else 0
    sweep = 1 if a2 > a1 else 0
    return f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {large} {sweep} {x2:.1f},{y2:.1f}" fill="none" stroke="{c}" stroke-width="1"/>'


def lab(x, y, s, c=RED, size=8, w=700, anchor='middle'):
    return T(x, y, s, size, w, c, anchor)


def arrow2(x1, y1, x2, y2, c=BLUE):
    """double flèche de cote"""
    a = math.atan2(y2 - y1, x2 - x1); h = 3
    def head(x, y, ang):
        return f'<path d="M{x:.1f},{y:.1f} L{x + h * math.cos(ang + 2.6):.1f},{y + h * math.sin(ang + 2.6):.1f} L{x + h * math.cos(ang - 2.6):.1f},{y + h * math.sin(ang - 2.6):.1f}Z" fill="{c}"/>'
    return ln(x1, y1, x2, y2, c, 1) + head(x2, y2, a) + head(x1, y1, a + math.pi)


# ---------------- OS-04 Rachis ----------------
def rachis():
    W, H = 166, 100
    it = []
    # 1. Cobb
    s = ''
    verts = []
    for i in range(9):
        y = 12 + i * 9.5
        x = 70 + 16 * math.sin(math.pi * i / 8)
        ang = 20 * math.cos(math.pi * i / 8)  # inclinaison des plateaux
        verts.append((x, y, ang))
        s += f'<rect x="{x - 9:.1f}" y="{y - 3.6:.1f}" width="18" height="7.2" rx="1.5" fill="{BONE}" stroke="{LINE}" stroke-width="0.7" transform="rotate({-ang:.1f} {x:.1f} {y:.1f})"/>'
    # limites : vertèbres 1 et 7 (les plus inclinées dans la courbure)
    for (x, y, ang), side in ((verts[1], -1), (verts[7], 1)):
        a = math.radians(-ang)
        yy = y + side * 3.6
        s += ln(x - 13 * math.cos(a), yy - 13 * math.sin(a), x + 50 * math.cos(a), yy + 50 * math.sin(a))
    s += lab(140, 54, 'Cobb', RED, 8.5) + T(140, 64, 'angle entre', 6.8, 400, MUT) + T(140, 72, 'les 2 lignes', 6.8, 400, MUT)
    it.append((s, 'Angle de Cobb', 'plateaux des vertèbres limites', CHIP[3]))
    # 2. Paramètres pelviens (vue de profil, avant à droite)
    ss, pt = 40, 13
    M = (62, 30)
    u = (math.cos(math.radians(ss)), math.sin(math.radians(ss)))
    n = (-u[1], u[0])
    d = (math.sin(math.radians(pt)), math.cos(math.radians(pt)))
    Hh = (M[0] + 56 * d[0], M[1] + 56 * d[1])
    Pp = (M[0] - 15 * u[0], M[1] - 15 * u[1]); Pa = (M[0] + 15 * u[0], M[1] + 15 * u[1])
    sac = [Pp, Pa, (Pa[0] + 30 * n[0], Pa[1] + 30 * n[1]), (Pp[0] + 22 * n[0] - 4, Pp[1] + 22 * n[1])]
    s = bone('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in sac) + 'Z') + circ(Hh[0], Hh[1], 9)
    s += ln(Pp[0], Pp[1], Pa[0], Pa[1], INK, 1.8)
    s += ln(Pa[0], Pa[1], Pa[0] + 34, Pa[1], BLUE, 1, True) + arc(Pa[0], Pa[1], 12, 0 - 180 + 180, ss, BLUE)
    s += ln(M[0], M[1], M[0] + 40 * n[0], M[1] + 40 * n[1], RED, 1, True)
    s += ln(M[0], M[1], Hh[0], Hh[1], RED, 1.4) + dot(M[0], M[1], 1.8) + dot(Hh[0], Hh[1], 1.8)
    s += ln(Hh[0], Hh[1], Hh[0], Hh[1] - 34, BLUE, 1, True)
    s += lab(Pa[0] + 22, Pa[1] - 3, 'SS', BLUE, 7.5) + lab(M[0] + 1, M[1] + 30, 'PI', RED, 7.5) + lab(Hh[0] + 9, Hh[1] - 26, 'PT', BLUE, 7.5)
    s += T(138, 60, 'PI = PT + SS', 7.6, 700, INK) + T(138, 71, 'PI 55° ± 10°', 6.8, 400, MUT)
    it.append((s, 'Paramètres pelviens', 'incidence, version, pente', CHIP['b']))
    # 3. SVA
    pts = [(96, 10), (86, 26), (82, 44), (90, 62), (80, 80)]
    s = f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{BONE}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{LINE}" stroke-width="0.7" stroke-dasharray="2 2"/>'
    s += bone('M70,78 L90,78 L84,96 L74,96Z') + dot(96, 10, 2.4, INK) + dot(72, 79, 2.2, INK)
    s += ln(96, 10, 96, 90, RED, 1.1, True) + arrow2(72, 86, 96, 86)
    s += T(103, 14, 'C7', 7, 700, INK, 'start') + T(60, 77, 'S1', 7, 700, INK, 'end') + lab(84, 95, 'SVA', BLUE, 7) + T(150, 92, 'avant →', 6.4, 400, MUT)
    s += T(138, 46, 'fil à plomb C7', 6.8, 400, MUT) + T(138, 55, '→ coin postéro-', 6.8, 400, MUT) + T(138, 63, 'supérieur de S1', 6.8, 400, MUT)
    it.append((s, 'SVA', 'positif si C7 en avant de S1', CHIP[4]))
    # 4. Risser
    s = bone('M18,78 C22,20 120,8 148,52 L134,60 C112,32 40,40 36,82Z')
    q = [(148, 52, 128, 22), (128, 22, 94, 12), (94, 12, 58, 18), (58, 18, 24, 48)]
    for i, (x1, y1, x2, y2) in enumerate(q):
        col = RED if i < 2 else '#c7cdd5'
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s += f'<path d="M{x1},{y1} Q{mx + (6 if i < 2 else 0)},{my - 8} {x2},{y2}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round"/>'
        s += T(mx, my - 9, str(i + 1), 7, 700, INK)
    s += T(146, 70, 'EIAS', 6.6, 400, MUT) + T(88, 62, 'Risser 2 ici :', 7, 700, RED) + T(88, 72, '2 quarts ossifiés', 6.8, 400, MUT)
    it.append((s, 'Test de Risser', '5 = apophyse fusionnée', CHIP['p']))
    # 5. Meyerding
    s = bone('M40,58 L104,58 L104,88 L40,88Z') + bone('M66,22 L130,22 L130,52 L66,52Z')
    for k in range(1, 4):
        x = 40 + k * 16
        s += ln(x, 58, x, 62, INK, 0.8)
    s += ln(40, 52, 40, 92, BLUE, 0.9, True) + ln(66, 16, 66, 56, RED, 1.2, True) + arrow2(40, 55, 66, 55)
    s += T(53, 50, '40 %', 7, 700, BLUE) + T(150, 74, 'avant', 6.4, 400, MUT) + T(18, 74, 'arrière', 6.4, 400, MUT)
    it.append((s, 'Meyerding', 'ici grade II (26–50 %)', CHIP[3]))
    # 6. C1-dens
    s = f'<ellipse cx="54" cy="44" rx="9" ry="13" fill="{BONE}" stroke="{LINE}" stroke-width="0.8"/>'
    s += bone('M74,92 L74,40 Q74,22 86,22 Q98,22 98,40 L98,92Z')
    s += arrow2(63, 44, 74, 44) + T(68, 34, 'IAO', 7, 700, BLUE)
    s += T(54, 68, 'arc ant. C1', 6.6, 400, MUT) + T(86, 98, 'dens', 6.6, 400, MUT)
    s += T(136, 44, '< 3 mm adulte', 6.8, 700, INK) + T(136, 54, '< 5 mm enfant', 6.8, 700, INK) + T(136, 64, '(radiographie)', 6.6, 400, MUT)
    it.append((s, 'Intervalle C1–dens', 'atloïdo-odontoïdien antérieur', CHIP[1]))
    save('os04.svg', tiles(it, 3, tw=W, th=H, gap=10, title='Télérachis : mesures principales (profil et face)', note=NOTE + ' · rouge = mesure, bleu = référence'))


# ---------------- OS-05 Hanche ----------------
def hanche():
    W, H = 166, 100
    it = []
    def head(cx, cy, r=20):
        return circ(cx, cy, r)
    def roof(x1, y1, x2, y2, bulge=-16):
        mx = (x1 + x2) / 2; my = (y1 + y2) / 2 + bulge
        return f'<path d="M{x1 - 18},{y1 - 4} L{x1},{y1} Q{mx},{my} {x2},{y2} L{x2 + 4},{y2 - 10} L{x1 - 18},{y1 - 14}Z" fill="#c9d0d9" stroke="{LINE}" stroke-width="0.8"/>'
    def band(C, a1, a2, r1=21, r2=31):
        P = lambda a, r: (C[0] + r * math.cos(math.radians(a)), C[1] + r * math.sin(math.radians(a)))
        p1, p2, p3, p4 = P(a1, r1), P(a2, r1), P(a2, r2), P(a1, r2)
        return (f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A{r1},{r1} 0 0 1 {p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f} '
                f'A{r2},{r2} 0 0 0 {p4[0]:.1f},{p4[1]:.1f}Z" fill="#c9d0d9" stroke="{LINE}" stroke-width="0.8"/>'), p1, p2
    # 1. VCE
    C = (66, 64); r = 20
    b, p1, E = band(C, -175, -60)
    s = b + head(*C, r)
    s += ln(C[0], C[1], C[0], C[1] - 52, BLUE, 1, True) + ln(C[0], C[1], E[0], E[1]) + dot(*E, 1.8) + dot(*C, 1.8) + arc(C[0], C[1], 13, -90, -60)
    s += lab(E[0] + 9, E[1] + 2, 'VCE', RED, 7.5, anchor='start') + T(134, 50, 'normal 25–40°', 6.8, 700, INK) + T(134, 60, '< 20° dysplasie', 6.8, 400, MUT) + T(134, 69, '> 40° pince', 6.8, 400, MUT) + T(108, 94, 'latéral →', 6.4, 400, MUT)
    it.append((s, 'VCE de Wiberg', 'couverture latérale (face)', CHIP[1]))
    # 2. HTE / Tönnis
    C = (66, 64)
    b, Mp, Lp = band(C, -140, -55)
    s = b + head(*C, 20)
    s += ln(Mp[0] - 6, Mp[1], Lp[0] + 22, Mp[1], BLUE, 1, True) + ln(Mp[0], Mp[1], Lp[0] + 8, Lp[1] - 1.1) + dot(*Mp, 1.8) + dot(*Lp, 1.8)
    s += lab(Lp[0] + 14, Lp[1] - 6, 'HTE', RED, 7.5, anchor='start') + T(134, 56, 'normal 0–10°', 6.8, 700, INK) + T(134, 66, '> 10° dysplasie', 6.8, 400, MUT) + T(134, 75, '< 0° pince', 6.8, 400, MUT)
    it.append((s, 'HTE · Tönnis', 'obliquité du sourcil (face)', CHIP[1]))
    # 3. CC'D
    s = bone('M70,96 L92,96 L90,58 L84,40 L70,30 L58,40 L66,56Z') + circ(56, 28, 13)
    s += ln(81, 98, 79, 46, RED, 1.2) + ln(79, 46, 52, 26, RED, 1.2) + arc(79, 46, 12, -143, -92)
    s += lab(92, 34, '130°', RED, 7.5) + T(132, 48, '125–135° normal', 6.8, 700, INK) + T(132, 58, '< 120° coxa vara', 6.8, 400, MUT) + T(132, 67, '> 140° coxa valga', 6.8, 400, MUT)
    it.append((s, "CC'D", 'angle cervico-diaphysaire', CHIP['b']))
    # 4. VCA faux profil
    C = (80, 64)
    b, A, p2 = band(C, -120, -40)
    s = b + head(*C, 20)
    s += ln(C[0], C[1], C[0], C[1] - 52, BLUE, 1, True) + ln(C[0], C[1], A[0], A[1]) + dot(*A, 1.8) + dot(*C, 1.8) + arc(C[0], C[1], 13, -120, -90)
    s += lab(A[0] - 8, A[1] + 2, 'VCA', RED, 7.5, anchor='end') + T(30, 94, '← avant', 6.4, 400, MUT) + T(136, 54, 'normal 25–40°', 6.8, 700, INK) + T(136, 64, '< 20° dysplasie', 6.8, 400, MUT)
    it.append((s, 'VCA de Lequesne', 'couverture antérieure (faux profil)', CHIP[1]))
    # 5. Angle alpha
    C = (52, 46); r = 20
    s = bone(f'M{C[0] + 14},{C[1] - 14} Q{C[0] + 26},{C[1] - 20} {C[0] + 30},{C[1] - 8} L{C[0] + 66},{C[1] - 2} L{C[0] + 66},{C[1] + 22} L{C[0] + 14},{C[1] + 16}Z') + circ(*C, r)
    s += f'<circle cx="{C[0]}" cy="{C[1]}" r="{r}" fill="none" stroke="{BLUE}" stroke-width="0.9" stroke-dasharray="2.5 2"/>'
    P = (C[0] + r * math.cos(math.radians(-58)), C[1] + r * math.sin(math.radians(-58)))
    s += ln(C[0], C[1], C[0] + 70, C[1] + 6, RED, 1.2) + ln(C[0], C[1], P[0] + 6 * math.cos(math.radians(-58)), P[1] + 6 * math.sin(math.radians(-58))) + dot(*P, 2) + arc(C[0], C[1], 11, -58, 5)
    s += lab(C[0] + 18, C[1] - 4, 'α', RED, 9) + T(124, 82, 'bosse : effet came', 6.8, 400, MUT) + T(124, 92, 'α > 55°', 6.8, 700, INK)
    it.append((s, 'Angle alpha', 'jonction tête–col (Dunn, IRM)', CHIP[4]))
    # 6. Signe du croisement
    s = circ(84, 64, 22) + f'<path d="M50,30 Q86,26 100,80" fill="none" stroke="{INK}" stroke-width="1.6"/>' + f'<path d="M62,22 Q74,40 110,70" fill="none" stroke="{RED}" stroke-width="1.6"/>'
    s += dot(73, 34, 2.4, BLUE) + T(126, 26, 'paroi antérieure', 6.6, 700, RED) + T(126, 88, 'paroi postérieure', 6.6, 700, INK) + T(40, 50, 'croisement', 6.8, 700, BLUE)
    it.append((s, 'Signe du croisement', 'rétroversion du cotyle', CHIP[4]))
    save('os05.svg', tiles(it, 3, tw=W, th=H, gap=10, title='Coxométrie et conflit fémoro-acétabulaire', note=NOTE + ' · hanche droite de face, latéral à droite'))


# ---------------- OS-06 Membre inférieur ----------------
def membre():
    W, H = 166, 100
    it = []
    # 1. HKA / MAD (genu varum)
    Hc, K, A = (58, 14), (74, 53), (62, 90)
    s = circ(Hc[0], Hc[1], 7) + f'<path d="M{Hc[0]},{Hc[1]} L{K[0]},{K[1]}" stroke="{BONE}" stroke-width="8" stroke-linecap="round"/>' + f'<path d="M{K[0]},{K[1]} L{A[0]},{A[1]}" stroke="{BONE}" stroke-width="7" stroke-linecap="round"/>'
    s += ln(Hc[0], Hc[1], K[0], K[1], RED, 1.3) + ln(K[0], K[1], A[0], A[1], RED, 1.3) + ln(Hc[0], Hc[1], A[0], A[1], BLUE, 1, True)
    s += dot(*K, 2) + arrow2(60, 52, 73, 52, BLUE) + T(60, 46, 'MAD', 6.6, 700, BLUE, 'end') + lab(84, 56, 'HKA', RED, 7.5, anchor='start')
    s += T(130, 36, 'normal : ≈ 1–1,5°', 6.8, 700, INK) + T(130, 46, 'de varus', 6.8, 700, INK) + T(130, 60, 'MAD 2–6 mm', 6.8, 400, MUT) + T(130, 69, 'en dedans', 6.8, 400, MUT) + T(30, 96, '← dedans', 6.4, 400, MUT)
    it.append((s, 'HKA et axe de Mikulicz', 'ici genu varum', CHIP[3]))
    # 2. mLDFA / MPTA
    s = bone('M44,8 L84,8 L88,38 Q66,48 40,38Z') + bone('M40,54 L90,54 L82,94 L50,94Z')
    s += ln(36, 41, 94, 41, INK, 1.2) + ln(36, 52, 94, 52, INK, 1.2) + ln(70, 2, 66, 44, RED, 1.2) + ln(66, 50, 66, 98, RED, 1.2)
    s += arc(66, 41, 9, -95, 0) + arc(66, 52, 9, 90, 180) + lab(84, 30, 'mLDFA', RED, 7) + lab(46, 68, 'MPTA', RED, 7)
    s += T(132, 44, '85–90°', 7.5, 700, INK) + T(132, 55, 'pour les deux', 6.8, 400, MUT)
    it.append((s, 'mLDFA · MPTA', 'où siège la déformation ?', CHIP['b']))
    # 3. TA-GT
    s = bone('M24,58 Q24,24 58,22 Q74,36 80,36 Q86,36 102,22 Q136,24 136,58Z') + f'<ellipse cx="114" cy="72" rx="12" ry="8" fill="#c9d0d9" stroke="{LINE}" stroke-width="0.8"/>'
    s += ln(20, 60, 140, 60, BLUE, 1, True) + ln(80, 36, 80, 92, RED, 1, True) + ln(114, 66, 114, 92, RED, 1, True) + dot(80, 36, 2) + dot(114, 66, 2)
    s += arrow2(80, 88, 114, 88) + lab(97, 84, 'TA-GT', BLUE, 7) + T(80, 31, 'gorge', 6.4, 400, MUT) + T(140, 82, 'TTA', 6.4, 700, INK)
    it.append((s, 'TA-GT', '< 15 mm · > 20 mm pathologique', CHIP[4]))
    # 4. Caton-Deschamps
    s = bone('M30,4 L74,4 L82,36 Q60,48 30,40Z') + bone('M30,62 L96,62 L86,98 L40,98Z')
    s += f'<ellipse cx="98" cy="34" rx="8" ry="16" fill="#c9d0d9" stroke="{LINE}" stroke-width="0.8" transform="rotate(-12 98 34)"/>'
    s += ln(93, 20, 91, 46, BLUE, 2) + dot(91, 46, 2, BLUE) + dot(96, 62, 2) + ln(91, 46, 96, 62, RED, 1.4)
    s += lab(104, 58, 'A', RED, 7.5, anchor='start') + lab(84, 28, 'B', BLUE, 7.5) + T(136, 34, 'CD = A / B', 7.5, 700, INK) + T(136, 46, 'normal 0,6–1,2', 6.8, 400, MUT) + T(136, 56, '> 1,2 : haute', 6.8, 400, MUT)
    it.append((s, 'Caton-Deschamps', 'hauteur rotulienne, profil 30°', CHIP[1]))
    # 5. Signe du croisement (Dejour)
    s = bone('M20,96 L20,40 Q24,10 62,8 Q96,10 104,40 Q108,62 98,96Z')
    s += f'<path d="M96,22 Q108,40 104,62 Q100,80 92,96" fill="none" stroke="{INK}" stroke-width="1.4"/>'
    s += f'<path d="M84,12 Q92,30 106,46 Q96,70 90,96" fill="none" stroke="{RED}" stroke-width="1.4"/>'
    s += dot(103, 44, 2.4, BLUE) + f'<path d="M84,12 L90,6 L92,14" fill="none" stroke="{RED}" stroke-width="1.2"/>'
    s += T(132, 30, 'fond de trochlée', 6.6, 700, RED) + T(132, 40, '(rouge)', 6.4, 400, MUT) + T(132, 60, 'condyle latéral', 6.6, 700, INK) + T(132, 82, 'éperon en haut', 6.4, 400, MUT)
    it.append((s, 'Signe du croisement', 'dysplasie de la trochlée', CHIP[4]))
    # 6. Antéversion fémorale (superposition)
    s = circ(60, 30, 11) + bone('M64,38 L94,48 L90,58 L60,44Z') + bone('M30,74 Q46,62 66,70 Q86,62 110,74 L106,92 L34,92Z')
    s += ln(40, 22, 104, 50, RED, 1.3) + ln(26, 92, 116, 92, BLUE, 1.2, True) + ln(26, 78, 116, 78, BLUE, 0.7, True)
    s += ln(40, 22, 100, 22, BLUE, 0.8, True) + arc(40, 22, 20, 0, 24) + lab(66, 18, 'antéversion', RED, 6.8, anchor='start')
    s += T(134, 60, 'Lerat 14 ± 7°', 6.8, 700, INK) + T(134, 70, 'col / condyles', 6.6, 400, MUT) + T(134, 79, 'postérieurs', 6.6, 400, MUT)
    it.append((s, 'Antéversion fémorale', 'scanner, coupes superposées', CHIP['b']))
    save('os06.svg', tiles(it, 3, tw=W, th=H, gap=10, title='Pangonogramme et fémoro-patellaire', note=NOTE + ' · rouge = mesure, bleu = référence'))


# ---------------- OS-07 Pied, poignet, épaule, coude ----------------
def extremites():
    it = []
    # 1. Djian-Annonier
    Ca, Tn, Se = (16, 80), (62, 44), (106, 80)
    s = bone('M10,82 Q8,58 30,52 Q50,34 70,38 Q90,52 112,74 L112,84 Q60,90 10,82Z')
    s += ln(Ca[0], Ca[1], Tn[0], Tn[1]) + ln(Tn[0], Tn[1], Se[0], Se[1]) + dot(*Ca) + dot(*Tn) + dot(*Se)
    s += arc(Tn[0], Tn[1], 10, 38, 142) + lab(62, 70, '115–135°', RED, 7) + ln(4, 88, 114, 88, MUT, 0.6)
    it.append((s, 'Djian-Annonier', 'arche interne, profil en charge', CHIP[1]))
    # 2. Méary
    s = bone('M14,50 Q20,34 40,36 L58,44 Q50,58 30,58Z') + bone('M64,46 L104,60 L102,68 L62,54Z')
    s += ln(10, 40, 110, 66, RED, 1.2) + T(59, 84, 'axe talus = axe M1', 6.8, 700, INK) + T(59, 30, 'rectiligne', 6.6, 400, MUT)
    it.append((s, 'Méary-Toméno', 'cassure : plat ou creux', CHIP[1]))
    # 3. Hallux valgus
    s = bone('M50,92 L60,92 L48,46 L38,46Z') + bone('M68,92 L78,92 L78,44 L70,44Z') + bone('M38,44 L48,44 L64,18 L56,14Z')
    s += ln(55, 96, 41, 34, RED, 1.1) + ln(73, 96, 74, 30, BLUE, 1.1) + ln(43, 46, 62, 10, RED, 1.1)
    s += lab(26, 22, 'HVA', RED, 7) + T(100, 30, 'HVA', 6.6, 700, RED) + T(100, 39, '< 15°', 6.6, 700, INK) + T(100, 62, 'M1–M2', 6.6, 700, BLUE) + T(100, 71, '< 9°', 6.6, 700, INK)
    it.append((s, 'Hallux valgus', 'HVA &lt; 15° · M1–M2 &lt; 9°', CHIP[3]))
    # 4. Böhler
    P1, P2, P3 = (100, 46), (62, 30), (18, 44)
    s = bone('M14,48 Q14,30 30,32 L62,28 L80,40 L104,44 Q112,58 100,70 L30,74 Q12,70 14,48Z')
    s += ln(P1[0], P1[1], P2[0], P2[1]) + ln(P2[0], P2[1], P3[0], P3[1]) + dot(*P1) + dot(*P2) + dot(*P3)
    s += lab(60, 50, 'Böhler', RED, 7) + T(60, 88, 'normal 25–40°', 6.8, 700, INK)
    it.append((s, 'Angle de Böhler', '&lt; 25° : enfoncement', CHIP[4]))
    # 5. Inclinaison radiale (styloïde radiale à gauche, ulna à droite)
    s = bone('M28,96 L28,30 L74,48 L74,96Z') + bone('M82,96 L82,52 L96,52 L96,96Z')
    s += ln(51, 98, 51, 18, BLUE, 1, True) + ln(18, 26, 84, 52, RED, 1.2) + ln(18, 30, 84, 30, BLUE, 0.8, True)
    s += lab(96, 26, '22–23°', RED, 7) + T(51, 90, 'radius', 6.4, 400, MUT) + T(89, 90, 'ulna', 6.4, 400, MUT)
    it.append((s, 'Inclinaison radiale', 'face · pente palmaire ≈ 11°', CHIP[1]))
    # 6. Scapho-lunaire
    s = f'<ellipse cx="44" cy="58" rx="13" ry="22" fill="{BONE}" stroke="{LINE}" stroke-width="0.8" transform="rotate(-48 44 58)"/>' + bone('M70,42 Q90,36 96,52 Q90,68 70,64 Q76,52 70,42Z')
    s += ln(26, 78, 64, 38, RED, 1.2) + ln(83, 26, 83, 84, BLUE, 1.2)
    s += lab(30, 32, 'scaphoïde', MUT, 6.4, 400) + lab(100, 82, 'lunatum', MUT, 6.4, 400) + lab(62, 92, '30–60°', RED, 7.5)
    it.append((s, 'Angle scapho-lunaire', '&gt; 60° DISI · &lt; 30° VISI', CHIP['b']))
    # 7. CSA
    s = bone('M70,30 L76,30 L80,86 L72,86Z') + bone('M60,14 L112,10 L112,18 L64,22Z') + circ(96, 58, 15)
    s += ln(73, 22, 76, 94, BLUE, 1.2) + ln(76, 86, 112, 16, RED, 1.2) + dot(112, 16) + dot(76, 86)
    s += lab(42, 56, '30–35°', RED, 7.5) + T(40, 66, 'normal', 6.4, 400, MUT)
    it.append((s, 'Angle critique (CSA)', '&gt; 35° coiffe · &lt; 30° arthrose', CHIP[3]))
    # 8. Coude : ligne humérale antérieure
    s = bone('M36,4 L60,4 L66,60 Q60,76 46,74 Q36,60 36,4Z') + circ(62, 74, 12) + bone('M74,84 L104,96 L100,100 L70,92Z')
    s += ln(43, 4, 66, 94, RED, 1.2) + f'<path d="M58,63 A12,12 0 0 1 58,85" fill="none" stroke="{BLUE}" stroke-width="2.2"/>'
    s += T(96, 50, 'tiers moyen', 6.6, 700, INK) + T(96, 59, 'du capitulum', 6.6, 400, MUT)
    it.append((s, 'Ligne humérale ant.', 'coude de l\'enfant, profil', CHIP[1]))
    save('os07.svg', tiles(it, 4, title='Pied, poignet, épaule, coude', note=NOTE + ' · rouge = mesure, bleu = référence'))


if __name__ == '__main__':
    rachis(); hanche(); membre(); extremites(); print('ok')
