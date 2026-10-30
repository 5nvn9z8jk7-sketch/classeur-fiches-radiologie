"""Schémas de la fiche NE-04 (scanner de perfusion, IntelliSpace Portal). Lancer : python3 src/gen/perfusion.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import T, tiles, save, CHIP, NOTE, INK, MUT, LINE
from ortho import ln, dot, lab, arrow2, RED, BLUE

GREEN = '#2f8f4e'; ORANGE = '#d9822b'; YEL = '#d8b11f'


def curve(f, x0, x1, y0, sx, sy, c, w=1.6):
    pts = []
    for i in range(61):
        t = i / 60
        x = x0 + (x1 - x0) * t
        pts.append(f"{x:.1f},{y0 - sy * f(t):.1f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"/>'


def g(mu, sd, a):
    return lambda t: a * math.exp(-((t - mu) ** 2) / (2 * sd * sd))


def build():
    W, H = 166, 100
    it = []
    # 1. Courbes temps-densité
    s = ln(14, 88, 156, 88, INK, 0.8) + ln(14, 88, 14, 8, INK, 0.8)
    s += curve(g(0.30, 0.07, 1.0), 14, 156, 88, 1, 70, RED) + curve(g(0.42, 0.10, 0.9), 14, 156, 88, 1, 70, BLUE)
    s += curve(g(0.40, 0.13, 0.18), 14, 156, 88, 1, 70, MUT, 1.3)
    s += f'<rect x="15" y="80" width="20" height="7" fill="#e8ecf1"/>' + T(25, 78, 'base', 6.2, 400, MUT)
    s += T(52, 14, 'artère', 6.8, 700, RED) + T(96, 22, 'veine', 6.8, 700, BLUE) + T(120, 70, 'tissu', 6.6, 400, MUT) + T(140, 97, 'temps', 6.2, 400, MUT)
    it.append((s, 'Courbes temps-densité', 'montée et descente complètes', CHIP['b']))
    # 2. Summary map schématique (hémisphère droit du patient à gauche de l'image)
    s = f'<ellipse cx="66" cy="50" rx="42" ry="44" fill="#eef1f4" stroke="{LINE}" stroke-width="0.9"/>'
    s += ln(66, 6, 66, 94, MUT, 0.8, True)
    s += f'<path d="M63,22 Q32,16 28,46 Q30,74 58,80 Q50,52 63,22Z" fill="{GREEN}" opacity="0.75"/>'
    s += f'<ellipse cx="45" cy="52" rx="10" ry="13" fill="{RED}" opacity="0.9"/>'
    s += T(146, 36, 'rouge', 6.8, 700, RED) + T(146, 45, 'cœur estimé', 6.4, 400, MUT) + T(146, 62, 'vert', 6.8, 700, GREEN) + T(146, 71, 'pénombre', 6.4, 400, MUT)
    s += T(14, 96, 'D', 6.6, 700, INK) + T(118, 96, 'G', 6.6, 700, INK)
    it.append((s, 'Summary map ISP', 'MTT &gt; 150 % · CBV 2 mL/100 g', CHIP[4]))
    # 3. Profils cœur / pénombre
    rows = [('CBF', '↓↓', '↓'), ('CBV', '↓', '= ou ↑'), ('MTT', '↑', '↑'), ('Tmax', '↑', '↑')]
    s = T(80, 14, 'cœur', 7, 700, RED) + T(130, 14, 'pénombre', 7, 700, GREEN)
    for i, (p, a, b) in enumerate(rows):
        y = 32 + i * 17
        s += f'<rect x="10" y="{y - 10}" width="146" height="14" rx="3" fill="{"#f4f6f8" if i % 2 == 0 else "#fff"}"/>'
        s += T(30, y, p, 7.5, 700, INK) + T(80, y, a, 8, 700, RED) + T(130, y, b, 8, 700, GREEN)
    it.append((s, 'Cœur ou pénombre ?', 'la clé : le CBV', CHIP[1]))
    # 4. Conversion du ratio
    s = f'<rect x="14" y="20" width="62" height="26" rx="4" fill="{GREEN}" opacity="0.8"/>' + f'<rect x="76" y="20" width="24" height="26" rx="4" fill="{RED}" opacity="0.9"/>'
    s += T(45, 37, 'V vert', 7.4, 700, '#fff') + T(88, 37, 'rouge', 6.4, 700, '#fff')
    s += arrow2(14, 54, 100, 54) + T(57, 64, 'hypoperfusion totale', 6.6, 400, MUT)
    s += T(83, 84, 'ratio = (V vert + V rouge) / V rouge', 7, 700, INK) + T(83, 95, 'mismatch absolu = V vert', 6.6, 400, MUT)
    s += T(134, 30, 'DEFUSE 3', 6.6, 700, INK) + T(134, 39, '≥ 1,8', 6.6, 400, MUT) + T(134, 52, 'EXTEND', 6.6, 700, INK) + T(134, 61, '&gt; 1,2', 6.6, 400, MUT)
    it.append((s, 'Ratio de mismatch', 'au format des essais', CHIP[3]))
    # 5. Traffic Lights
    s = ''
    for i, (c, t1, t2) in enumerate([(GREEN, 'vert', 'analyse possible'), (YEL, 'jaune', 'prudence'), (RED, 'rouge', 'ne pas utiliser')]):
        y = 22 + i * 28
        s += f'<circle cx="40" cy="{y}" r="10" fill="{c}"/>' + T(60, y - 1, t1, 7.4, 700, INK, 'start') + T(60, y + 9, t2, 6.6, 400, MUT, 'start')
    it.append((s, 'Traffic Lights', 'contrôle qualité automatique', CHIP[3]))
    # 6. Où placer artère et veine
    s = f'<ellipse cx="62" cy="50" rx="40" ry="44" fill="#eef1f4" stroke="{LINE}" stroke-width="0.9"/>' + ln(62, 6, 62, 94, MUT, 0.8, True)
    s += dot(72, 30, 3.6, RED) + dot(62, 90, 4, BLUE) + f'<path d="M30,40 Q44,58 54,50" fill="none" stroke="#c7cdd5" stroke-width="5"/>'
    s += T(108, 26, 'ACA ou ACM', 6.6, 700, RED, 'start') + T(108, 35, 'côté sain', 6.4, 400, MUT, 'start') + T(108, 84, 'sinus sagittal', 6.6, 700, BLUE, 'start') + T(108, 93, 'supérieur', 6.4, 400, MUT, 'start')
    s += T(40, 22, 'côté atteint', 6.2, 400, MUT)
    it.append((s, 'Artère et veine', 'références du calcul', CHIP['b']))
    save('ne04.svg', tiles(it, 3, tw=W, th=H, gap=10, title='Scanner de perfusion sur IntelliSpace Portal', note=NOTE + ' · couleurs de la summary map Philips'))


if __name__ == '__main__':
    build(); print('ok')
