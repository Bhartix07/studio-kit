"""Horizontal comparison bars with groups, ranges, status chips and a callout. Spec-driven."""
from studio import page, chip
def build(sp):
    xm=sp["x"]["max"]; bx0,bx1=640,1440; k=(bx1-bx0)/xm; X=lambda v: bx0+v*k
    y=262; svg=""; html=""; seq=0
    for g in sp["groups"]:
        html+=f"<div class='gh' style='top:{y}px'>{g['label']}</div>"; y+=34
        for r in g["rows"]:
            ts=.8+.55*seq; seq+=1; st=r.get("style","tide"); cy=y+40
            if "range" in r:
                a,b=r["range"]; svg+=f"<rect data-a='growx' data-s='{ts:.2f}' data-d='.8' x='{X(a)}' y='{cy-20}' width='{(b-a)*k}' height='40' fill='#3E5C6B' fill-opacity='.85'/><line x1='{X(a)}' x2='{X(a)}' y1='{cy-28}' y2='{cy+28}' stroke='#1C1B19' stroke-width='1.5'/><line x1='{X(b)}' x2='{X(b)}' y1='{cy-28}' y2='{cy+28}' stroke='#1C1B19' stroke-width='1.5'/>"
                vx=X(b)+16; val=f"{a}–{b}"
            else:
                v=r["value"]; w=v*k
                if st=="unverified": svg+=f"<rect data-a='growx' data-s='{ts:.2f}' data-d='.8' x='{bx0}' y='{cy-20}' width='{w}' height='40' fill='none' stroke='#BDB6A8' stroke-width='1.6' stroke-dasharray='6 5'/>"
                else:
                    fill={'base':'#BDB6A8','crisis':'#B4492D','tide':'#3E5C6B'}[st]; op=f" fill-opacity='{r['opacity']}'" if "opacity" in r else ""
                    svg+=f"<rect data-a='growx' data-s='{ts:.2f}' data-d='.8' x='{bx0}' y='{cy-20}' width='{w}' height='40' fill='{fill}'{op}/>"
                vx=X(v)+16; val=str(v)
            strike="text-decoration:line-through;color:#9A9385;" if st=="unverified" else ""
            html+=f"<div class='rl' style='top:{cy-30}px'><b>{r['label']}</b><span>{r.get('note','')}</span></div>"
            html+=f"<div class='rv num' data-a='fade' data-s='{ts+.7:.2f}' data-d='.3' style='left:{vx}px;top:{cy-22}px;{strike}'>{val}</div>"
            html+=f"<div class='rc' data-a='fade' data-s='{ts+.7:.2f}' data-d='.3' style='top:{cy-14}px'>{chip(r['chip_status'],r['chip'])}</div>"
            y+=86
        y+=20
    ybot=y-14
    grid="".join(f"<line x1='{X(v)}' x2='{X(v)}' y1='250' y2='{ybot}' stroke='#E3DFD6'/><text x='{X(v)}' y='{ybot+24}' text-anchor='middle' class='ax num'>{v}</text>" for v in sp["x"]["ticks"])
    svgall=f"<svg width='1920' height='1080' style='position:absolute;left:0;top:0'><g data-a='fade' data-s='.2' data-d='.6'>{grid}<line x1='{bx0}' x2='{bx0}' y1='250' y2='{ybot}' stroke='#1C1B19' stroke-width='1.5'/></g>{svg}</svg>"
    c=sp["callout"]; ct=.8+.55*seq+.6
    css=""".ax{font:500 14px 'Sans';fill:#6F6B63}
.gh{position:absolute;left:80px;font:700 12.5px 'Sans';letter-spacing:.16em;text-transform:uppercase;color:#4A4741}
.rl{position:absolute;left:80px;width:520px}.rl b{display:block;font:600 24px/1.15 'Serif'}.rl span{display:block;font:400 14px/1.35 'Sans';color:#6F6B63;margin-top:3px}
.rv{position:absolute;font:600 34px/1 'Serif';letter-spacing:-.01em}
.rc{position:absolute;left:1560px;width:300px}
.call{position:absolute;left:80px;bottom:132px;display:flex;align-items:baseline;gap:26px;border-top:1px solid #1C1B19;padding-top:14px;right:80px}
.call i{font:600 64px/1 'Serif';font-style:normal;letter-spacing:-.02em}.call span{font:italic 400 24px/1.3 'Serif';color:#4A4741;max-width:1200px}"""
    body=f"""<div class='frame-top'><span class='kicker'>{sp['kicker']}</span><span class='brand'>STUDIO OS</span></div>
<div class='h1' data-a='fade' data-s='0' data-d='.5'>{sp['title']}</div><div class='sub' data-a='fade' data-s='.1' data-d='.5'>{sp['subtitle']}</div>{svgall}{html}
<div class='call' data-a='fade' data-s='{ct:.2f}' data-d='.6'><i class='num'>{c['big']}</i><span>{c['text']}</span></div>
<div class='frame-bot'><span class='src'>{sp['source']}</span><span class='brand'>{sp.get('page','')}</span></div>"""
    return page(body,css), ct+1.8
