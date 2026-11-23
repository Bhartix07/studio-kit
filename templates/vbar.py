"""Column chart with baseline, shortfall outlines and dated event markers. Spec-driven."""
from datetime import date
from studio import page, chip
def _d(s): y,m,d=map(int,s.split("-")); return date(y,m,d)
def build(sp):
    ymax=sp["y"]["max"]; base=860; top=300; k=(base-top)/ymax; Y=lambda v: base-v*k
    slots=sp["slots"]; n=len(slots); x0,x1=140,1540; sw=(x1-x0)/n; bw=sw*.75; off=(sw-bw)/2
    T=sp.get("timing",{}); t0=T.get("first",0.9); gap=T.get("gap",1.2)
    pre=sp["baseline"]["value"]; grid=""
    for v in sp["y"]["ticks"]:
        grid+=f"<line x1='{x0}' x2='{x1}' y1='{Y(v)}' y2='{Y(v)}' stroke='#E3DFD6'/><text x='{x0-14}' y='{Y(v)+5}' text-anchor='end' class='ax num'>{v}</text>"
    bars=""; ev=""; seq=0; slot_t={}
    for i,s in enumerate(slots):
        sx=x0+i*sw; bx=sx+off
        if "value" not in s:
            bars+=f"<g data-a='fade' data-s='{t0+gap*(n-1)+1.2:.2f}' data-d='.5'><rect x='{bx}' y='{Y(12)}' width='{bw}' height='{12*k}' fill='none' stroke='#BDB6A8' stroke-width='1.4' stroke-dasharray='3 6'/><text x='{bx+bw/2}' y='{Y(6)+6}' text-anchor='middle' class='qs'>{s.get('pending','')}</text></g><text x='{bx+bw/2}' y='{base+34}' text-anchor='middle' class='ql' style='fill:#9A9385'>{s['label']}</text>"
            continue
        v=s["value"]; ts=t0+gap*seq; slot_t[i]=ts; seq+=1; base_bar=(s.get("style")=="base")
        fill='#BDB6A8' if base_bar else '#B4492D'; op=f" fill-opacity='{s['opacity']}'" if "opacity" in s else ""
        if not base_bar:
            gh=(pre-v)*k
            bars+=f"<g data-a='fade' data-s='{ts+.4:.2f}' data-d='.5'><rect x='{bx}' y='{Y(pre)}' width='{bw}' height='{gh}' fill='none' stroke='#9A9385' stroke-width='1.4' stroke-dasharray='6 5'/><text x='{bx+bw/2}' y='{Y(pre)+gh/2+7}' text-anchor='middle' class='gl num'>−{pre-v:.1f}</text></g>"
        bars+=f"<rect data-a='grow' data-s='{ts:.2f}' data-d='.9' x='{bx}' y='{Y(v)}' width='{bw}' height='{v*k}' fill='{fill}'{op}/>"
        bars+=f"<text data-a='fade' data-s='{ts+.7:.2f}' data-d='.3' x='{bx+bw/2}' y='{Y(v)-14}' text-anchor='middle' class='vl num'>{v}</text>"
        if not base_bar:
            pct=str(round((v-pre)/pre*100)).replace('-','−')
            bars+=f"<text data-a='fade' data-s='{ts+.8:.2f}' data-d='.3' x='{bx+bw/2}' y='{base-18}' text-anchor='middle' class='pc num'>{pct}%</text>"
        bars+=f"<text x='{bx+bw/2}' y='{base+34}' text-anchor='middle' class='ql'>{s['label']}</text>"
        if s.get("sub"): bars+=f"<text x='{bx+bw/2}' y='{base+58}' text-anchor='middle' class='qs'>{s['sub']}</text>"
    for e in sp.get("events",[]):
        d=_d(e["date"]); idx=next(i for i,s in enumerate(slots) if _d(s["start"])<=d<=_d(s["end"]))
        s=slots[idx]; span=(_d(s["end"])-_d(s["start"])).days+1; x=x0+idx*sw+sw*((d-_d(s["start"])).days/span)
        y=262 if e.get("row",0)==0 else 292; ts=slot_t.get(idx,t0)-.3
        ev+=f"<g data-a='fade' data-s='{max(ts,0):.2f}' data-d='.4'><line x1='{x}' x2='{x}' y1='{y+6}' y2='{Y(pre)-4}' stroke='#1C1B19' stroke-width='1.1' stroke-dasharray='3 4' opacity='.55'/><circle cx='{x}' cy='{y+6}' r='4' fill='#1C1B19'/><text x='{x+10}' y='{y+11}' class='ev'><tspan style='font-weight:700'>{e['label_date']}</tspan> {e['label']}</text></g>"
    bl=f"<g data-a='fade' data-s='{t0+.6:.2f}' data-d='.5'><line x1='{x0}' x2='{x1}' y1='{Y(pre)}' y2='{Y(pre)}' stroke='#1C1B19' stroke-width='1.2' stroke-dasharray='2 4'/><text x='{x1}' y='{Y(pre)-10}' text-anchor='end' class='ax' style='fill:#1C1B19;font-weight:600'>{sp['baseline']['label']}</text></g>"
    svg=f"<svg width='1920' height='1080' style='position:absolute;left:0;top:0'><g data-a='fade' data-s='.2' data-d='.6'>{grid}<line x1='{x0}' x2='{x1}' y1='{base}' y2='{base}' stroke='#1C1B19' stroke-width='1.5'/></g>{bars}{bl}{ev}</svg>"
    side=sp["side"]; end=t0+gap*(n-1)+1.4
    stats="".join(f"<div class='n'><i class='num'>{x['n']}</i><span>{x['t']}</span></div>" for x in side["stats"])
    css=""".ax{font:500 14px 'Sans';fill:#6F6B63}.vl{font:600 30px 'Serif';fill:#1C1B19}.gl{font:500 17px 'Sans';fill:#6F6B63}.pc{font:600 18px 'Sans';fill:#F7F5F0}
.ql{font:600 17px 'Sans';fill:#1C1B19}.qs{font:italic 400 17px 'Serif';fill:#6F6B63}.ev{font:400 15.5px 'Sans';fill:#1C1B19}
.side{position:absolute;left:1600px;top:300px;width:240px}.side .n{border-top:1px solid #1C1B19;padding:12px 0 22px}
.side i{font:600 52px/1 'Serif';font-style:normal;letter-spacing:-.02em;display:block}.side span{font:400 15px/1.4 'Sans';color:#4A4741;display:block;margin-top:6px}"""
    body=f"""<div class='frame-top'><span class='kicker'>{sp['kicker']}</span><span class='brand'>STUDIO OS</span></div>
<div class='h1' data-a='fade' data-s='0' data-d='.5'>{sp['title']}</div><div class='sub' data-a='fade' data-s='.1' data-d='.5'>{sp['subtitle']}</div>{svg}
<div class='side' data-a='fade' data-s='{end:.2f}' data-d='.6'><div style='margin-bottom:14px'>{chip(side['chip_status'],side['chip'])}</div>{stats}</div>
<div class='frame-bot'><span class='src'>{sp['source']}</span><span class='brand'>{sp.get('page','')}</span></div>"""
    return page(body,css), end+1.2
