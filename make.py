"""One command: python make.py specs/<spec>.json [--still-only]
Builds the still (4K PNG) and, if the spec has "motion": true, a 1080p MP4 from the same spec."""
import sys, json, importlib
sys.path.insert(0,__file__.rsplit("/",1)[0])
import studio
def run(path,still_only=False):
    sp=json.load(open(path,encoding="utf-8")); t=importlib.import_module("templates."+sp["type"])
    html,dur=t.build(sp); out=[studio.render(html,sp["name"])]
    if sp.get("motion") and not still_only: out.append(studio.animate(html,sp["name"],duration=dur))
    return out
if __name__=="__main__":
    for o in run(sys.argv[1],"--still-only" in sys.argv): print(o)
