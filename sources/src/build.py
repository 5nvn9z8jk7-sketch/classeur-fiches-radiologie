import json, subprocess, sys, os, html, re, segno
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH=os.path.expanduser('~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome')
meta=json.load(open(f'{D}/src/fiches.json'))
sys.path.insert(0,f'{D}/src/gen'); from atlas import A as ATLAS
def head(m,suite=False):
    t=m['title']+(' <span class="mute" style="font-weight:500;font-size:10pt">(suite)</span>' if suite else '')
    return f'''<div class="head"><div class="l"><span class="pill">{m['organe']} · {m.get('disp',m['code'])}</span><h1>{t}</h1></div><div class="meta"><b>{m['ref']}</b><br>{m['sub']}</div></div>'''
def build(m):
    body=open(f"{D}/src/fiches/{m['code']}.html").read()
    if m['code'] in ATLAS and m['code']!='NE-01':
        svg,intro,links=ATLAS[m['code']]
        m['links']=[list(l) for l in links]
        if m.get('atlas_only'):
            body=''
            pre=''
        else:
            pre='{{HEAD2}}'
        body+=pre+('<h2>Atlas visuel</h2><div class="c" style="background:#fff">{{SVG:'+svg+'}}</div>' if svg else '')+(f'<div class="sm mute" style="margin-top:3px">{intro}</div>' if intro else '')+'<h2>Pour aller plus loin · cliquer ou scanner le QR code</h2>{{RESS}}'
    body=body.replace('{{HEAD2}}','<div class="pb"></div>'+head(m,True))
    def qr(u): return segno.make(u,error='m').svg_inline(scale=1.6,border=0,dark='#1d2430')
    if '{{RESS}}' in body:
        cards=''.join(f'''<a class="res" href="{html.escape(u)}"><span class="qr">{qr(u)}</span><span><b>{html.escape(t)}</b><br><span class="sm mute">{html.escape(d)}</span><br><span class="url">{html.escape(u.split("//")[1][:48])}</span></span></a>''' for t,u,d in m.get('links',[]))
        body=body.replace('{{RESS}}',f'<div class="ress">{cards}</div>')
    body=re.sub(r'\{\{SVG:([\w.-]+)\}\}',lambda g:open(f"{D}/src/gen/{g.group(1)}").read(),body)
    src=' · '.join(f'{html.escape(l)} – <a href="{html.escape(u)}">{html.escape(u.split("//")[1][:60])}{"…" if len(u.split("//")[1])>60 else ""}</a>' for l,u in m['sources'])
    doc=f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{m['code']} – {html.unescape(m['plain'])}</title><meta name="author" content="Perplexity Computer"><link rel="stylesheet" href="base.css"><style>:root{{--oc:{m['oc']};--ol:{m['ol']}}}</style></head><body>{head(m)}{body}<div class="foot"><b>Sources :</b> {src}<br>Aide-mémoire pour radiologues et internes · ne remplace pas les recommandations originales ni la discussion multidisciplinaire · mise à jour octobre 2026</div></body></html>'''
    p=f"{D}/src/{m['code']}.html"; open(p,'w').write(doc)
    out=f"{D}/pdf/{m['code']}.pdf"
    subprocess.run([CH,'--headless','--no-sandbox','--disable-gpu','--no-pdf-header-footer',f'--print-to-pdf={out}',p],capture_output=True)
    n=subprocess.run(['pdfinfo',out],capture_output=True,text=True).stdout
    pages=[l for l in n.splitlines() if l.startswith('Pages')][0].split()[-1]
    print(m['code'],'pages',pages,'expected',m.get('pages',1))
codes=sys.argv[1:]
for m in meta:
    if not codes or m['code'] in codes: build(m)
