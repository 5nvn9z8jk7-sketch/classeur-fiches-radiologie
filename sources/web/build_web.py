"""Génère la version web statique du classeur dans ../site à partir des fiches HTML déjà construites (src/build.py)."""
import json, os, re, html, shutil, ast
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = f'{D}/src'; OUT = f'{D}/site'; W = f'{D}/web'
meta = json.load(open(f'{S}/fiches.json'))
order = ["Transversal","Neuro","Cou","Sein","Thorax","Cœur · vaisseaux","Foie","Pancréas","Tube digestif","Rein · surrénale","Pelvis","Ostéo-articulaire"]
bsrc = open(f'{S}/binder.py').read()
desc = ast.literal_eval(re.search(r'^desc=(\{.*?\})\s*$', bsrc, re.M).group(1))
veille = ast.literal_eval(re.search(r'^veille=(\{.*?\n\})', bsrc, re.M | re.S).group(1))
vdate_m = re.search(r'^vdate=(\{.*?\})\s*
fo1 = {"code":"FO-01","organe":"Foie","oc":"#0f6e6e","ol":"#eef6f6","plain":"LI-RADS CT/IRM – foie cirrhotique",
       "title":"LI-RADS <span>CT/IRM</span> · foie cirrhotique","ref":"LI-RADS CT/MRI v2018","sub":"critères majeurs, accessoires, arbre diagnostique"}
fiches = [m for m in meta if not m.get('hidden')] + [fo1]
fiches.sort(key=lambda m: (order.index(m['organe']), m['code']))
ocol = {}
for m in fiches: ocol.setdefault(m['organe'], m['oc'])

def scope_css(css, scope):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'@font-face\{[^}]*\}|@page\{[^}]*\}', '', css)
    out = []
    for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        sels = []
        for s in sel.split(','):
            s = s.strip()
            if not s: continue
            if s in ('body', 'html'): sels.append(scope)
            elif s == '*': sels.append(f'{scope} *')
            else: sels.append(f'{scope} {s}')
        body = body.replace('font-family:IS,sans-serif', 'font-family:inherit').replace('font-family:InterS,sans-serif', 'font-family:inherit')
        out.append(','.join(sels) + '{' + body + '}')
    return '\n'.join(out)

def parts(path):
    t = open(path).read()
    st = ''.join(re.findall(r'<style>(.*?)</style>', t, re.S))
    if 'href="base.css"' in t: st = open(f'{S}/base.css').read() + st
    body = re.search(r'<body[^>]*>(.*)</body>', t, re.S).group(1)
    return st, body

HEAD_RE = r'<div class="head"(?: style="[^"]*")?><div class="l">.*?</div><div class="meta">.*?</div></div>'
def clean(body, drop_first=True):
    body = re.sub(r'<div class="pb"></div>', '', body)
    # on retire tous les en-têtes (le titre est affiché par la page web) : div équilibrée
    while True:
        i = body.find('<div class="head"')
        if i < 0: break
        depth = 0; j = i
        for mt in re.finditer(r'<div\b|</div>', body[i:]):
            depth += 1 if mt.group(0) != '</div>' else -1
            if depth == 0: j = i + mt.end(); break
        body = body[:i] + body[j:]
    body = body.replace('Pour aller plus loin · cliquer ou scanner le QR code', 'Pour aller plus loin')
    body = re.sub(r'<div class="foot">', '<div class="foot">', body)
    return body

CODES = None
def xlink(body, self_code):
    codes = CODES
    out = []; in_a = 0
    for part in re.split(r'(<[^>]+>)', body):
        if part.startswith('<'):
            if re.match(r'<a\b', part): in_a += 1
            elif part.startswith('</a'): in_a = max(0, in_a - 1)
            out.append(part); continue
        if in_a or not part: out.append(part); continue
        out.append(re.sub(r'\b([A-Z]{2}-0\d)\b', lambda g: f'<a class="xref" href="{g.group(1)}.html">{g.group(1)}</a>' if g.group(1) in codes and g.group(1) != self_code else g.group(1), part))
    return ''.join(out)

def text_of(h):
    t = re.sub(r'<svg.*?</svg>', ' ', h, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()

# ---------- pages ----------
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(f'{OUT}/f'); os.makedirs(f'{OUT}/pdf'); os.makedirs(f'{OUT}/assets')
for w in (400, 500, 600, 700): shutil.copy(f'{S}/Inter-{w}.ttf', f'{OUT}/assets/Inter-{w}.ttf')
shutil.copy(f'{W}/site.css', f'{OUT}/assets/site.css')
shutil.copy(f'{W}/app.js', f'{OUT}/assets/app.js')
for ic in ('icon-192.png','icon-512.png','icon-maskable-512.png','apple-touch-icon.png'): shutil.copy(f'{W}/{ic}', f'{OUT}/assets/{ic}')
shutil.copy(f'{D}/Classeur-fiches-radiologie.pdf', f'{OUT}/pdf/Classeur-fiches-radiologie.pdf')
shutil.copy(f'{D}/Fiches-radiologie-par-organe.zip', f'{OUT}/pdf/Fiches-radiologie-par-organe.zip')
for m in fiches: shutil.copy(f'{D}/pdf/{m["code"]}.pdf', f'{OUT}/pdf/{m["code"]}.pdf')

def nav(cur=None, root=''):
    s = ''
    for o in order:
        items = ''.join(f'<li><a data-code="{m["code"]}" href="{root}f/{m["code"]}.html"{" aria-current=page" if m["code"]==cur else ""}><span class="w-code">{m["code"]}</span>{html.escape(html.unescape(m["plain"]))}</a></li>' for m in fiches if m['organe'] == o)
        s += f'<div class="w-navg" style="--oc:{ocol[o]}"><div class="w-navh"><i></i>{o}</div><ul>{items}</ul></div>'
    return s

def page(title, main, root='', cur=None, extra_head='', side=True, active=''):
    tabs = [('index.html','Fiches'),('outils.html','Calculateurs'),('registre.html','Registre des versions')]
    tb = ''.join(f'<a href="{root}{u}"{" class=on" if active==u else ""}>{l}</a>' for u, l in tabs)
    sidebar = f'<aside class="w-side" id="w-side"><div class="w-sidein"><div class="w-sidetabs">{tb}</div>{nav(cur, root)}</div></aside>'
    return f'''<!DOCTYPE html><html lang="fr" data-root="{root}"><head><meta name="theme-color" content="#1d2430"><link rel="manifest" href="{root}manifest.webmanifest"><link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Classeur radio"><meta name="apple-mobile-web-app-status-bar-style" content="black"><script>document.documentElement.dataset.theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'</script><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22%3E%3Crect x=%223%22 y=%223%22 width=%2218%22 height=%2218%22 rx=%224%22 fill=%22%231d2430%22/%3E%3C/svg%3E"><link rel="stylesheet" href="{root}assets/site.css">{extra_head}</head>
<body class="{'w-hasside' if side else ''}"><header class="w-top"><div class="w-topin">
<button class="w-burger" aria-label="Menu et liste des fiches" aria-controls="w-side" aria-expanded="false"><span></span><span></span><span></span></button>
<a class="w-brand" href="{root}index.html" aria-label="Accueil du classeur"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8 3v18M12 8h5M12 12h5M12 16h3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><span>Classeur radiologie</span></a>
<nav class="w-tabs" aria-label="Sections">{tb}</nav>
<button class="w-theme" type="button" aria-label="Changer de thème" title="Mode clair ou sombre (suit le réglage de l'appareil à l'ouverture)"></button><form class="w-search" action="{root}index.html" role="search"><input type="search" name="q" placeholder="Rechercher une fiche, un score, un signe…" aria-label="Rechercher"></form>
</div></header>
<div class="w-shell">{sidebar}<main class="w-main" id="contenu">{main}</main></div>
<footer class="w-foot"><div>Aide-mémoire pour radiologues et internes. Ne remplace ni les recommandations originales, ni la discussion multidisciplinaire, ni le jugement clinique. Schémas simplifiés, non à l'échelle ; les images de référence sont consultables via les liens (Radiopaedia, sociétés savantes). Dernière vérification : 30 octobre 2026. <span id="w-offline" hidden>· Consultable hors ligne sur cet appareil après une première visite.</span></div></footer>
<script src="{root}assets/app.js"></script></body></html>'''

CODES = {m['code'] for m in fiches}
index_data = []
for i, m in enumerate(fiches):
    code = m['code']
    if code == 'FO-01':
        st1, b1 = parts(f'{S}/FO-01.html'); st2, b2 = parts(f'{S}/FO-01X.html')
        css = scope_css(st1, '.fx1') + '\n' + scope_css(st2, '.fx2')
        b1 = clean(b1); b2 = clean(b2)
        # pied de page unique : celui de la partie atlas
        b1 = re.sub(r'<div class="foot">.*?</div>\s*$', '', b1.strip(), flags=re.S)
        content = f'<div class="fiche fx1">{b1}</div><div class="fiche fx2" style="--oc:#0f6e6e;--ol:#eef6f6">{b2}</div>'
        srcs = []
    else:
        st, b = parts(f'{S}/{code}.html')
        css = scope_css(st, '.fx1')
        b = clean(b)
        if code == 'NE-01':
            b = b.replace('{{SVG:aspects.svg}}', '')
        content = f'<div class="fiche fx1" style="--oc:{m["oc"]};--ol:{m.get("ol","#f3f5f8")}">{b}</div>'
    content = xlink(content, code)
    prev = fiches[i-1] if i > 0 else None; nxt = fiches[i+1] if i < len(fiches)-1 else None
    pn = '<nav class="w-pn" aria-label="Fiche précédente ou suivante">' + (f'<a href="{prev["code"]}.html"><small>Précédente</small>{prev["code"]} · {html.escape(html.unescape(prev["plain"]))}</a>' if prev else '<span></span>') + (f'<a class="nx" href="{nxt["code"]}.html"><small>Suivante</small>{nxt["code"]} · {html.escape(html.unescape(nxt["plain"]))}</a>' if nxt else '<span></span>') + '</nav>'
    tools = {'NE-01':'aspects','FO-01':'lirads','CO-01':'eutirads','OS-01':'bonerads','TH-01':'fleischner','TH-02':'lungrads','CV-01':'cadrads','RS-01':'bosniak','PE-01':'pirads'}
    tl = f'<a class="w-btn ghost" href="../outils.html#{tools[code]}">Calculateur interactif</a>' if code in tools else ''
    hdr = f'''<div class="w-fh" style="--oc:{m['oc']}"><div><span class="w-pill">{m['organe']} · {code}</span><h1>{m['title']}</h1><p>{m['ref']} · {m['sub']}</p></div>
<div class="w-actions">{tl}<a class="w-btn" href="../pdf/{code}.pdf" download>Télécharger le PDF</a><button class="w-btn ghost" onclick="window.print()">Imprimer</button></div></div>'''
    main = hdr + content + pn
    html_ = page(f'{code} – {html.unescape(m["plain"])} · Classeur radiologie', main, '../', code, f'<style>{css}</style>')
    open(f'{OUT}/f/{code}.html', 'w').write(html_)
    index_data.append({'c': code, 'o': m['organe'], 'oc': m['oc'], 't': html.unescape(m['plain']), 'r': m['ref'], 's': m['sub'],
                       'x': text_of(content)[:6000]})

# ---------- accueil ----------
cards = ''
for o in order:
    fs = [d for d in index_data if d['o'] == o]
    cs = ''.join(f'<a class="w-card" href="f/{d["c"]}.html" data-code="{d["c"]}"><span class="w-code">{d["c"]}</span><b>{html.escape(d["t"])}</b><small>{html.escape(d["r"])}</small></a>' for d in fs)
    cards += f'<section class="w-org" style="--oc:{ocol[o]}" data-org="{o}"><div class="w-orgh"><h2>{o}</h2><p>{desc[o]}</p></div><div class="w-cards">{cs}</div></section>'
home = f'''<section class="w-hero"><div><h1>Fiches d'aide à la lecture en radiologie</h1>
<p>{len(fiches)} fiches classées par organe, alignées sur les recommandations et classifications en vigueur en octobre 2026 : critères, seuils, catégories et conduites à tenir, avec schémas et liens vers les aspects d'imagerie attendus.</p>
<div class="w-actions"><a class="w-btn" href="pdf/Classeur-fiches-radiologie.pdf" download>Classeur complet (PDF)</a><a class="w-btn ghost" href="pdf/Fiches-radiologie-par-organe.zip" download>PDF séparés (zip)</a><a class="w-btn ghost" href="outils.html">Calculateurs</a></div></div>
<div class="w-stats"><div><b>{len(fiches)}</b><span>fiches</span></div><div><b>12</b><span>organes</span></div><div><b>11</b><span>calculateurs</span></div></div></section>
<div class="w-filter"><input id="q" type="search" placeholder="Filtrer : PI-RADS, wash-out, Bosniak, embolie…" aria-label="Filtrer les fiches"><div class="w-chips" id="chips"><button class="on" data-o="">Tous</button>{''.join(f'<button data-o="{o}" style="--oc:{ocol[o]}">{o}</button>' for o in order)}</div></div>
<div id="results" class="w-results" hidden></div>
<div id="orgs">{cards}</div>
<script>window.IDX={json.dumps(index_data, ensure_ascii=False)};</script>'''
open(f'{OUT}/index.html', 'w').write(page("Classeur – Fiches d'aide à la lecture en radiologie", home, '', None, '', False, 'index.html'))

# ---------- registre ----------
rows = ''.join(f'<tr><td><a class="w-code" style="--oc:{d["oc"]}" href="f/{d["c"]}.html">{d["c"]}</a></td><td>{html.escape(d["t"])}</td><td>{veille.get(d["c"],("",""))[0]}</td><td class="nw">{vdate.get(d["c"],"29/10/2026")}</td><td class="{"mute" if veille.get(d["c"],("","—"))[1]=="—" else "watch"}">{veille.get(d["c"],("","—"))[1]}</td></tr>' for d in index_data)
reg = f'''<div class="w-fh" style="--oc:#1d2430"><div><span class="w-pill">Veille</span><h1>Registre des versions</h1><p>Référence utilisée par fiche et mises à jour attendues. Vérification trimestrielle programmée.</p></div></div>
<div class="w-tablewrap"><table class="w-table"><thead><tr><th>Code</th><th>Fiche</th><th>Référence en vigueur</th><th>Vérifiée le</th><th>À surveiller</th></tr></thead><tbody>{rows}</tbody></table></div>'''
open(f'{OUT}/registre.html', 'w').write(page('Registre des versions · Classeur radiologie', reg, '', None, '', False, 'registre.html'))

# ---------- outils ----------
tools_html = open(f'{W}/outils_body.html').read().replace('{{ASPECTS_SVG}}', open(f'{S}/gen/aspects_i.svg').read())
open(f'{OUT}/outils.html', 'w').write(page('Calculateurs · Classeur radiologie', tools_html, '', None, '', False, 'outils.html'))
files = []
for dp, dn, fn in os.walk(OUT):
    for x in fn:
        r = os.path.relpath(os.path.join(dp, x), OUT)
        if r.endswith('.zip') or r == 'pdf/Classeur-fiches-radiologie.pdf' or r.startswith('.git'): continue
        files.append(r)
files.append('')
import hashlib
ver = hashlib.md5(''.join(sorted(open(os.path.join(OUT, f), 'rb').read().hex()[:64] + f for f in files if f)).encode()).hexdigest()[:10]
open(f'{OUT}/sw.js', 'w').write(open(f'{W}/sw_template.js').read().replace('__VER__', ver).replace('__FILES__', json.dumps(files)))
open(f'{OUT}/manifest.webmanifest', 'w').write(json.dumps({"name": "Classeur de fiches radiologie", "short_name": "Classeur radio", "lang": "fr", "start_url": "index.html", "display": "standalone", "background_color": "#f4f5f7", "theme_color": "#1d2430", "id": "classeur-radiologie", "scope": "./", "orientation": "any", "description": "Fiches d'aide à la lecture en radiologie classées par organe, avec calculateurs", "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"}, {"src": "assets/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}, {"src": "assets/icon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False))
open(f'{OUT}/assets/icon.svg', 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="5" fill="#1d2430"/><rect x="5" y="5" width="14" height="14" rx="3" fill="none" stroke="#fff" stroke-width="1.6"/><path d="M9 5v14M12 9h4M12 12h4M12 15h2.5" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/></svg>')
print('ok', len(index_data), 'fiches', len(files), 'fichiers hors ligne')
, bsrc, re.M)
vdate = ast.literal_eval(vdate_m.group(1)) if vdate_m else {}
fo1 = {"code":"FO-01","organe":"Foie","oc":"#0f6e6e","ol":"#eef6f6","plain":"LI-RADS CT/IRM – foie cirrhotique",
       "title":"LI-RADS <span>CT/IRM</span> · foie cirrhotique","ref":"LI-RADS CT/MRI v2018","sub":"critères majeurs, accessoires, arbre diagnostique"}
fiches = [m for m in meta if not m.get('hidden')] + [fo1]
fiches.sort(key=lambda m: (order.index(m['organe']), m['code']))
ocol = {}
for m in fiches: ocol.setdefault(m['organe'], m['oc'])

def scope_css(css, scope):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'@font-face\{[^}]*\}|@page\{[^}]*\}', '', css)
    out = []
    for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        sels = []
        for s in sel.split(','):
            s = s.strip()
            if not s: continue
            if s in ('body', 'html'): sels.append(scope)
            elif s == '*': sels.append(f'{scope} *')
            else: sels.append(f'{scope} {s}')
        body = body.replace('font-family:IS,sans-serif', 'font-family:inherit').replace('font-family:InterS,sans-serif', 'font-family:inherit')
        out.append(','.join(sels) + '{' + body + '}')
    return '\n'.join(out)

def parts(path):
    t = open(path).read()
    st = ''.join(re.findall(r'<style>(.*?)</style>', t, re.S))
    if 'href="base.css"' in t: st = open(f'{S}/base.css').read() + st
    body = re.search(r'<body[^>]*>(.*)</body>', t, re.S).group(1)
    return st, body

HEAD_RE = r'<div class="head"(?: style="[^"]*")?><div class="l">.*?</div><div class="meta">.*?</div></div>'
def clean(body, drop_first=True):
    body = re.sub(r'<div class="pb"></div>', '', body)
    # on retire tous les en-têtes (le titre est affiché par la page web) : div équilibrée
    while True:
        i = body.find('<div class="head"')
        if i < 0: break
        depth = 0; j = i
        for mt in re.finditer(r'<div\b|</div>', body[i:]):
            depth += 1 if mt.group(0) != '</div>' else -1
            if depth == 0: j = i + mt.end(); break
        body = body[:i] + body[j:]
    body = body.replace('Pour aller plus loin · cliquer ou scanner le QR code', 'Pour aller plus loin')
    body = re.sub(r'<div class="foot">', '<div class="foot">', body)
    return body

CODES = None
def xlink(body, self_code):
    codes = CODES
    out = []; in_a = 0
    for part in re.split(r'(<[^>]+>)', body):
        if part.startswith('<'):
            if re.match(r'<a\b', part): in_a += 1
            elif part.startswith('</a'): in_a = max(0, in_a - 1)
            out.append(part); continue
        if in_a or not part: out.append(part); continue
        out.append(re.sub(r'\b([A-Z]{2}-0\d)\b', lambda g: f'<a class="xref" href="{g.group(1)}.html">{g.group(1)}</a>' if g.group(1) in codes and g.group(1) != self_code else g.group(1), part))
    return ''.join(out)

def text_of(h):
    t = re.sub(r'<svg.*?</svg>', ' ', h, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()

# ---------- pages ----------
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(f'{OUT}/f'); os.makedirs(f'{OUT}/pdf'); os.makedirs(f'{OUT}/assets')
for w in (400, 500, 600, 700): shutil.copy(f'{S}/Inter-{w}.ttf', f'{OUT}/assets/Inter-{w}.ttf')
shutil.copy(f'{W}/site.css', f'{OUT}/assets/site.css')
shutil.copy(f'{W}/app.js', f'{OUT}/assets/app.js')
for ic in ('icon-192.png','icon-512.png','icon-maskable-512.png','apple-touch-icon.png'): shutil.copy(f'{W}/{ic}', f'{OUT}/assets/{ic}')
shutil.copy(f'{D}/Classeur-fiches-radiologie.pdf', f'{OUT}/pdf/Classeur-fiches-radiologie.pdf')
shutil.copy(f'{D}/Fiches-radiologie-par-organe.zip', f'{OUT}/pdf/Fiches-radiologie-par-organe.zip')
for m in fiches: shutil.copy(f'{D}/pdf/{m["code"]}.pdf', f'{OUT}/pdf/{m["code"]}.pdf')

def nav(cur=None, root=''):
    s = ''
    for o in order:
        items = ''.join(f'<li><a data-code="{m["code"]}" href="{root}f/{m["code"]}.html"{" aria-current=page" if m["code"]==cur else ""}><span class="w-code">{m["code"]}</span>{html.escape(html.unescape(m["plain"]))}</a></li>' for m in fiches if m['organe'] == o)
        s += f'<div class="w-navg" style="--oc:{ocol[o]}"><div class="w-navh"><i></i>{o}</div><ul>{items}</ul></div>'
    return s

def page(title, main, root='', cur=None, extra_head='', side=True, active=''):
    tabs = [('index.html','Fiches'),('outils.html','Calculateurs'),('registre.html','Registre des versions')]
    tb = ''.join(f'<a href="{root}{u}"{" class=on" if active==u else ""}>{l}</a>' for u, l in tabs)
    sidebar = f'<aside class="w-side" id="w-side"><div class="w-sidein"><div class="w-sidetabs">{tb}</div>{nav(cur, root)}</div></aside>'
    return f'''<!DOCTYPE html><html lang="fr" data-root="{root}"><head><meta name="theme-color" content="#1d2430"><link rel="manifest" href="{root}manifest.webmanifest"><link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Classeur radio"><meta name="apple-mobile-web-app-status-bar-style" content="black"><script>document.documentElement.dataset.theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'</script><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22%3E%3Crect x=%223%22 y=%223%22 width=%2218%22 height=%2218%22 rx=%224%22 fill=%22%231d2430%22/%3E%3C/svg%3E"><link rel="stylesheet" href="{root}assets/site.css">{extra_head}</head>
<body class="{'w-hasside' if side else ''}"><header class="w-top"><div class="w-topin">
<button class="w-burger" aria-label="Menu et liste des fiches" aria-controls="w-side" aria-expanded="false"><span></span><span></span><span></span></button>
<a class="w-brand" href="{root}index.html" aria-label="Accueil du classeur"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8 3v18M12 8h5M12 12h5M12 16h3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><span>Classeur radiologie</span></a>
<nav class="w-tabs" aria-label="Sections">{tb}</nav>
<button class="w-theme" type="button" aria-label="Changer de thème" title="Mode clair ou sombre (suit le réglage de l'appareil à l'ouverture)"></button><form class="w-search" action="{root}index.html" role="search"><input type="search" name="q" placeholder="Rechercher une fiche, un score, un signe…" aria-label="Rechercher"></form>
</div></header>
<div class="w-shell">{sidebar}<main class="w-main" id="contenu">{main}</main></div>
<footer class="w-foot"><div>Aide-mémoire pour radiologues et internes. Ne remplace ni les recommandations originales, ni la discussion multidisciplinaire, ni le jugement clinique. Schémas simplifiés, non à l'échelle ; les images de référence sont consultables via les liens (Radiopaedia, sociétés savantes). Dernière vérification : 29 octobre 2026. <span id="w-offline" hidden>· Consultable hors ligne sur cet appareil après une première visite.</span></div></footer>
<script src="{root}assets/app.js"></script></body></html>'''

CODES = {m['code'] for m in fiches}
index_data = []
for i, m in enumerate(fiches):
    code = m['code']
    if code == 'FO-01':
        st1, b1 = parts(f'{S}/FO-01.html'); st2, b2 = parts(f'{S}/FO-01X.html')
        css = scope_css(st1, '.fx1') + '\n' + scope_css(st2, '.fx2')
        b1 = clean(b1); b2 = clean(b2)
        # pied de page unique : celui de la partie atlas
        b1 = re.sub(r'<div class="foot">.*?</div>\s*$', '', b1.strip(), flags=re.S)
        content = f'<div class="fiche fx1">{b1}</div><div class="fiche fx2" style="--oc:#0f6e6e;--ol:#eef6f6">{b2}</div>'
        srcs = []
    else:
        st, b = parts(f'{S}/{code}.html')
        css = scope_css(st, '.fx1')
        b = clean(b)
        if code == 'NE-01':
            b = b.replace('{{SVG:aspects.svg}}', '')
        content = f'<div class="fiche fx1" style="--oc:{m["oc"]};--ol:{m.get("ol","#f3f5f8")}">{b}</div>'
    content = xlink(content, code)
    prev = fiches[i-1] if i > 0 else None; nxt = fiches[i+1] if i < len(fiches)-1 else None
    pn = '<nav class="w-pn" aria-label="Fiche précédente ou suivante">' + (f'<a href="{prev["code"]}.html"><small>Précédente</small>{prev["code"]} · {html.escape(html.unescape(prev["plain"]))}</a>' if prev else '<span></span>') + (f'<a class="nx" href="{nxt["code"]}.html"><small>Suivante</small>{nxt["code"]} · {html.escape(html.unescape(nxt["plain"]))}</a>' if nxt else '<span></span>') + '</nav>'
    tools = {'NE-01':'aspects','FO-01':'lirads','CO-01':'eutirads','OS-01':'bonerads','TH-01':'fleischner','TH-02':'lungrads','CV-01':'cadrads','RS-01':'bosniak','PE-01':'pirads'}
    tl = f'<a class="w-btn ghost" href="../outils.html#{tools[code]}">Calculateur interactif</a>' if code in tools else ''
    hdr = f'''<div class="w-fh" style="--oc:{m['oc']}"><div><span class="w-pill">{m['organe']} · {code}</span><h1>{m['title']}</h1><p>{m['ref']} · {m['sub']}</p></div>
<div class="w-actions">{tl}<a class="w-btn" href="../pdf/{code}.pdf" download>Télécharger le PDF</a><button class="w-btn ghost" onclick="window.print()">Imprimer</button></div></div>'''
    main = hdr + content + pn
    html_ = page(f'{code} – {html.unescape(m["plain"])} · Classeur radiologie', main, '../', code, f'<style>{css}</style>')
    open(f'{OUT}/f/{code}.html', 'w').write(html_)
    index_data.append({'c': code, 'o': m['organe'], 'oc': m['oc'], 't': html.unescape(m['plain']), 'r': m['ref'], 's': m['sub'],
                       'x': text_of(content)[:6000]})

# ---------- accueil ----------
cards = ''
for o in order:
    fs = [d for d in index_data if d['o'] == o]
    cs = ''.join(f'<a class="w-card" href="f/{d["c"]}.html" data-code="{d["c"]}"><span class="w-code">{d["c"]}</span><b>{html.escape(d["t"])}</b><small>{html.escape(d["r"])}</small></a>' for d in fs)
    cards += f'<section class="w-org" style="--oc:{ocol[o]}" data-org="{o}"><div class="w-orgh"><h2>{o}</h2><p>{desc[o]}</p></div><div class="w-cards">{cs}</div></section>'
home = f'''<section class="w-hero"><div><h1>Fiches d'aide à la lecture en radiologie</h1>
<p>{len(fiches)} fiches classées par organe, alignées sur les recommandations et classifications en vigueur en octobre 2026 : critères, seuils, catégories et conduites à tenir, avec schémas et liens vers les aspects d'imagerie attendus.</p>
<div class="w-actions"><a class="w-btn" href="pdf/Classeur-fiches-radiologie.pdf" download>Classeur complet (PDF)</a><a class="w-btn ghost" href="pdf/Fiches-radiologie-par-organe.zip" download>PDF séparés (zip)</a><a class="w-btn ghost" href="outils.html">Calculateurs</a></div></div>
<div class="w-stats"><div><b>{len(fiches)}</b><span>fiches</span></div><div><b>12</b><span>organes</span></div><div><b>11</b><span>calculateurs</span></div></div></section>
<div class="w-filter"><input id="q" type="search" placeholder="Filtrer : PI-RADS, wash-out, Bosniak, embolie…" aria-label="Filtrer les fiches"><div class="w-chips" id="chips"><button class="on" data-o="">Tous</button>{''.join(f'<button data-o="{o}" style="--oc:{ocol[o]}">{o}</button>' for o in order)}</div></div>
<div id="results" class="w-results" hidden></div>
<div id="orgs">{cards}</div>
<script>window.IDX={json.dumps(index_data, ensure_ascii=False)};</script>'''
open(f'{OUT}/index.html', 'w').write(page("Classeur – Fiches d'aide à la lecture en radiologie", home, '', None, '', False, 'index.html'))

# ---------- registre ----------
rows = ''.join(f'<tr><td><a class="w-code" style="--oc:{d["oc"]}" href="f/{d["c"]}.html">{d["c"]}</a></td><td>{html.escape(d["t"])}</td><td>{veille.get(d["c"],("",""))[0]}</td><td class="nw">29/10/2026</td><td class="{"mute" if veille.get(d["c"],("","—"))[1]=="—" else "watch"}">{veille.get(d["c"],("","—"))[1]}</td></tr>' for d in index_data)
reg = f'''<div class="w-fh" style="--oc:#1d2430"><div><span class="w-pill">Veille</span><h1>Registre des versions</h1><p>Référence utilisée par fiche et mises à jour attendues. Vérification trimestrielle programmée.</p></div></div>
<div class="w-tablewrap"><table class="w-table"><thead><tr><th>Code</th><th>Fiche</th><th>Référence en vigueur</th><th>Vérifiée le</th><th>À surveiller</th></tr></thead><tbody>{rows}</tbody></table></div>'''
open(f'{OUT}/registre.html', 'w').write(page('Registre des versions · Classeur radiologie', reg, '', None, '', False, 'registre.html'))

# ---------- outils ----------
tools_html = open(f'{W}/outils_body.html').read().replace('{{ASPECTS_SVG}}', open(f'{S}/gen/aspects_i.svg').read())
open(f'{OUT}/outils.html', 'w').write(page('Calculateurs · Classeur radiologie', tools_html, '', None, '', False, 'outils.html'))
files = []
for dp, dn, fn in os.walk(OUT):
    for x in fn:
        r = os.path.relpath(os.path.join(dp, x), OUT)
        if r.endswith('.zip') or r == 'pdf/Classeur-fiches-radiologie.pdf' or r.startswith('.git'): continue
        files.append(r)
files.append('')
import hashlib
ver = hashlib.md5(''.join(sorted(open(os.path.join(OUT, f), 'rb').read().hex()[:64] + f for f in files if f)).encode()).hexdigest()[:10]
open(f'{OUT}/sw.js', 'w').write(open(f'{W}/sw_template.js').read().replace('__VER__', ver).replace('__FILES__', json.dumps(files)))
open(f'{OUT}/manifest.webmanifest', 'w').write(json.dumps({"name": "Classeur de fiches radiologie", "short_name": "Classeur radio", "lang": "fr", "start_url": "index.html", "display": "standalone", "background_color": "#f4f5f7", "theme_color": "#1d2430", "id": "classeur-radiologie", "scope": "./", "orientation": "any", "description": "Fiches d'aide à la lecture en radiologie classées par organe, avec calculateurs", "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"}, {"src": "assets/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}, {"src": "assets/icon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False))
open(f'{OUT}/assets/icon.svg', 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="5" fill="#1d2430"/><rect x="5" y="5" width="14" height="14" rx="3" fill="none" stroke="#fff" stroke-width="1.6"/><path d="M9 5v14M12 9h4M12 12h4M12 15h2.5" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/></svg>')
print('ok', len(index_data), 'fiches', len(files), 'fichiers hors ligne')
