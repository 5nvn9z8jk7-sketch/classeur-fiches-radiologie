import math
def pt(cx,cy,rx,ry,a,k=1): 
    r=math.radians(a); return cx+k*rx*math.cos(r), cy+k*ry*math.sin(r)
def band(cx,cy,rx,ry,a1,a2,k1,k2,n=24):
    pts=[pt(cx,cy,rx,ry,a1+(a2-a1)*i/n,k2) for i in range(n+1)]+[pt(cx,cy,rx,ry,a2+(a1-a2)*i/n,k1) for i in range(n+1)]
    return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'Z'
def lab(cx,cy,rx,ry,a,k,t,fill='#1d2430'):
    x,y=pt(cx,cy,rx,ry,a,k); return f'<text x="{x:.1f}" y="{y+3.5:.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="{fill}">{t}</text>'
INTER=False
def RA(n): return f'class="rg" data-r="{n}"' if INTER else ''
MCA='#F6C1C1'; MCA2='#FBD9BD'; DEEP='#FCEFC7'; GRAY='#e6e9ee'
def slice_(ox,title,level):
    cx,cy,rx,ry=ox+125,150,112,128
    s=f'<g font-family="IS">'
    s+=f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#f8f9fb" stroke="#4a5462" stroke-width="1.2"/>'
    s+=f'<line x1="{cx}" y1="{cy-ry}" x2="{cx}" y2="{cy+ry}" stroke="#aab2bd" stroke-width="0.8" stroke-dasharray="3 2"/>'
    k1=0.86 if level=='g' else 0.62
    # ACA / PCA gray on left hemisphere
    s+=f'<path d="{band(cx,cy,rx,ry,270,233,k1,1)}" fill="{GRAY}" stroke="#fff" stroke-width="1"/>'
    s+=f'<path d="{band(cx,cy,rx,ry,121,90,k1,1)}" fill="{GRAY}" stroke="#fff" stroke-width="1"/>'
    names=['M1','M2','M3'] if level=='g' else ['M4','M5','M6']
    secs=[(233,197),(197,159),(159,121)]
    for (a1,a2),nm in zip(secs,names):
        s+=f'<path {RA(nm)} d="{band(cx,cy,rx,ry,a1,a2,k1,1)}" fill="{MCA}" stroke="#fff" stroke-width="1.2"/>'
        s+=lab(cx,cy,rx,ry,(a1+a2)/2,(k1+1)/2,nm,'#8B1A1A')
    s+=lab(cx,cy,rx,ry,251,(k1+1)/2,'ACA','#7a8492')+lab(cx,cy,rx,ry,105,(k1+1)/2,'ACP','#7a8492')
    if level=='g':
        s+=f'<path d="M{cx-3},{cy-72} C{cx-20},{cy-70} {cx-24},{cy-45} {cx-16},{cy-24} L{cx-3},{cy-24} Z" fill="#cfd8e3"/>'
        s+=f'<ellipse {RA('C')} cx="{cx-30}" cy="{cy-50}" rx="10" ry="17" fill="{DEEP}" stroke="#7A5200" stroke-width="0.8"/><text x="{cx-30}" y="{cy-46}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#7A5200">C</text>'
        s+=f'<path {RA('IC')} d="M{cx-44},{cy-74} L{cx-34},{cy-22} L{cx-50},{cy+36}" fill="none" stroke="#D9CCF2" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/><text x="{cx-37}" y="{cy+8}" text-anchor="middle" font-size="8" font-weight="700" fill="#4B2A8A">IC</text>'
        s+=f'<ellipse cx="{cx-17}" cy="{cy+12}" rx="12" ry="24" fill="{GRAY}"/><text x="{cx-17}" y="{cy+15}" text-anchor="middle" font-size="7" fill="#7a8492">Th</text>'
        s+=f'<path {RA('L')} d="M{cx-46},{cy-52} C{cx-60},{cy-50} {cx-72},{cy-30} {cx-72},{cy-5} C{cx-72},{cy+18} {cx-64},{cy+30} {cx-54},{cy+30} L{cx-42},{cy-22} Z" fill="{DEEP}" stroke="#7A5200" stroke-width="0.8"/><text x="{cx-58}" y="{cy-6}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#7A5200">L</text>'
        s+=f'<path {RA('I')} d="M{cx-80},{cy-52} C{cx-86},{cy-22} {cx-86},{cy+12} {cx-80},{cy+36}" fill="none" stroke="#F4A97A" stroke-width="6" stroke-linecap="round"/><text x="{cx-91}" y="{cy-20}" text-anchor="middle" font-size="9" font-weight="700" fill="#8A3A0F">I</text>'
    else:
        s+=f'<path d="M{cx-3},{cy-40} C{cx-14},{cy-38} {cx-14},{cy+30} {cx-3},{cy+34} Z" fill="#cfd8e3"/>'
    s+=f'<text x="{cx}" y="{cy+ry+18}" text-anchor="middle" font-size="10.5" font-weight="600" fill="#1d2430">{title}</text>'
    s+=f'<text x="{cx}" y="{cy-ry-6}" text-anchor="middle" font-size="8" fill="#7a8492">avant</text></g>'
    return s
def make():
  return f'''<svg viewBox="0 0 520 318" role="img" style="width:100%;height:auto"><title>Schéma simplifié des 10 régions ASPECTS</title>
{slice_(10,'Niveau des noyaux gris (thalamo-striatal)','g')}{slice_(265,'Niveau supra-ganglionnaire','s')}
<text x="10" y="314" font-size="7.5" fill="#7a8492" font-family="IS">Schéma simplifié, non à l'échelle · hémisphère droit du patient à gauche de l'image (convention radiologique)</text></svg>'''
open('gen/aspects.svg','w').write(make())
INTER=True
open('gen/aspects_i.svg','w').write(make())
