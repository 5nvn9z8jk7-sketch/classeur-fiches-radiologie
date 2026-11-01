(function(){
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
const ROOT=document.documentElement.dataset.root||'';
// stockage local protégé (aperçu en iframe sans origine : repli en mémoire)
// thème : suit le réglage de l'appareil ; le bouton bascule pour la page en cours et se propage par les liens internes (?theme=)
const qp=new URLSearchParams(location.search).get('theme');

// ---------- thème ----------
const tb=$('.w-theme');
function applyTheme(t){document.documentElement.dataset.theme=t; if(tb){tb.setAttribute('aria-label',t==='dark'?'Passer en mode clair':'Passer en mode sombre'); tb.innerHTML=t==='dark'?'<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>':'<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'}}
applyTheme(qp==='dark'||qp==='light'?qp:document.documentElement.dataset.theme||'light');
function propagate(){const t=document.documentElement.dataset.theme, sys=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
 $$('a[href]').forEach(a=>{const h=a.getAttribute('href'); if(/^(https?:|mailto:|#)/.test(h)||/\.(pdf|zip)$/.test(h.split('#')[0].split('?')[0])) return;
  const [base,hash]=h.split('#'); const u=base.split('?')[0]; a.setAttribute('href',u+(t!==sys?'?theme='+t:'')+(hash!==undefined?'#'+hash:''))});
 $$('form.w-search').forEach(f=>{let i=f.querySelector('input[name=theme]'); if(t!==sys){if(!i){i=document.createElement('input');i.type='hidden';i.name='theme';f.appendChild(i)} i.value=t} else if(i) i.remove()})}
propagate();
if(tb) tb.addEventListener('click',()=>{applyTheme(document.documentElement.dataset.theme==='dark'?'light':'dark');propagate()});

// ---------- tiroir mobile ----------
const bg=$('.w-burger');
if(bg){const close=()=>{document.body.classList.remove('w-open');bg.setAttribute('aria-expanded','false')};
 bg.addEventListener('click',()=>{const o=document.body.classList.toggle('w-open');bg.setAttribute('aria-expanded',o)});
 document.addEventListener('keydown',e=>{if(e.key==='Escape')close()}); $('.w-main').addEventListener('click',close);}
$$('a[href^="http"]').forEach(a=>{a.target='_blank';a.rel='noopener'});
const cur=$('.w-navg a[aria-current]'); if(cur) cur.scrollIntoView({block:'center'});

// ---------- accueil : filtre et recherche ----------
if(window.IDX){
 const q=$('#q'), res=$('#results'), orgs=$('#orgs'); let org='';
 const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const IDX=window.IDX.map(d=>({...d,n:norm(d.c+' '+d.t+' '+d.r+' '+d.s+' '+d.o+' '+d.x)}));
 const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
 function snip(d,terms){const t=d.x, nt=norm(t); let i=-1; for(const w of terms){i=nt.indexOf(w); if(i>=0)break}
  if(i<0) return esc(d.s); const a=Math.max(0,i-70); let h=esc((a?'…':'')+t.slice(a,i+150)+'…');
  for(const w of terms){ if(w.length<2) continue; const re=new RegExp('('+w.split('').map(c=>c.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('[\\u0300-\\u036f]*')+')','gi'); h=h.normalize('NFD').replace(re,'<mark>$1</mark>').normalize('NFC')} return h}
 function run(){const v=q.value.trim(), terms=norm(v).split(/\s+/).filter(Boolean);
  $$('#chips button').forEach(b=>b.classList.toggle('on',b.dataset.o===org));
  if(!terms.length){res.hidden=true; orgs.hidden=false; $$('.w-org').forEach(s=>s.hidden=!!org&&s.dataset.org!==org); return}
  const hits=IDX.filter(d=>(!org||d.o===org)&&terms.every(w=>d.n.includes(w)));
  orgs.hidden=true; res.hidden=false;
  res.innerHTML=hits.length?hits.map(d=>`<a class="w-res" href="f/${d.c}.html" style="--oc:${d.oc}"><span class="w-code">${d.c}</span><b>${esc(d.t)}</b><p>${snip(d,terms)}</p></a>`).join(''):`<div class="w-empty">Aucune fiche ne contient « ${esc(v)} ». Essayer un terme plus court ou une autre orthographe.</div>`;}
 q.addEventListener('input',run);
 $$('#chips button').forEach(b=>b.addEventListener('click',()=>{org=b.dataset.o;run()}));
 const p=new URLSearchParams(location.search).get('q'); if(p){q.value=p; const t=$('.w-search input'); if(t)t.value=p}
 run();
}

// ---------- hors ligne ----------
if('serviceWorker' in navigator){try{navigator.serviceWorker.register(ROOT+'sw.js').then(()=>{const o=$('#w-offline'); if(o) o.hidden=false}).catch(()=>{})}catch(e){}}

// ---------- calculateurs : rendu commun ----------
function copyText(t,btn){const done=()=>{const o=btn.textContent;btn.textContent='Copié';setTimeout(()=>btn.textContent=o,1500)};
 const fb=()=>{const ta=btn.parentElement.querySelector('textarea'); ta.focus(); ta.select(); try{document.execCommand('copy');done()}catch(e){btn.textContent='Sélectionné : Ctrl+C'}};
 try{navigator.clipboard.writeText(t).then(done,fb)}catch(e){fb()}}
function render(id,r){const box=$('#res-'+id); if(!box) return;
 box.innerHTML=`<div class="k">${r.k||'Résultat'}</div>${r.v!==undefined?`<div class="v">${r.v}</div>`:''}<div class="cat ${r.cls}">${r.cat}</div>${r.why?`<p class="mute">${r.why}</p>`:''}${r.cdt?`<p><b>Conduite :</b> ${r.cdt}</p>`:''}
 <div class="t-phrase"><label for="ph-${id}">Phrase de compte rendu</label><textarea id="ph-${id}" rows="3" readonly>${r.ph}</textarea><button type="button" class="w-btn ghost">Copier</button></div>`;
 const b=box.querySelector('button'); b.addEventListener('click',()=>copyText(box.querySelector('textarea').value,b));}
function bind(id,fn){const f=$('#f-'+id); if(!f) return; const go=()=>render(id,fn(new FormData(f),f)); f.addEventListener('input',go); f.addEventListener('change',go); go();}
const n=(x)=>String(x).replace('.',',');
const dis=(sel,off)=>{$$(sel).forEach(el=>{el.style.opacity=off?.4:1; $$('input',el).forEach(i=>i.disabled=off)})};

// ---------- ASPECTS ----------
const asp=$('#asp-svg');
if(asp){const R=['C','L','IC','I','M1','M2','M3','M4','M5','M6'], off=new Set(), btns=$('#asp-btns');
 const nm={C:'noyau caudé',L:'noyau lenticulaire',IC:'capsule interne',I:'ruban insulaire',M1:'M1',M2:'M2',M3:'M3',M4:'M4',M5:'M5',M6:'M6'};
 btns.innerHTML=R.map(r=>`<button type="button" data-r="${r}" aria-pressed="false">${r}</button>`).join('');
 function draw(){const s=10-off.size, side=($('#asp-side input:checked')||{}).value||'droit';
  $$('.rg',asp).forEach(e=>e.classList.toggle('off',off.has(e.dataset.r)));
  $$('button',btns).forEach(b=>b.setAttribute('aria-pressed',off.has(b.dataset.r)));
  const [c,t]=s>=6?['c2','6–10 · infarctus constitué limité']:s>=3?['c4','3–5 · « large core »']:['c5','0–2 · infarctus étendu'];
  const cdt=s>=6?'Thrombectomie recommandée si occlusion ACI ou M1 et autres critères réunis (0–24 h, NIHSS ≥ 6, mRS 0–1).':s>=3?'Thrombectomie recommandée dans des cas sélectionnés (0–6 h ; 6–24 h si âge &lt; 80 ans et pas d\'effet de masse significatif).':'Thrombectomie seulement dans des cas très sélectionnés (0–6 h).';
  const list=R.filter(r=>off.has(r)).map(r=>nm[r]);
  render('aspects',{k:'ASPECTS',v:s,cls:c,cat:t,why:list.length?'Régions atteintes : '+R.filter(r=>off.has(r)).join(', ')+'.':'Aucune région atteinte sélectionnée.',cdt:cdt+' Voir NE-01.',
   ph:`ASPECTS ${s}/10 (hémisphère ${side})`+(list.length?`, signes précoces d'ischémie : ${list.join(', ')}.`:', sans signe précoce d\'ischémie.')});}
 function tog(r){off.has(r)?off.delete(r):off.add(r);draw()}
 $$('.rg',asp).forEach(e=>{e.setAttribute('tabindex','0');e.setAttribute('role','button');e.setAttribute('aria-label','Région '+e.dataset.r);
  e.addEventListener('click',()=>tog(e.dataset.r)); e.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();tog(e.dataset.r)}})});
 btns.addEventListener('click',e=>{const b=e.target.closest('button');if(b)tog(b.dataset.r)});
 $('#asp-side').addEventListener('change',draw); draw();}

// ---------- PC-ASPECTS ----------
bind('pcaspects',(f,form)=>{const ch=$$('input[name=r]:checked',form); const s=10-ch.reduce((a,i)=>a+ +i.value,0);
 const ok=s>=6; return {k:'PC-ASPECTS',v:s,cls:ok?'c2':'c5',cat:ok?'≥ 6':'&lt; 6',why:ch.length?'Régions atteintes : '+ch.map(i=>i.dataset.n).join(', ')+'.':'Aucune région atteinte.',
  cdt:'Occlusion du tronc basilaire : thrombectomie recommandée jusqu\'à 24 h si mRS 0–1, NIHSS ≥ 10 et PC-ASPECTS ≥ 6 (NE-01).',
  ph:`PC-ASPECTS ${s}/10`+(ch.length?` (atteinte : ${ch.map(i=>i.dataset.n).join(', ')}).`:', sans lésion ischémique visible.')}});

// ---------- EU-TIRADS ----------
bind('eutirads',(f,form)=>{const ben=f.get('ben')==='1'; dis('.eu-rest',ben); const mm=+f.get('size')||0;
 const hr=$$('input[name=hr]:checked',form).map(i=>i.dataset.n); let c,cl,lab,thr,risk;
 if(ben){c=2;cl='c1';lab='bénin';thr=null;risk='≈ 0 %'} else if(hr.length){c=5;cl='c5';lab='haut risque';thr=10;risk='26–87 %'} else if(f.get('echo')==='hypo'){c=4;cl='c4';lab='risque intermédiaire';thr=15;risk='6–17 %'} else {c=3;cl='c3';lab='faible risque';thr=20;risk='2–4 %'}
 let cdt; if(thr===null) cdt='Pas de cytoponction (sauf à visée évacuatrice).'; else if(mm>thr) cdt=`Cytoponction recommandée (&gt; ${thr} mm).`; else if(c===5&&mm>=5) cdt='EU-TIRADS 5 de 5–10 mm : surveillance active ou cytoponction selon le contexte (localisation, patient).'; else cdt=`Pas de cytoponction (seuil &gt; ${thr} mm) ; surveillance selon le contexte.`;
 cdt+=' Toujours cytoponctionner une adénopathie suspecte.';
 return {k:'EU-TIRADS',v:c,cls:cl,cat:`EU-TIRADS ${c} · ${lab}`,why:`Risque de malignité : ${risk}.`+(hr.length?` Signe(s) de haut risque : ${hr.join(', ')}.`:''),cdt,
  ph:`Nodule thyroïdien de ${mm} mm, ${ben?'d\'aspect bénin (kyste pur ou spongiforme)':(hr.length?hr.join(', '):(f.get('echo')==='hypo'?'modérément hypoéchogène, sans signe de haut risque':'iso- ou hyperéchogène, ovale, à contours réguliers, sans signe de haut risque'))}, classé EU-TIRADS ${c}.`}});

// ---------- ACR TI-RADS ----------
bind('tirads',(f)=>{const comp=f.get('comp'), benign=comp==='0c'||comp==='0s'; dis('#ti-rest',benign);
 let p=0; if(!benign){p=+comp+ +f.get('echo')+ +f.get('shape')+ +f.get('marg')+(f.get('f1')?1:0)+(f.get('f2')?2:0)+(f.get('f3')?3:0)}
 const mm=+f.get('size')||0, cm=mm/10; let tr,cl,lab,fna=null,fu=null,fuT='';
 if(p===0){tr='TR1';cl='c1';lab='bénin'} else if(p<=2){tr='TR2';cl='c2';lab='non suspect'}
 else if(p===3){tr='TR3';cl='c3';lab='peu suspect';fna=2.5;fu=1.5;fuT='à 1, 3 et 5 ans'}
 else if(p<=6){tr='TR4';cl='c4';lab='modérément suspect';fna=1.5;fu=1.0;fuT='à 1, 2, 3 et 5 ans'}
 else{tr='TR5';cl='c5';lab='très suspect';fna=1.0;fu=0.5;fuT='tous les ans pendant 5 ans'}
 let c; if(fna===null)c='Ni cytoponction ni surveillance.'; else if(cm>=fna)c=`Cytoponction recommandée (taille ≥ ${n(fna)} cm).`; else if(cm>=fu)c=`Surveillance échographique ${fuT} (taille ≥ ${n(fu)} cm et &lt; ${n(fna)} cm).`; else c=`Ni cytoponction ni surveillance (taille &lt; ${n(fu)} cm).`;
 if(f.get('marg')==='3'&&!benign) c+=' Extension extrathyroïdienne franche : considérer comme malin jusqu\'à preuve du contraire.';
 return {k:'Total',v:p+' pt'+(p>1?'s':''),cls:cl,cat:`${tr} · ${lab}`,why:benign?'Kystique ou spongiforme : TR1 d\'emblée.':'',cdt:c,ph:`Nodule thyroïdien de ${mm} mm, ACR TI-RADS ${tr} (${p} point${p>1?'s':''}).`}});

// ---------- Fleischner ----------
bind('fleischner',(f)=>{const t=f.get('type'), multi=f.get('nb')==='n', hi=f.get('risk')==='haut', s=+f.get('size')||0, so=+f.get('solid')||0;
 dis('.fl-solid',t!=='solide'); dis('.fl-ps',t!=='ps'); let cdt,cls,cat;
 if(t==='solide'){ if(s<6){cat='&lt; 6 mm';cls='c1';cdt=hi?'Scanner à 12 mois optionnel.':'Pas de suivi systématique.'}
  else if(s<=8){cat='6–8 mm';cls='c3';cdt=multi?(hi?'Scanner à 3–6 mois, puis à 18–24 mois.':'Scanner à 3–6 mois, puis envisager à 18–24 mois.'):(hi?'Scanner à 6–12 mois, puis à 18–24 mois.':'Scanner à 6–12 mois, puis envisager à 18–24 mois.')}
  else {cat='&gt; 8 mm';cls='c4';cdt=multi?'Scanner à 3–6 mois, puis envisager à 18–24 mois.':'Envisager un scanner à 3 mois, une TEP-TDM ou un prélèvement.'} }
 else if(multi){ if(s<6){cat='subsolides multiples &lt; 6 mm';cls='c2';cdt='Scanner à 3–6 mois ; si stable, envisager à 2 et 4 ans.'} else {cat='subsolides multiples ≥ 6 mm';cls='c3';cdt='Scanner à 3–6 mois, puis selon le nodule le plus suspect.'} }
 else if(t==='vd'){ if(s<6){cat='verre dépoli &lt; 6 mm';cls='c1';cdt='Pas de suivi systématique.'} else {cat='verre dépoli ≥ 6 mm';cls='c3';cdt='Scanner à 6–12 mois ; si persistant, scanner tous les 2 ans jusqu\'à 5 ans.'} }
 else { if(s<6){cat='partiellement solide &lt; 6 mm';cls='c1';cdt='Pas de suivi systématique.'} else if(so>=6){cat='composante solide ≥ 6 mm';cls='c5';cdt='Scanner à 3–6 mois ; composante solide ≥ 6 mm : très suspect, discuter un prélèvement ou une exérèse (RCP).'} else {cat='partiellement solide ≥ 6 mm';cls='c3';cdt='Scanner à 3–6 mois ; si persistant et composante solide &lt; 6 mm, scanner annuel pendant 5 ans.'} }
 const ty={solide:'solide',vd:'en verre dépoli pur',ps:'partiellement solide'}[t];
 return {k:'Fleischner 2017',cls,cat,why:`Nodule ${ty}, ${multi?'multiples':'unique'}${t==='solide'?', patient à '+(hi?'haut':'bas')+' risque':''}.`,cdt,
  ph:`${multi?'Nodules':'Nodule'} pulmonaire${multi?'s':''} ${ty}${multi?'s':''} de ${n(s)} mm${t==='ps'?` (composante solide ${n(so)} mm)`:''}. Selon Fleischner 2017 : ${cdt.replace(/&lt;/g,'<').replace(/&gt;/g,'>').toLowerCase()}`}});

// ---------- Lung-RADS ----------
const LRC={'0':['c0','Comparaison avec un examen antérieur ou scanner à 1–3 mois.'],'1':['c1','Scanner faible dose à 12 mois.'],'2':['c2','Scanner faible dose à 12 mois.'],'3':['c3','Scanner faible dose à 6 mois.'],'4A':['c4','Scanner à 3 mois ; TEP-TDM si composante solide ≥ 8 mm.'],'4B':['c5','Scanner diagnostique ± injection, TEP-TDM, prélèvement ; avis RCP.'],'4X':['c5','Comme 4B : scanner diagnostique, TEP-TDM, prélèvement ; avis RCP.']};
bind('lungrads',(f)=>{const pre=f.get('pre'); dis('#lr-grid',pre!=='none'); const t=f.get('type'); dis('.lr-ps',t!=='ps');
 const st=f.get('st'), s=+f.get('size')||0, so=+f.get('solid')||0; let c, why='';
 if(pre==='0'){c='0';why='Examen incomplet ou aspect infectieux ou inflammatoire.'}
 else if(pre==='1'){c='1';why='Pas de nodule, ou nodule à calcification bénigne ou graisseux.'}
 else if(pre==='jp'){c='2';why='Nodule juxtapleural solide typique ≤ 10 mm.'}
 else if(t==='s'){ if(st==='init') c=s<6?'2':s<8?'3':s<15?'4A':'4B'; else if(st==='new') c=s<4?'2':s<6?'3':s<8?'4A':'4B'; else c=s<8?'4A':'4B';}
 else if(t==='ps'){ if(st==='init') c=s<6?'2':so<6?'3':so<8?'4A':'4B'; else if(st==='new') c=s<6?'3':so<4?'4A':'4B'; else c=so<4?'4A':'4B';}
 else { c=s<30?'2':(st==='grow'?'2':'3'); if(st==='grow') why='Verre dépoli : croissance lente ou stabilité → 2.';}
 if(f.get('x')&&pre==='none'&&(c==='3'||c.startsWith('4'))){c='4X';why=(why+' Signe suspect supplémentaire.').trim()}
 const S=f.get('s')?'S':''; const ty={s:'solide',ps:'partiellement solide',vd:'en verre dépoli'}[t]; const sta={init:'',new:'nouveau, ',grow:'en croissance, '}[st];
 const [cl,cdt]=LRC[c];
 return {k:'Lung-RADS v2022',cls:cl,cat:`Lung-RADS ${c}${S?' S':''}`,why,cdt,
  ph:pre==='none'?`Nodule ${ty}, ${sta}de ${n(s.toFixed(1))} mm de diamètre moyen${t==='ps'?` (composante solide ${n(so.toFixed(1))} mm)`:''} : Lung-RADS ${c}${S?' S':''}. ${cdt}`:`Lung-RADS ${c}${S?' S':''}. ${cdt}`}});

// ---------- CAD-RADS ----------
bind('cadrads',(f,form)=>{let c=f.get('st'); const b=f.get('b'); if(c==='4') c=b?'4B':'4A'; else if(b&&(c==='3'||c==='2')) c='4B';
 const mods=[]; if(f.get('mN'))mods.push('N'); const hrp=$$('input[name=hrp]:checked',form).length>=2; if(hrp)mods.push('HRP'); if(f.get('isch'))mods.push(f.get('isch')); if(f.get('mS'))mods.push('S'); if(f.get('mG'))mods.push('G'); if(f.get('mE'))mods.push('E');
 const cac=+f.get('cac'); let P=''; if(c!=='0'&&cac>0) P=cac<=100?'P1':cac<=300?'P2':cac<1000?'P3':'P4';
 const code='CAD-RADS '+c+(mods.length?'/'+mods.join('/'):'')+(P?'/'+P:'');
 const M={'0':['c1','Pas d\'autre exploration cardiaque.'],'1':['c1','Pas d\'autre exploration ; prévention selon la charge plaquaire.'],'2':['c2','Pas d\'autre exploration ; prévention.'],'3':['c3','Envisager une évaluation fonctionnelle (FFR-CT, perfusion CT, échographie de stress, scintigraphie, TEP, IRM, FFR invasive).'],'4A':['c4','Coronarographie ou évaluation fonctionnelle ; coronarographie favorisée si &gt; 90 %, HRP, ischémie ou symptômes persistants.'],'4B':['c5','Coronarographie recommandée.'],'5':['c5','Coronarographie, évaluation fonctionnelle ou de viabilité.']};
 const [cl,cdt]=M[c];
 return {k:'Coroscanner',cls:cl,cat:code,why:(hrp?'Plaque à haut risque : au moins 2 signes. ':'')+(P?`Score calcique ${cac} → ${P}.`:''),cdt,ph:`Coroscanner : ${code}. ${cdt.replace(/&gt;/g,'>')}`}});

// ---------- LI-RADS ----------
const LIC={NC:['c0','LR-NC','Non catégorisable','Nouvelle imagerie (même technique ou autre) dans un délai ≤ 3 mois.'],
 TIV:['ct','LR-TIV','Tumeur dans une veine','Discussion multidisciplinaire. En cas de doute, ne pas classer TIV.'],
 '1':['c1','LR-1','Certainement bénigne','Poursuite de la surveillance habituelle à 6 mois.'],
 '2':['c2','LR-2','Probablement bénigne','Surveillance ; contrôle envisageable dans ≤ 6 mois.'],
 '3':['c3','LR-3','Probabilité intermédiaire','Contrôle par imagerie multiphasique dans 3 à 6 mois.'],
 '4':['c4','LR-4','Probablement un CHC','Discussion multidisciplinaire : contrôle rapproché ≤ 3 mois, autre technique d\'imagerie ou biopsie.'],
 '5':['c5','LR-5','CHC certain','Diagnostic de CHC sans biopsie ; discussion multidisciplinaire pour le traitement.'],
 M:['cm','LR-M','Maligne, pas forcément un CHC','Discussion multidisciplinaire ; biopsie souvent nécessaire.']};
bind('lirads',(f)=>{const pre=f.get('pre'); dis('#li-grid',pre!=='none'); let k=pre, why='', feats='';
 if(pre==='none'){const a=f.get('aphe')==='1', sz=f.get('sz'), wo=!!f.get('wo'), cap=!!f.get('cap'), gr=!!f.get('gr'), nn=wo+cap+gr; let b;
  if(!a){b=sz==='l'?(nn===0?3:4):(nn<=1?3:4)} else if(sz==='s'){b=nn===0?3:4} else if(sz==='m'){b=nn===0?3:nn>=2?5:((wo||gr)?5:4)} else{b=nn===0?4:5}
  const szT={s:'< 10 mm',m:'10–19 mm',l:'≥ 20 mm'}[sz];
  why=`Grille : ${a?'APHE présent':'pas d\'APHE'}, ${szT}, ${nn} critère${nn>1?'s':''} majeur${nn>1?'s':''} en plus → LR-${b}.`;
  const fl=[a?'APHE non périphérique':'sans APHE']; if(wo)fl.push('wash-out non périphérique'); if(cap)fl.push('capsule rehaussée'); if(gr)fl.push('croissance seuil'); feats=`Observation de ${szT}, ${fl.join(', ')}`;
  const am=!!f.get('am'), ab=!!f.get('ab'); let c=b;
  if(am&&!ab&&b<4){c=b+1; why+=' Critère accessoire de malignité : +1 catégorie (plafond LR-4).'}
  else if(am&&!ab&&b>=4){why+=' Critère accessoire de malignité : pas de passage en LR-5 par les critères accessoires.'}
  else if(ab&&!am){c=Math.max(1,b-1); why+=' Critère accessoire de bénignité : −1 catégorie.'}
  else if(ab&&am){why+=' Critères accessoires dans les deux sens : pas d\'ajustement.'}
  k=String(c);}
 const [cl,code,lab,cdt]=LIC[k];
 return {k:'Catégorie',cls:cl,cat:`${code} · ${lab}`,why,cdt,ph:(feats?feats.replace('<','&lt;')+' : ':'')+`${code} (${lab.toLowerCase()}, LI-RADS CT/IRM v2018).`}});

// ---------- Bosniak ----------
bind('bosniak',(f)=>{const c=f.get('c'); const M={I:['c1','I','≈ 0 %','Aucune surveillance.'],II:['c1','II','≈ 0 %','Aucune surveillance.'],IIF:['c3','IIF','≈ 5–10 %','Contrôle à 6 et 12 mois, puis annuel pendant 5 ans.'],IIFm:['c3','IIF','≈ 5–10 %','Contrôle à 6 et 12 mois, puis annuel pendant 5 ans.'],III:['c4','III','≈ 50 %','Surveillance active ou chirurgie / ablation (RCP).'],IV:['c5','IV','≈ 90 %','Chirurgie ou ablation.']}[c];
 return {k:'Bosniak v2019',v:M[1],cls:M[0],cat:`Classe ${M[1]} · malignité ${M[2]}`,cdt:M[3],ph:`Masse kystique rénale classée Bosniak ${M[1]} (v2019). ${M[3]}`}});

// ---------- PI-RADS ----------
bind('pirads',(f)=>{const z=f.get('z'), t2=+f.get('t2'), dw=+f.get('dw'), dce=f.get('dce'); dis('.pi-dce',z==='ZT'); let s, why;
 if(z==='ZP'){ s=dw; why=`Zone périphérique : diffusion ${dw} dominante.`; if(dw===3&&dce==='+'){s=4; why+=' DCE positif : 3 → 4.'} if(dw===3&&dce==='x') why+=' Biparamétrique : pas de reclassement possible par le DCE.'}
 else { s=t2; why=`Zone de transition : T2 ${t2} dominant.`; if(t2===2&&dw>=4){s=3; why+=' Diffusion ≥ 4 : 2 → 3.'} if(t2===3&&dw===5){s=4; why+=' Diffusion 5 : 3 → 4.'} }
 const L={1:['c1','très peu probable'],2:['c2','peu probable'],3:['c3','équivoque'],4:['c4','probable'],5:['c5','très probable']}[s];
 const cdt=s>=4?'Biopsie ciblée en général recommandée.':s===3?'Biopsie selon la densité de PSA et le contexte clinique.':'Pas de biopsie ciblée sur cette lésion.';
 return {k:'PI-RADS v2.1',v:s,cls:L[0],cat:`PI-RADS ${s} · cancer significatif ${L[1]}`,why,cdt,ph:`Lésion de la ${z==='ZP'?'zone périphérique':'zone de transition'} : T2 ${t2}, diffusion ${dw}${z==='ZP'?', DCE '+({'+':'positif','-':'négatif','x':'non réalisé'})[dce]:''}. Score PI-RADS v2.1 : ${s}.`}});

// ---------- Bone-RADS ----------
bind('bonerads',(f)=>{const p=+f.get('mg')+ +f.get('pr')+ +f.get('en')+(f.get('fx')?2:0)+(f.get('pm')?4:0)+(f.get('ca')?2:0);
 let r; if(p<=2)r=['c1','1 · très faible risque','Asymptomatique : bilan terminé ou surveillance annuelle ; symptomatique : imagerie avancée, avis orthopédique.'];
 else if(p<=4)r=['c2','2 · faible risque','Contrôle rapproché à 3–6 mois ; imagerie avancée ± biopsie si besoin ; avis d\'orthopédie oncologique à discuter.'];
 else if(p<=6)r=['c3','3 · risque intermédiaire','Avis d\'orthopédie oncologique pour biopsie probable ; scanner, IRM ou scintigraphie.'];
 else r=['c5','4 · haut risque','Maligne jusqu\'à preuve du contraire : centre de référence, biopsie planifiée avec le chirurgien, bilan d\'extension.'];
 return {k:'Total',v:p+' pt'+(p>1?'s':''),cls:r[0],cat:'Bone-RADS '+r[1],cdt:r[2],ph:`Lésion osseuse solitaire : Bone-RADS ${r[1].split(' ·')[0]} (${p} points, v2023). ${r[2]}`}});
// ---------- AVC aigu : thrombolyse / thrombectomie (questions progressives) ----------
const fa=$('#f-avctt');
if(fa){const steps=$$('.a-step',fa);
 const num=v=>{const x=parseFloat(String(v==null?'':v).replace(',','.')); return isNaN(x)?null:x};
 function upd(){const f=new FormData(fa);
  const hem=f.get('hem'),win=f.get('win'),occ=f.get('occ'),mrs=f.get('mrs'),asp=f.get('asp'),age=f.get('age'),nih=f.get('nih');
  const core=num(f.get('core')),pen=num(f.get('pen')),ratio=num(f.get('ratio'));
  const hasCTP=core!=null||ratio!=null||pen!=null;
  // révélation progressive des étapes
  steps[1].style.display=hem==='0'?'':'none';
  steps[2].style.display=win?'':'none';
  steps[3].style.display=(occ&&win!=='wout')?'':'none';
  steps[4].style.display=(mrs==='01'&&win!=='wout')?'':'none';
  steps[5].style.display=((win==='w9'&&hem==='0')||(win==='w24'&&mrs==='01'&&asp&&asp!=='02'))?'':'none';
  let r;
  if(hem==='1'){r={k:'Décision',cls:'c5',cat:'Hémorragie intracrânienne',cdt:'Ni thrombolyse ni thrombectomie.',why:'Contrôle de la pression artérielle, bilan de coagulation ; avis neurochirurgical selon le volume et la localisation (fiche NE-01).',ph:'Scanner sans injection : hémorragie intracrânienne. Pas d\'indication de thrombolyse ni de thrombectomie.'};}
  else if(!hem||!win){r={k:'Décision',cls:'c0',cat:'Répondre aux étapes',why:'Les questions apparaissent au fur et à mesure des réponses.',cdt:'Commencer par l\'absence d\'hémorragie puis l\'heure du dernier contact normal.',ph:' '};}
  else{
   // voie thrombolyse
   let ivt;
   if(win==='w45') ivt={ok:1,t:'IVT immédiate',d:'TNK 0,25 mg/kg (max 25 mg) ou altéplase 0,9 mg/kg — sans attendre l\'imagerie avancée (CTP inutile)'};
   else if(win==='w9'){ if(hasCTP){const ext=(core!=null?core<70:true)&&(ratio!=null?ratio>1.2:true)&&(pen!=null?pen>10:true)&&(core!=null||ratio!=null||pen!=null);
     ivt=ext?{ok:1,t:'IVT raisonnable (profil EXTEND)',d:'cœur < 70 mL · ratio > 1,2 · mismatch > 10 mL'}:{ok:0,t:'Pas d\'IVT (hors profil EXTEND)',d:'cœur ≥ 70 mL, ratio ≤ 1,2 ou mismatch ≤ 10 mL'};}
    else ivt={pend:1,t:'IVT : CTP ou IRM nécessaire',d:'EXTEND : cœur < 70 mL · ratio > 1,2 · mismatch > 10 mL (ou mismatch FLAIR–DWI à l\'IRM)'};}
   else if(win==='w24') ivt={ok:0,t:'Pas d\'IVT',d:'9–24 h : classe 2b (LVO + tissu sauvable sans option d\'EVT, cas marginal) seulement'};
   else ivt={ok:0,t:'Pas d\'IVT',d:'hors fenêtre thérapeutique (> 24 h)'};
   // voie thrombectomie
   let evt;
   if(occ==='non') evt={ok:0,t:'Pas d\'EVT systématique',d:'occlusion distale (M2 non dominante, M3, ACA, ACP) ou absente — ESCAPE-MeVo et DISTAL négatifs'};
   else if(win==='wout') evt={ok:0,t:'Pas d\'EVT',d:'hors fenêtre thérapeutique (> 24 h)'};
   else if(mrs==='ge2') evt={ok:0,t:'Pas d\'EVT',d:'mRS préalable ≥ 2'};
   else if(!asp) evt={pend:1,t:'EVT : ASPECTS à préciser',d:''};
   else if(win==='w45'){ if(asp!=='02') evt={ok:1,t:'EVT recommandée (0–6 h, classe 1 A)',d:'ASPECTS 3–10 · NIHSS ≥ 6 · CTP inutile, ne pas retarder'};
    else evt={ok:0,t:'EVT : cas très sélectionnés',d:'ASPECTS 0–2'};}
   else{ // w9 (4,5–9) ou w24 (9–24) : fenêtre étendue
    if(asp==='ge6'){ let det='ASPECTS ≥ 6 · classe 1 A · CTP ou IRM requise (profils DAWN / DEFUSE 3)';
     if(hasCTP&&core!=null){const defuse=core<70&&ratio!=null&&ratio>=1.8&&pen!=null&&pen>=15;
      const dawn=(age==='ge80'&&nih!=='lt10'&&nih&&core<21)||(age==='lt80'&&((nih==='ge10'&&core<31)||(nih==='ge20'&&core>=31&&core<=51)));
      det+=defuse?' · profil DEFUSE 3 ✓':(dawn?' · profil DAWN ✓':' · CTP non concluante : décision avec le neurologue et le PERT');}
     evt={ok:1,t:'EVT recommandée ('+(win==='w9'?'4,5–9 h':'6–24 h')+', classe 1 A)',d:det};}
    else if(asp==='35'){ if(age==='lt80') evt={ok:1,t:'EVT chez des patients sélectionnés',d:'ASPECTS 3–5 · < 80 ans · pas d\'effet de masse · un cœur > 70 mL n\'exclut plus seul'};
     else if(age==='ge80') evt={ok:0,t:'EVT : très sélectionnée',d:'ASPECTS 3–5 et ≥ 80 ans : profil DAWN uniquement (cœur < 21 mL, NIHSS ≥ 10)'};
     else evt={pend:1,t:'EVT : âge à préciser (profil cœur étendu)',d:'ASPECTS 3–5 : EVT si < 80 ans sans effet de masse'};}
    else evt={ok:0,t:'Pas d\'EVT',d:'ASPECTS 0–2 en fenêtre étendue'};}
   // synthèse
   const iv=ivt?(ivt.ok?'IVT ✓':(ivt.pend?'IVT ?':'IVT ✗')):'';
   const ev=evt?(evt.ok?'EVT ✓':(evt.pend?'EVT ?':'EVT ✗')):'';
   const cls=(ivt&&ivt.ok&&(!evt||evt.ok))?'c1':((ivt&&ivt.ok)||(evt&&evt.ok))?'c2':'c5';
   const bridging=(ivt&&ivt.ok&&evt&&evt.ok)?' Éligible aux deux = les deux : l\'IVT part sans attendre et ne retarde jamais l\'EVT.':'';
   r={k:'Décision',v:[iv,ev].filter(Boolean).join(' · '),cls,cat:[ivt&&ivt.t,evt&&evt.t].filter(Boolean).filter(t=>t).join(' · '),
    why:'Fenêtre : '+(win==='w45'?'< 4,5 h':win==='w9'?'4,5–9 h ou réveil':win==='w24'?'9–24 h':'> 24 h')+(occ?' · occlusion proximale : '+(occ==='oui'?'oui':'non'):'')+(asp?' · ASPECTS '+(asp==='ge6'?'≥ 6':asp==='35'?'3–5':'0–2'):'')+'.',
    cdt:[ivt&&ivt.d,evt&&evt.d].filter(Boolean).filter(d=>d).join(' — ')+bridging+' Cohérence finale avec la clinique et le neurologue (PERT si catégorie C–E).',
    ph:'AVC ischémique aigu : '+(win==='w45'?'dernier contact normal < 4,5 h':win==='w9'?'dernier contact normal 4,5–9 h ou réveil':win==='w24'?'dernier contact normal 9–24 h':'dernier contact normal > 24 h')+(occ==='oui'?', occlusion proximale (ACI/M1)':occ==='non'?', pas d\'occlusion proximale':'')+(asp?', ASPECTS '+(asp==='ge6'?'≥ 6':asp==='35'?'3–5':'0–2'):'')+(mrs==='01'?', mRS préalable 0–1':'')+'. Décision : '+[ivt&&ivt.t,evt&&evt.t].filter(Boolean).filter(t=>t).join(' ; ')+'. '+((ivt&&ivt.ok&&evt&&evt.ok)?'Bridging : IVT sans attendre puis thrombectomie.':'')};
  }
  render('avctt',r);}
 fa.addEventListener('input',upd); fa.addEventListener('change',upd); upd();}

// ---------- Coroscanner : préparation ralentisseur + trinitrine (questions progressives) ----------
const fp=$('#f-coroprep');
if(fp){const stepsP=$$('.a-step',fp);
 function updP(){const f=new FormData(fp);
  const fc=f.get('fc'),cibb=f.get('cibb'),cible=f.get('cible'),alt=f.get('alt');
  const ci=f.getAll('citng').filter(v=>v!=='none');
  const noTng=ci.length>0;
  stepsP[1].style.display=fc==='ge65'?'':'none';
  stepsP[2].style.display=(fc==='ge65'&&cibb==='non')?'':'none';
  stepsP[3].style.display=(fc==='ge65'&&cibb==='oui')?'':'none';
  stepsP[4].style.display=fc?'':'none';
  const CITXT={pde5:'PDE5 récent (sildénafil/vardénafil < 24 h, tadalafil < 48 h)',pa:'PAS < 90–100 mmHg',sa:'sténose aortique sévère ou HCM',hyp:'hypovolémie ou choc'};
  let r;
  if(!fc){r={k:'Préparation',cls:'c0',cat:'Répondre aux étapes',why:'Les questions apparaissent au fur et à mesure des réponses.',cdt:'Commencer par la fréquence cardiaque au repos ( idéalement après inspiration).',ph:' '};}
  else{
   let bb,acq='acquisition prospective (basse dose) si la FC reste basse et régulière';
   if(fc==='lt65') bb={t:'Pas de ralentisseur requis',d:'FC < 65/min ; une petite dose de bêtabloquant reste possible pour réduire la variabilité de FC et permettre le prospectif.'};
   else if(cibb==='non'&&cible==='oui') bb={t:'Métoprolol per os suffisant',d:'Cible < 60/min atteinte ~1 h après 50–100 mg per os (aténolol si insuffisance hépatique).'};
   else if(cibb==='non'&&cible==='non'){bb={t:'Relais IV en salle de scanner',d:'Métoprolol IV lent par paliers de 5 mg sous monitorage PA/FC ; si la cible n\'est pas atteinte, basculer en rétrospectif multi-phase (dose plus élevée, mais rattrapage possible dans une autre phase du cycle).'};acq='acquisition rétrospective multi-phase si la cible n\'est pas atteinte';}
   else if(cibb==='oui'&&alt==='iva') bb={t:'Ivabradine',d:'Ralentisseur sinusal pur, sans effet sur la conduction ni la PA — hors AMM, phase investigationnelle (SCCT 2016).'};
   else if(cibb==='oui'&&alt==='dil') bb={t:'Diltiazem',d:'Alternative si pas de trouble conductif ; surveiller PA et FC.'};
   else if(cibb==='oui'&&alt==='aucun'){bb={t:'Aucun ralentisseur possible',d:'FC non contrôlée : acquisition rétrospective multi-phase d\'emblée (dose plus élevée). Lecture prudente : artefacts de mouvement attendus, surtout IVA distale et CX.'};acq='acquisition rétrospective multi-phase d\'emblée';}
   else bb={t:'Ralentisseur à préciser',d:'Répondre à l\'étape en cours : cible atteinte après métoprolol per os, ou alternative retenue en cas de contre-indication.'};
   const tng=noTng?{t:'Trinitrine contre-indiquée',d:'Pas de TNG ('+ci.map(v=>CITXT[v]).join(', ')+'). Réserve de lecture : lumière sous-estimée, sténoses surévaluées.'}:{t:'Trinitrine 0,4 mg sublinguale',d:'Administrer 3–5 min avant l\'acquisition (vasodilatation : sans nitrates, la lumière est sous-estimée et les sténoses surévaluées).'};
   const done=(fc==='lt65')||(cibb==='non'&&cible)||(cibb==='oui'&&alt);
   const cls=!done?'c0':(noTng?'c2':'c1');
   r={k:'Préparation',cls,cat:bb.t+' · '+tng.t,
    why:'FC '+(fc==='ge65'?'≥ 65/min':'< 65/min')+(cibb?' · contre-indication au bêtabloquant : '+(cibb==='oui'?'oui':'non'):'')+(cible?' · cible < 60/min atteinte : '+(cible==='oui'?'oui':'non'):'')+(alt?' · alternative : '+(alt==='iva'?'ivabradine':alt==='dil'?'diltiazem':'aucune'):'')+(noTng?' · CI trinitrine : '+ci.map(v=>CITXT[v]).join(', '):'')+'.',
    cdt:bb.d+' '+tng.d+' '+acq+'. Cohérence finale avec la clinique et les protocoles du service.',
    ph:'Préparation coroscanner : FC '+(fc==='ge65'?'≥ 65/min':'< 65/min')+' — '+bb.t.toLowerCase()+' ; trinitrine '+(noTng?'non administrée ('+ci.map(v=>CITXT[v]).join(', ')+')':'0,4 mg sublinguale 3–5 min avant l\'acquisition')+'.'};
  }
  render('coroprep',r);}
 fp.addEventListener('input',updP); fp.addEventListener('change',updP); updP();}

})();