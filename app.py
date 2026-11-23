"""Flask web app for STUDIO OS visual kit."""
import os, json, tempfile, shutil, traceback
from flask import Flask, request, jsonify, send_file, render_template_string

app = Flask(__name__)
ROOT = os.path.dirname(os.path.abspath(__file__))

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>STUDIO OS — Visual Kit</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#F7F5F0;color:#1C1B19;font-family:'Inter',system-ui,sans-serif;min-height:100vh}
  header{border-bottom:1.5px solid #E3DFD6;padding:22px 40px;display:flex;justify-content:space-between;align-items:center}
  header h1{font-size:14px;letter-spacing:.2em;text-transform:uppercase;font-weight:600;color:#BDB6A8}
  header span{font-size:13px;color:#6F6B63}
  main{max-width:900px;margin:0 auto;padding:48px 24px}
  h2{font-size:28px;font-weight:600;margin-bottom:8px;line-height:1.2}
  .sub{color:#4A4741;font-size:16px;margin-bottom:36px;line-height:1.5}
  label{display:block;font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:#4A4741;margin-bottom:8px}
  textarea{width:100%;height:280px;border:1.5px solid #E3DFD6;border-radius:4px;background:#fff;font-family:'Courier New',monospace;font-size:13px;padding:16px;resize:vertical;outline:none;color:#1C1B19;transition:border-color .2s}
  textarea:focus{border-color:#3E5C6B}
  .opts{display:flex;gap:16px;margin:16px 0 24px;flex-wrap:wrap}
  .opts label{font-size:14px;letter-spacing:0;text-transform:none;font-weight:400;color:#1C1B19;display:flex;align-items:center;gap:6px;cursor:pointer}
  .opts input{cursor:pointer;accent-color:#3E5C6B}
  .examples{display:flex;gap:12px;margin-bottom:12px;flex-wrap:wrap}
  .ex-btn{background:none;border:1.5px solid #BDB6A8;border-radius:3px;padding:7px 14px;font-size:12px;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;color:#4A4741;transition:all .15s}
  .ex-btn:hover{border-color:#3E5C6B;color:#3E5C6B}
  .ex-label{font-size:12px;color:#6F6B63;margin-bottom:8px}
  button[type=submit]{background:#1C1B19;color:#F7F5F0;border:none;border-radius:3px;padding:14px 32px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;cursor:pointer;transition:opacity .2s}
  button[type=submit]:hover{opacity:.8}
  button[type=submit]:disabled{opacity:.4;cursor:not-allowed}
  #status{margin-top:20px;padding:16px;border-radius:4px;font-size:14px;display:none}
  .s-ok{background:#E3DFD6;color:#1C1B19;border:1px solid #BDB6A8}
  .s-err{background:#fce8e3;color:#8B1A00;border:1px solid #f5b4a0}
  .s-loading{background:#E3DFD6;color:#4A4741;border:1px solid #BDB6A8}
  #results{margin-top:28px;display:flex;gap:16px;flex-wrap:wrap}
  .dl-btn{display:inline-flex;align-items:center;gap:8px;background:#3E5C6B;color:#F7F5F0;text-decoration:none;padding:12px 24px;border-radius:3px;font-size:13px;font-weight:600;letter-spacing:.08em;transition:opacity .2s}
  .dl-btn:hover{opacity:.8}
  .dl-btn.mp4{background:#B4492D}
  .preview{margin-top:28px}
  .preview img{max-width:100%;border:1px solid #E3DFD6;border-radius:4px}
  .chip-row{display:flex;gap:8px;flex-wrap:wrap;margin:28px 0 12px}
  .chip{display:inline-block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;padding:5px 10px;border-radius:2px;font-weight:600}
  .s-verified{background:#1C1B19;color:#F7F5F0}
  .s-reported{border:1.5px solid #1C1B19;color:#1C1B19}
  .s-estimate{border:1.5px dashed #B4492D;color:#B4492D}
  .s-analysis{background:#E3DFD6;color:#4A4741;font-style:italic}
  .s-unverified{border:1.5px solid #BDB6A8;color:#6F6B63;text-decoration:line-through}
  .s-officialclaim{border:1.5px solid #3E5C6B;color:#3E5C6B}
  footer{border-top:1px solid #E3DFD6;text-align:center;padding:24px;font-size:13px;color:#9A9385;margin-top:60px}
</style>
</head>
<body>
<header>
  <h1>Studio OS</h1>
  <span>Visual Kit · Data Graphics Generator</span>
</header>
<main>
  <h2>Generate a data graphic</h2>
  <p class="sub">Paste a JSON spec below (vbar or hbar template), choose your outputs, and hit Generate.<br>You'll get a 4K PNG and optionally an animated 1080p MP4.</p>

  <div class="chip-row">
    <span class="chip s-verified">verified</span>
    <span class="chip s-reported">reported</span>
    <span class="chip s-officialclaim">officialclaim</span>
    <span class="chip s-estimate">estimate</span>
    <span class="chip s-analysis">analysis</span>
    <span class="chip s-unverified">unverified</span>
  </div>

  <div class="ex-label">Load an example spec:</div>
  <div class="examples">
    <button class="ex-btn" onclick="loadExample('vbar')">vbar — Hormuz Flows</button>
    <button class="ex-btn" onclick="loadExample('hbar')">hbar — Bypass Capacity</button>
  </div>

  <form id="form" onsubmit="generate(event)">
    <label for="spec">JSON Spec</label>
    <textarea id="spec" name="spec" placeholder='{"type":"vbar","name":"my_chart", ...}'></textarea>

    <div class="opts">
      <label><input type="checkbox" id="want_png" checked> PNG (4K still)</label>
      <label><input type="checkbox" id="want_mp4" checked> MP4 (animated, only if spec has "motion":true)</label>
    </div>

    <button type="submit" id="btn">Generate</button>
  </form>

  <div id="status"></div>
  <div id="results"></div>
  <div class="preview" id="preview"></div>
</main>
<footer>STUDIO OS Visual Kit &mdash; open-source, data graphics for journalists &amp; researchers</footer>

<script>
const EXAMPLES = {
  vbar: {{ vbar_example | tojson }},
  hbar: {{ hbar_example | tojson }}
};

function loadExample(k) {
  document.getElementById('spec').value = JSON.stringify(EXAMPLES[k], null, 2);
}

async function generate(e) {
  e.preventDefault();
  const btn = document.getElementById('btn');
  const status = document.getElementById('status');
  const results = document.getElementById('results');
  const preview = document.getElementById('preview');
  
  btn.disabled = true;
  results.innerHTML = '';
  preview.innerHTML = '';
  status.className = 's-loading';
  status.style.display = 'block';
  status.textContent = 'Rendering… this takes 15–40 seconds (Playwright is launching a headless browser)';

  try {
    const spec = document.getElementById('spec').value;
    JSON.parse(spec); // validate JSON first
    
    const want_mp4 = document.getElementById('want_mp4').checked;
    
    const res = await fetch('/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({spec: JSON.parse(spec), want_mp4})
    });
    
    const data = await res.json();
    
    if (!res.ok || data.error) {
      status.className = 's-err';
      status.textContent = 'Error: ' + (data.error || 'Unknown error');
    } else {
      status.className = 's-ok';
      status.textContent = 'Done! Your files are ready to download.';
      
      let html = '';
      if (data.png) html += `<a class="dl-btn" href="${data.png}" download>⬇ Download PNG</a>`;
      if (data.mp4) html += `<a class="dl-btn mp4" href="${data.mp4}" download>⬇ Download MP4</a>`;
      results.innerHTML = html;
      
      if (data.png) {
        preview.innerHTML = `<p style="font-size:12px;color:#6F6B63;margin-bottom:8px;letter-spacing:.1em;text-transform:uppercase">Preview</p><img src="${data.png}" alt="Generated chart">`;
      }
    }
  } catch (err) {
    status.className = 's-err';
    status.textContent = 'Error: ' + err.message;
  }
  
  btn.disabled = false;
}
</script>
</body>
</html>
"""

import importlib, sys

@app.route("/")
def index():
    # Load example specs
    specs_dir = os.path.join(ROOT, "specs")
    vbar_ex = json.load(open(os.path.join(specs_dir, "ep001_hormuz_flows.json"), encoding="utf-8"))
    hbar_ex = json.load(open(os.path.join(specs_dir, "ep001_bypass_capacity.json"), encoding="utf-8"))
    return render_template_string(HTML, vbar_example=vbar_ex, hbar_example=hbar_ex)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    sp = data.get("spec")
    want_mp4 = data.get("want_mp4", True)

    if not sp or "type" not in sp or "name" not in sp:
        return jsonify(error="Spec must have 'type' and 'name' fields."), 400

    # Sanitize name to prevent path traversal
    name = "".join(c for c in sp["name"] if c.isalnum() or c in "_-")
    sp["name"] = name

    try:
        sys.path.insert(0, ROOT)
        import studio
        t = importlib.import_module("templates." + sp["type"])
        html, dur = t.build(sp)

        result = {}

        # Render PNG
        out_png = studio.render(html, name)
        # Serve from /out/ route
        result["png"] = f"/out/{os.path.basename(out_png)}"

        # Render MP4 if wanted and spec has motion
        if want_mp4 and sp.get("motion"):
            out_mp4 = studio.animate(html, name, duration=dur)
            result["mp4"] = f"/out/{os.path.basename(out_mp4)}"

        return jsonify(result)

    except Exception:
        return jsonify(error=traceback.format_exc()), 500


@app.route("/out/<path:filename>")
def serve_out(filename):
    out_dir = os.path.join(ROOT, "out")
    return send_file(os.path.join(out_dir, filename))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
