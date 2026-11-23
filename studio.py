"""STUDIO OS visual kit: design tokens, shared CSS, still render and motion render."""
import os, shutil, subprocess, tempfile, glob

def _find_ffmpeg():
    """Return ffmpeg binary path: system PATH first, then Playwright's bundled copy."""
    import shutil as _sh
    ff = _sh.which("ffmpeg")
    if ff:
        return ff
    # Playwright bundles ffmpeg — find it across common locations
    patterns = [
        os.path.expanduser("~/.cache/ms-playwright/ffmpeg-*/ffmpeg"),
        os.path.expanduser("~/.cache/ms-playwright/ffmpeg-*/ffmpeg-linux"),
        os.path.expandvars("%LOCALAPPDATA%/ms-playwright/ffmpeg-*/ffmpeg-win64.exe"),
        os.path.expandvars("%USERPROFILE%/AppData/Local/ms-playwright/ffmpeg-*/ffmpeg-win64.exe"),
    ]
    for pat in patterns:
        found = glob.glob(pat)
        if found:
            return found[0]
    raise FileNotFoundError("ffmpeg not found. Install ffmpeg or run: playwright install chromium")
ROOT=os.path.dirname(os.path.abspath(__file__))
FONTS="file://"+os.path.join(ROOT,"fonts")+"/"
TOK=dict(paper="#F7F5F0",ink="#1C1B19",graphite="#4A4741",mute="#6F6B63",stone="#BDB6A8",hair="#E3DFD6",signal="#B4492D",tide="#3E5C6B")
def _ff(fam,w,f,style=""):
    return f"@font-face{{font-family:'{fam}';font-weight:{w};{style}src:url({FONTS}{f}.woff2)}}"
CSS="".join([_ff("Serif",400,"source-serif-4-latin-400-normal"),_ff("Serif",600,"source-serif-4-latin-600-normal"),_ff("Serif",700,"source-serif-4-latin-700-normal"),
 _ff("Serif",400,"source-serif-4-latin-400-italic","font-style:italic;"),_ff("Serif",600,"source-serif-4-latin-600-italic","font-style:italic;"),
 _ff("Sans",400,"inter-latin-400-normal"),_ff("Sans",500,"inter-latin-500-normal"),_ff("Sans",600,"inter-latin-600-normal"),_ff("Sans",700,"inter-latin-700-normal")])+"""
:root{--paper:#F7F5F0;--ink:#1C1B19;--graphite:#4A4741;--mute:#6F6B63;--stone:#BDB6A8;--hair:#E3DFD6;--signal:#B4492D;--tide:#3E5C6B}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1920px;height:1080px;background:var(--paper);color:var(--ink);font-family:'Sans',sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}
.kicker{font:600 15px 'Sans';letter-spacing:.16em;text-transform:uppercase;color:var(--signal)}
.src{font:400 14px/1.45 'Sans';color:var(--mute)}
.num{font-feature-settings:'tnum' 1,'lnum' 1}
.frame-top{position:absolute;left:80px;top:56px;right:80px;display:flex;justify-content:space-between;align-items:baseline}
.frame-bot{position:absolute;left:80px;right:80px;bottom:44px;display:flex;justify-content:space-between;align-items:flex-end;gap:60px;border-top:1px solid var(--hair);padding-top:14px}
.brand{font:600 13px 'Sans';letter-spacing:.2em;color:var(--stone);white-space:nowrap}
.h1{position:absolute;left:80px;top:92px;font:600 54px/1.06 'Serif';letter-spacing:-.015em;width:1700px}
.sub{position:absolute;left:80px;top:160px;font:italic 400 24px/1.35 'Serif';color:var(--graphite)}
.st{display:inline-block;font:600 12px 'Sans';letter-spacing:.12em;text-transform:uppercase;padding:6px 11px;border-radius:2px}
.s-verified{background:#1C1B19;color:#F7F5F0}.s-reported{border:1.5px solid #1C1B19;color:#1C1B19}.s-officialclaim{border:1.5px solid #3E5C6B;color:#3E5C6B}
.s-estimate{border:1.5px dashed #B4492D;color:#B4492D}.s-analysis{background:#E3DFD6;color:#4A4741;font-style:italic}.s-unverified{border:1.5px solid #BDB6A8;color:#6F6B63;text-decoration:line-through}
"""
def chip(status,text=None):
    return f"<span class='st s-{status.lower().replace(' ','')}'>{text or status}</span>"
def page(body,extra=""):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{extra}</style></head><body>{body}</body></html>"
MOTION_JS="""<script>
function ease(p){return 1-Math.pow(1-p,3)}
window.frame=function(t){document.querySelectorAll('[data-a]').forEach(function(el){
 var s=parseFloat(el.dataset.s||0),d=parseFloat(el.dataset.d||.5),p=Math.max(0,Math.min(1,(t-s)/d)),e=ease(p),a=el.dataset.a;
 if(a==='grow'){el.style.transformBox='fill-box';el.style.transformOrigin='50% 100%';el.style.transform='scaleY('+e+')'}
 else if(a==='growx'){el.style.transformBox='fill-box';el.style.transformOrigin='0% 50%';el.style.transform='scaleX('+e+')'}
 else{el.style.opacity=e}})}
</script>"""
def _pw():
    from playwright.sync_api import sync_playwright
    return sync_playwright()
def render(html,name,scale=2):
    path=os.path.join(ROOT,"build",name+".html"); open(path,"w",encoding="utf-8").write(html)
    out=os.path.join(ROOT,"out",name+".png")
    with _pw() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={"width":1920,"height":1080},device_scale_factor=scale)
        pg.goto("file://"+path); pg.wait_for_timeout(500); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
        pg.screenshot(path=out); b.close()
    return out
def animate(html,name,duration=7.0,fps=30,scale=1):
    path=os.path.join(ROOT,"build",name+"_motion.html"); open(path,"w",encoding="utf-8").write(html.replace("</body>",MOTION_JS+"</body>"))
    out=os.path.join(ROOT,"out",name+".mp4"); tmp=tempfile.mkdtemp(); n=int(duration*fps)
    with _pw() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={"width":1920,"height":1080},device_scale_factor=scale)
        pg.goto("file://"+path); pg.wait_for_timeout(500); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
        for i in range(n):
            pg.evaluate(f"window.frame({i/fps})"); pg.screenshot(path=f"{tmp}/f{i:04d}.png")
        b.close()
    subprocess.run([_find_ffmpeg(),"-y","-loglevel","error","-framerate",str(fps),"-i",f"{tmp}/f%04d.png","-c:v","libx264","-pix_fmt","yuv420p","-crf","16","-movflags","+faststart",out],check=True)
    shutil.rmtree(tmp); return out
