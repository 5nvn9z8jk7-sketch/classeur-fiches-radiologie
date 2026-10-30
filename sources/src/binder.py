import json, subprocess, os, html, shutil
from pypdf import PdfReader, PdfWriter
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(f'{D}/build',exist_ok=True)
CH=os.path.expanduser('~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome')
import glob as _glob
def _chrome():
    c=[os.environ.get('CHROME')]+_glob.glob(os.path.expanduser('~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome'))+['/usr/bin/chromium','/usr/bin/chromium-browser','/usr/bin/google-chrome','/usr/bin/google-chrome-stable']
    for x in c:
        if x and os.path.exists(x): return x
    raise SystemExit('Chrome/Chromium introuvable (installer playwright ou definir CHROME')
CH=_chrome()
meta=json.load(open(f'{D}/src/fiches.json'))
fo1={"code":"FO-01","organe":"Foie","oc":"#0f6e6e","plain":"LI-RADS CT/IRM – foie cirrhotique","ref":"LI-RADS CT/MRI v2018"}
order=["Transversal","Neuro","ORL","Sein","Thorax","Cœur · vaisseaux","Foie","Pancréas","Tube digestif","Rein · surrénale","Pelvis","Ostéo-articulaire"]
desc={"Transversal":"Sécurité, ganglions et situations communes à toutes les modalités","Neuro":"Encéphale, moelle, perfusion, traumatologie crânienne et cervicale","ORL":"Thyroïde, rocher","Sein":"Mammographie, tomosynthèse, échographie, IRM","Thorax":"Poumon, vaisseaux pulmonaires","Foie":"Foie cirrhotique et foie sain","Rein · surrénale":"Masses kystiques rénales, surrénales","Pelvis":"Prostate, annexes, endométriose","Ostéo-articulaire":"Tumeurs osseuses, traumatologie, rachis, mesures orthopédiques","Cœur · vaisseaux":"Coroscanner","Pancréas":"Lésions kystiques du pancréas","Tube digestif":"Rectum, côlon, appendice, grêle"}
meta=[m for m in meta if not m.get('hidden')]
if os.path.exists(f'{D}/pdf/FO-01X.pdf'):
    if not os.path.exists(f'{D}/pdf/FO-01-base.pdf'): shutil.copy(f'{D}/pdf/FO-01.pdf',f'{D}/pdf/FO-01-base.pdf')
    _w=PdfWriter()
    for _p in (f'{D}/pdf/FO-01-base.pdf',f'{D}/pdf/FO-01X.pdf'):
        for _pg in PdfReader(_p).pages: _w.add_page(_pg)
    _w.write(f'{D}/pdf/FO-01.pdf')
fiches=[m for m in meta]+[fo1]
fiches.sort(key=lambda m:(order.index(m['organe']),m['code']))
pc={m['code']:len(PdfReader(f"{D}/pdf/{m['code']}.pdf").pages) for m in fiches}
# layout: cover(1) + sommaire(1) then per section: divider(1) + fiches
def mkplan(front):
  page=front+1; plan=[]
  for o in order:
    fs=[m for m in fiches if m['organe']==o]
    sec={'o':o,'oc':fs[0]['oc'],'page':page,'fiches':[]}; page+=1
    for m in fs:
        sec['fiches'].append((m,page)); page+=pc[m['code']]
    plan.append(sec)
  return plan,page-1
front=4
plan,total=mkplan(front)
css='<link rel="stylesheet" href="base.css">'
modal={"TR-01":"Scanner · IRM","TR-02":"Toutes","NE-01":"Scanner · IRM","NE-02":"IRM","NE-03":"Scanner","NE-04":"Scanner de perfusion","CO-01":"Écho","SE-01":"Mammo · écho · IRM","TH-01":"Scanner","TH-02":"Scanner faible dose","TH-03":"Angioscanner","FO-01":"Scanner · IRM","FO-02":"Écho · CEUS","FO-03":"IRM · scanner · CEUS","RS-01":"Scanner · IRM","RS-02":"Scanner · IRM","PE-01":"IRM","PE-02":"Écho · IRM","PE-03":"IRM","OS-01":"Radio","OS-02":"Radio","OS-03":"IRM","OS-04":"Télérachis · EOS","OS-05":"Radio · écho · scanner","OS-06":"Pangonogramme · scanner · IRM","OS-07":"Radio","TR-03":"Scanner · IRM","CV-01":"Coroscanner","CV-02":"Scanner (score calcique)","CO-02":"TDM des rochers","PA-01":"IRM · scanner · EE","DI-01":"IRM","DI-02":"Scanner · écho","DI-03":"Écho · scanner · IRM","DI-04":"Scanner"}
cover=f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">{css}<style>
body{{display:flex;flex-direction:column;height:277mm}}
.top{{flex:1;display:flex;flex-direction:column;justify-content:center}}
.big{{font-size:34pt;font-weight:700;letter-spacing:-.02em;line-height:1.05;margin:0}}
.big span{{color:#0f6e6e}}
.lead{{font-size:12pt;color:#5b6573;margin-top:10px;max-width:150mm;line-height:1.45}}
.tabs{{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:22px}}
.tabs div{{border-left:4px solid var(--c);padding:6px 9px;background:#f8f9fb;border-radius:4px;font-weight:600;font-size:10pt}}
.tabs small{{display:block;font-weight:400;color:#5b6573;font-size:7.6pt}}
.bot{{font-size:8pt;color:#7a8492;border-top:0.6px solid #d5dae1;padding-top:6px}}
</style></head><body><div class="top"><div class="pill" style="background:#1d2430">Classeur · imagerie médicale</div>
<p class="big" style="margin-top:10px">Fiches d'aide<br>à la lecture <span>en radiologie</span></p>
<p class="lead">{len(fiches)} fiches classées par organe, chacune regroupant les modalités utiles (radiographie, échographie, mammographie, scanner, IRM), selon les recommandations les plus récentes disponibles en octobre 2026.</p>
<div class="tabs">{''.join(f'<div style="--c:{s["oc"]}">{s["o"]}<small>{len(s["fiches"])} fiche{"s" if len(s["fiches"])>1 else ""}</small></div>' for s in plan)}</div></div>
<div class="bot">Public : radiologues et internes · Aide-mémoire, ne remplace ni les recommandations originales ni la discussion multidisciplinaire · Sources citées en bas de chaque fiche · Version octobre 2026</div></body></html>'''
rows=''
for s in plan:
    rows+=f'<tr class="sec"><td colspan="4" style="color:{s["oc"]};border-bottom:1px solid {s["oc"]}"><b>{s["o"]}</b> <span class="mute" style="font-weight:400">· {desc[s["o"]]}</span></td><td class="pg">{s["page"]}</td></tr>'
    for m,p in s['fiches']:
        rows+=f'<tr><td class="nw"><span class="ch" style="background:{m["oc"]};color:#fff;font-size:7.2pt">{m["code"]}</span></td><td>{html.escape(html.unescape(m["plain"]))}</td><td class="mute">{m["ref"]}</td><td class="mute">{modal[m["code"]]}</td><td class="pg">{p}</td></tr>'
som=f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">{css}<style>.tb td{{padding:1.1px 5px;font-size:7.7pt;line-height:1.18}} .tb tr.sec td{{padding-top:4px;font-size:8.8pt}} .pg{{text-align:right;font-weight:600;width:8%}}</style></head><body>
<div class="head" style="--oc:#1d2430"><div class="l"><span class="pill" style="background:#1d2430">Classeur · sommaire</span><h1>Sommaire</h1></div><div class="meta"><b>{len(fiches)} fiches · {total} pages</b><br>classement par organe · numéros de page du classeur</div></div>
<table class="tb"><tr><th>Code</th><th>Fiche</th><th>Référence</th><th>Modalités</th><th style="text-align:right">Page</th></tr>{rows}</table>
<div class="key sm" style="margin-top:6px;--oc:#1d2430;--ol:#f3f4f6"><b class="t">Mode d'emploi :</b> chaque fiche se lit de haut en bas (critères → catégories → conduite à tenir). Les codes couleur sont communs à tout le classeur : <span class="ch r1">bénin / faible</span> <span class="ch r3">intermédiaire</span> <span class="ch r4">suspect</span> <span class="ch r5">très suspect / urgent</span>. Signets PDF pour aller directement à une fiche ; registre des versions page suivante.</div>
</body></html>'''

veille={
"TR-01":("ESUR CMSC 2025","—"),
"TR-02":("ACR–SPR 2023 · ESUR 2025","—"),
"TR-03":("Node-RADS v1.0 (2021)","—"),
"NE-01":("AHA/ASA 2026 (Stroke, janv. 2026)","Vérifiée le 30/10/2026 : fiche alignée sur le texte final (TNK 0,25 mg/kg, IVT 4,5–9 h sur pénombre, EVT mRS 2, créatinine)"),
"NE-02":("McDonald 2024 (publié en 2025)","—"),
"NE-03":("NICE NG232 (2023)","—"),
"NE-04":("AHA/ASA 2026 · ESO 2021/2023 · ESO-ESMINT","Seuils ISP par défaut ≠ seuils des essais ; recommandations ESO sur la thrombectomie à suivre"),
"CO-01":("ETA 2023 · ACR TI-RADS 2017","Système international I-TIRADS en cours d'élaboration (ACR et sociétés partenaires)"),
"SE-01":("ACR BI-RADS v2025","—"),
"TH-01":("Fleischner 2017","Glossaire Fleischner mis à jour (nouvelle terminologie des nodules) ; recommandations de suivi 2017 inchangées"),
"TH-02":("Lung-RADS v2022","—"),
"TH-03":("ESC/ERS 2019 · AHA/ACC 2026","Mise à jour ESC attendue"),
"CV-01":("CAD-RADS 2.0 (2022)","—"),
"CV-02":("ACC/AHA 2026 · ESC/EAS 2025 · CAC-DRS 2018 · Philips ISP","Mise à jour éventuelle du CAC-DRS (SCCT) ; seuils de volume et de masse non validés ; modèles de rapport ISP à aligner sur les catégories 2026"),
"CO-02":("RPC SFORL imagerie du rocher · ACR AC Hearing loss · SBO 2023","Pas de recommandation radiologique dédiée ; place du comptage photonique et du cone beam à suivre"),
"FO-01":("LI-RADS CT/MRI v2018","Algorithme de réponse au traitement mis à jour en 2024 (hors fiche)"),
"FO-02":("LI-RADS US v2024 · CEUS v2017","—"),
"FO-03":("EASL 2016","—"),
"PA-01":("Kyoto 2024","—"),
"DI-01":("ESGAR 2026 (partie I : bilan initial)","Partie II (réévaluation, préservation d'organe) à ajouter"),
"DI-02":("WSES 2020","—"),
"DI-03":("WSES Jerusalem 2025","Système de gradation WSES 2025 (6 grades) en cours de diffusion"),
"DI-04":("WSES Bologne 2017","Mise à jour WSES à surveiller"),
"RS-01":("Bosniak v2019","—"),
"RS-02":("ESE/ENSAT 2023","—"),
"PE-01":("PI-RADS v2.1 · PI-QUAL v2","Nouvelle version (« PI-RADS Pathway ») annoncée pour 2026"),
"PE-02":("O-RADS US v2022 · O-RADS MRI","Nouvelle version O-RADS attendue"),
"PE-03":("ESUR 2025 · dPEI","—"),
"OS-01":("Bone-RADS v2023","—"),
"OS-02":("Ottawa · Salter-Harris · Garden","—"),
"OS-03":("NASS/ASSR/ASNR v2.0 (2014)","—"),
"OS-04":("SRS-Schwab · SOSORT","—"),
"OS-05":("Coxométrie de Lequesne · Graf","Seuils de l'angle alpha variables selon les équipes"),
"OS-06":("Paley · protocole de Lyon","Seuils TA-GT dépendants de la modalité (scanner ou IRM)"),
"OS-07":("Mesures radiographiques usuelles","—"),
}
vdate={"NE-01":"30/10/2026","CV-02":"30/10/2026","CO-02":"30/10/2026"}
rrows=''.join(f'<tr><td class="nw"><span class="ch" style="background:{m["oc"]};color:#fff;font-size:7.2pt">{m["code"]}</span></td><td>{html.escape(html.unescape(m["plain"]))}</td><td>{veille[m["code"]][0]}</td><td class="nw">{vdate.get(m["code"],"29/10/2026")}</td><td class="mute">{veille[m["code"]][1]}</td></tr>' for s_ in plan for m,_ in s_['fiches'])
registre=f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">{css}<style>.tb td{{font-size:8pt;padding:3px 5px}}</style></head><body>
<div class="head" style="--oc:#1d2430"><div class="l"><span class="pill" style="background:#1d2430">Classeur · veille</span><h1>Registre des versions</h1></div><div class="meta"><b>Dernière vérification : 30 octobre 2026</b><br>référence utilisée par fiche et mises à jour attendues</div></div>
<table class="tb"><tr><th>Code</th><th>Fiche</th><th>Référence en vigueur</th><th>Vérifiée le</th><th>À surveiller</th></tr>{rrows}</table>
<div class="key sm" style="margin-top:8px;--oc:#1d2430;--ol:#f3f4f6"><b class="t">Mise à jour :</b> à chaque nouvelle version d'une recommandation, la fiche concernée est révisée, puis la date de vérification et ce registre sont mis à jour.</div>
</body></html>'''

def div(s):
    items=''.join(f'<div class="it"><span class="ch" style="background:{s["oc"]};color:#fff">{m["code"]}</span> {html.escape(html.unescape(m["plain"]))} <span class="mute">· p. {p}</span></div>' for m,p in s['fiches'])
    return f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">{css}<style>body{{height:277mm;display:flex;flex-direction:column;justify-content:center}} .band{{background:{s["oc"]};color:#fff;border-radius:10px;padding:26px 28px}} .band h1{{font-size:30pt;color:#fff}} .band p{{margin:6px 0 0;font-size:11pt;opacity:.9}} .it{{font-size:11pt;padding:7px 0;border-bottom:0.6px solid #d5dae1}}</style></head><body>
<div class="band"><div style="font-size:8pt;letter-spacing:.1em;text-transform:uppercase;font-weight:700;opacity:.85">Intercalaire</div><h1>{s["o"]}</h1><p>{desc[s["o"]]}</p></div><div style="margin-top:18px">{items}</div></body></html>'''
def pdf(htmlstr,name):
    p=f'{D}/src/_{name}.html'; open(p,'w').write(htmlstr); out=f'{D}/build/_{name}.pdf'
    subprocess.run([CH,'--headless','--no-sandbox','--disable-gpu','--no-pdf-header-footer',f'--print-to-pdf={out}',p],capture_output=True); return out
w=PdfWriter()
def add(path):
    r=PdfReader(path); start=len(w.pages)
    for pg in r.pages: w.add_page(pg)
    return start
add(pdf(cover,'cover')); s0=add(pdf(som,'sommaire')); w.add_outline_item('Sommaire',s0); s1=add(pdf(registre,'registre')); w.add_outline_item('Registre des versions',s1)
print('front pages',len(w.pages),'assumed',front)
for s in plan:
    st=add(pdf(div(s),'div_'+s['o'][:4]))
    par=w.add_outline_item(s['o'],st)
    for m,p in s['fiches']:
        st=add(f"{D}/pdf/{m['code']}.pdf"); w.add_outline_item(f"{m['code']} · {html.unescape(m['plain'])}",st,parent=par)
w.add_metadata({'/Title':"Classeur – Fiches d'aide à la lecture en radiologie (oct. 2026)",'/Author':'Perplexity Computer'})
w.page_mode='/UseOutlines'
out=f'{D}/Classeur-fiches-radiologie.pdf'; w.write(out); print('total',len(w.pages),'expected',total)
# individual folders
z=f'{D}/Fiches-radiologie-par-organe'; shutil.rmtree(z,ignore_errors=True)
for i,s in enumerate(plan):
    d=f'{z}/{i:02d}-{s["o"].replace(" · ","-")}'; os.makedirs(d)
    for m,p in s['fiches']:
        shutil.copy(f"{D}/pdf/{m['code']}.pdf",f"{d}/{m['code']} {html.unescape(m['plain']).replace('/','-')}.pdf")
# relance du build pour le premier deploiement GitHub Pages
