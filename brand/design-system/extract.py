#!/usr/bin/env python3
"""Balancia design system: balancia.css (+ inherited app tokens) -> tokens.json -> index.html.

    python3 brand/design-system/extract.py           # regenerate
    python3 brand/design-system/extract.py --check   # fail if tokens.json is stale or a claim is false

Sources, in order of authority:
  1. app.balancia/src/styles/theme/themes/balancia.css — Balancia's colours and type (the theme; see its
     header). Moved there from brand/design-system/ by step 3 of the rename (rnc-4, 16/11/2026): the
     app's copy is the source, and this script only reads it.
  2. the app's bootstrap tokens on the rnc-4 branch (radius, shadow, state colours, motion),
     read with `git show` so nothing has to be checked out. Balancia does not override them.

Checks before writing: the primary ramp equals brandPalette(teal, mint) as the app computes it,
and every "N:1" contrast written in a usage comment is re-measured.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent
REPO = BRAND.parent
sys.path.insert(0, str(HERE))
from palette import brand_palette, contrast  # noqa: E402

APP_REF = "feature/rnc-4-white-label-platform"
INHERITED = {
    "radius": ("app.balancia/src/styles/theme/themes/battoni-dev.css", r"--radius-[a-z]+"),
    "shadow": ("app.balancia/src/styles/theme/themes/battoni-dev.css", r"--shadow-(?:sm|md|lg|xl)"),
    "state": ("app.balancia/src/styles/theme/themes/battoni-dev.css", r"--color-(?:success|info|warn|danger)-500"),
    "motion": ("app.balancia/src/styles/tailwind.css", r"--motion-[a-z-]+"),
}
THEME = REPO / "app.balancia" / "src" / "styles" / "theme" / "themes" / "balancia.css"
DECL = re.compile(r"(--[\w-]+):\s*([^;]+);(?:\s*/\*\s*usage:\s*(.*?)\s*\*/)?")


def parse_blocks(css: str) -> dict[str, list[dict]]:
    """Split balancia.css into light and dark tokens, keeping each value's usage comment.

    The app's copy has three blocks: `:root` (brand and type, every screen), `:root[data-platform]`
    (ramp and neutrals, Balancia's own screens) and `:root[data-platform][data-theme='dark']`. The
    first two are the light set, in order; the dark block is the dark set.
    """
    blocks = {"light": [], "dark": []}
    pattern = r"(:root(?:\[data-platform\])?(?:\[data-theme='dark'\])?)\s*\{(.*?)\n\}"
    for selector, body in re.findall(pattern, css, re.S):
        key = "dark" if "dark" in selector else "light"
        blocks[key] += [{"name": n, "value": v.strip(), "usage": u or ""} for n, v, u in DECL.findall(body)]
    return blocks


def inherited() -> dict[str, list[dict]]:
    out = {}
    for family, (path, pattern) in INHERITED.items():
        try:
            text = subprocess.run(["git", "-C", str(REPO), "show", f"{APP_REF}:{path}"],
                                  check=True, capture_output=True, text=True).stdout
        except subprocess.CalledProcessError:
            sys.exit(f"cannot read {APP_REF}:{path} — fetch the branch or update INHERITED")
        seen, tokens = set(), []
        for name, value in re.findall(rf"({pattern}):\s*([^;]+);", text):
            if name in seen or "var(" in value:   # keep the base value, not the reduced-motion remap
                continue
            seen.add(name)
            tokens.append({"name": name, "value": " ".join(value.split()),
                           "usage": f"inherited from the bootstrap ({path})"})
        out[family] = tokens
    return out


def check(blocks: dict[str, list[dict]]) -> list[str]:
    errors = []
    light = {t["name"]: t["value"] for t in blocks["light"]}
    dark = {**light, **{t["name"]: t["value"] for t in blocks["dark"]}}
    expected = brand_palette(light["--brand-teal"], light["--brand-mint"])
    for name, value in expected.items():
        if light.get(name, "").lower() != value:
            errors.append(f"{name} is {light.get(name)}, brandPalette gives {value}")
    for scheme, values in (("light", light), ("dark", dark)):
        canvas = values["--color-canvas"]
        for t in blocks[scheme]:
            for claimed, ground in re.findall(r"(\d+\.\d+):1 on ([\w#-]+)", t["usage"]):
                ground_hex = ground if ground.startswith("#") else (
                    "#ffffff" if ground == "white" else values.get(f"--color-{ground}", canvas))
                measured = contrast(t["value"], ground_hex)
                if abs(measured - float(claimed)) > 0.02:
                    errors.append(f"{scheme} {t['name']}: claims {claimed}:1 on {ground}, measures {measured:.2f}")
    return errors


def tokens_json(blocks, inh) -> dict:
    def contrast_note(tok, ground):
        if re.fullmatch(r"#[0-9a-fA-F]{6}", tok["value"]):
            return dict(tok, contrast_on_canvas=round(contrast(tok["value"], ground), 2))
        return tok
    light_canvas = "#ffffff"
    dark_canvas = next(t["value"] for t in blocks["dark"] if t["name"] == "--color-canvas")
    colour_light = [contrast_note(t, light_canvas) for t in blocks["light"] if t["name"].startswith(("--color", "--brand"))]
    colour_dark = [contrast_note(t, dark_canvas) for t in blocks["dark"]]
    fonts = [t for t in blocks["light"] if t["name"].startswith("--font")]
    return {
        "name": "Balancia",
        "generated_by": "brand/design-system/extract.py — do not edit",
        "color": {"themes": [
            {"name": "light", "tokens": colour_light},
            {"name": "dark", "tokens": colour_dark},
        ]},
        "type": {
            "fonts": [{"name": "Manrope", "source": "assets/fonts/Manrope-Variable.ttf (OFL)",
                       "weights": [400, 500, 600, 700, 800]}],
            "families": {"tokens": fonts},
            "groups": [
                {"name": "display", "size": "48px", "weight": 800, "line_height": 1.1, "usage": "site hero, pitch titles"},
                {"name": "h1", "size": "32px", "weight": 700, "line_height": 1.2, "usage": "page titles"},
                {"name": "h2", "size": "24px", "weight": 700, "line_height": 1.25, "usage": "section titles"},
                {"name": "h3", "size": "18px", "weight": 600, "line_height": 1.35, "usage": "card titles"},
                {"name": "body", "size": "14px", "weight": 400, "line_height": 1.55, "usage": "UI text (the app's base size)"},
                {"name": "label", "size": "13px", "weight": 500, "line_height": 1.4, "usage": "labels, buttons"},
                {"name": "caption", "size": "12px", "weight": 500, "line_height": 1.4, "usage": "the floor: nothing smaller"},
                {"name": "figure", "size": "inherit", "weight": 700, "line_height": 1, "usage": "the number that matters (R$, clients, %), tabular-nums"},
            ],
        },
        "radius": {"tokens": inh["radius"]},
        "shadow": {"tokens": inh["shadow"]},
        "state": {"tokens": inh["state"]},
        "motion": {"tokens": inh["motion"]},
        "assets": {"logo": sorted(p.name for p in (HERE / "assets/logo").glob("*.svg"))},
    }


PAGE = """<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>[Battoni Dev] [Balancia] Design system</title>
<link rel="icon" href="assets/logo/balancia-icon.svg">
<style>
@font-face{{font-family:Manrope;src:url(assets/fonts/Manrope-Variable.ttf);font-weight:200 800}}
:root{{{light_vars}}}
[data-theme='dark']{{{dark_vars}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--color-canvas);color:var(--color-body);font:14px/1.55 var(--font-sans);
  transition:background var(--motion-quick) ease-out,color var(--motion-quick) ease-out}}
main{{margin:0 auto;padding:40px 48px 80px;max-width:1280px}}
h1,h2,h3{{color:var(--color-heading);margin:0}} h2{{font-size:24px;margin:56px 0 6px}} h3{{font-size:16px;margin:0 0 8px}}
p.lede{{color:var(--color-muted);margin:0 0 20px}}
header{{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:28px 0 8px}}
.logo-light{{display:block}} .logo-dark{{display:none}}
[data-theme='dark'] .logo-light{{display:none}} [data-theme='dark'] .logo-dark{{display:block}}
button.toggle{{font:600 13px var(--font-sans);border:1px solid var(--color-line-strong);background:var(--color-panel);
  color:var(--color-heading);border-radius:8px;padding:8px 14px;cursor:pointer;transition:background var(--motion-quick) ease-out}}
button.toggle:hover{{background:var(--color-panel-muted)}}
.grid{{display:grid;gap:14px}} .g4{{grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}} .g2{{grid-template-columns:1fr 1fr}}
.card{{background:var(--color-panel);border:1px solid var(--color-line);border-radius:12px;padding:16px}}
.sw{{height:64px;border-radius:8px;border:1px solid var(--color-line);margin-bottom:10px}}
.tok{{font:12px var(--font-mono);color:var(--color-muted)}} .use{{font-size:12px;color:var(--color-muted)}}
.ratio{{font:600 12px var(--font-mono);color:var(--color-heading)}}
.ramp{{display:flex;border-radius:10px;overflow:hidden;border:1px solid var(--color-line)}}
.ramp div{{flex:1;height:72px;display:flex;align-items:flex-end;padding:6px;font:11px var(--font-mono)}}
.stage{{display:flex;align-items:center;justify-content:center;border-radius:12px;padding:36px;min-height:180px}}
.stage.l{{background:#ffffff;border:1px solid var(--color-line)}} .stage.d{{background:#0b1416}}
.clear{{outline:2px dashed #2fb7a3;outline-offset:18px}}
.row{{display:flex;gap:24px;align-items:flex-end;flex-wrap:wrap}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.yes,.no{{border-radius:10px;padding:12px 14px;font-size:13px}}
.yes{{background:var(--color-primary-50);color:#0f1f20;border-left:4px solid var(--color-primary-500)}}
.no{{background:var(--color-panel-muted);color:var(--color-muted);border-left:4px solid var(--color-line-strong);text-decoration:line-through}}
[data-theme='dark'] .yes{{background:var(--color-primary-900);color:var(--color-heading);border-left-color:var(--color-primary-300)}}
.demo{{height:44px;width:44px;border-radius:10px;background:var(--color-primary-500)}}
.demo.a{{animation:rise var(--motion-calm) cubic-bezier(0.32,0.72,0,1) infinite alternate}}
@keyframes rise{{from{{transform:translateY(8px);opacity:.4}}to{{transform:none;opacity:1}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
ul.check li{{margin:6px 0}}
.shot{{background:var(--color-primary-50);border-radius:12px;padding:28px}}
.shot div{{background:#fff;border-radius:12px;border:1px solid #d3dede;height:120px;box-shadow:0 1px 2px rgb(10 10 9 / .06)}}
</style></head><body><main>
<header>
  <div><img class="logo-light" src="assets/logo/balancia-logo.svg" alt="Balancia" height="56">
       <img class="logo-dark" src="assets/logo/balancia-logo-dark.svg" alt="Balancia" height="56"></div>
  <button class="toggle" onclick="var h=document.documentElement;h.dataset.theme=h.dataset.theme==='dark'?'light':'dark'">Light / dark</button>
</header>
<p class="lede">Design system v1 · 16/11/2026 · generated by <code>brand/design-system/extract.py</code> from <code>app.balancia/src/styles/theme/themes/balancia.css</code>. The rules are in <code>brand/SYSTEM.md</code>.</p>

<h2>Colour</h2><p class="lede">Contrast measured against the canvas of the current scheme. Toggle the scheme to see the other.</p>
<div class="ramp">{ramp}</div><br>
<div class="grid g4">{swatches}</div>
<div class="grid g4" style="margin-top:14px">{states}</div>

<h2>Type</h2><p class="lede">Manrope everywhere. 12px is the floor.</p>
<div class="card">{type}</div>

<h2>Radius, relief, motion</h2><p class="lede">Inherited from the bootstrap; Balancia does not override them.</p>
<div class="grid g4">{radius}</div><br>
<div class="grid g4">{motion}</div>

<h2>The mark</h2><p class="lede">Full lockup and icon, on light and on dark. The dashed line is the clear space (0.25 × icon height). Minimum: lockup 20px tall, icon 16px.</p>
<div class="grid g2">
  <div class="stage l"><img class="clear" src="assets/logo/balancia-logo.svg" height="72" alt=""></div>
  <div class="stage d"><img class="clear" src="assets/logo/balancia-logo-dark.svg" height="72" alt=""></div>
  <div class="stage l"><div class="row"><img src="assets/logo/balancia-icon.svg" width="96" alt=""><img src="assets/logo/balancia-icon.svg" width="32" alt=""><img src="assets/logo/balancia-icon.svg" width="16" alt=""><img src="assets/logo/balancia-logo.svg" height="20" alt=""></div></div>
  <div class="stage d"><div class="row"><img src="assets/logo/balancia-icon-dark.svg" width="96" alt=""><img src="assets/logo/balancia-icon-dark.svg" width="32" alt=""><img src="assets/logo/balancia-icon-dark.svg" width="16" alt=""><img src="assets/logo/balancia-logo-dark.svg" height="20" alt=""></div></div>
</div>

<h2>Voice</h2><p class="lede">"Você", direct and calm. Lead with the number. No humour, no emoji in the product.</p>
<div class="grid" style="gap:10px">{voice}</div>

<h2>Imagery</h2><p class="lede">Real screenshots on a soft teal tint, 12px radius, no tilt, no glow. Photos only of real customers.</p>
<div class="grid g2"><div class="shot"><div></div></div><div class="card"><h3>Never</h3>Stock photos of accountants · 3D-tilted mockups · Reforma, flag or government imagery · glowing gradients</div></div>

<h2>Icons and motion</h2><p class="lede">Font Awesome 7 Regular; Solid only for the active state. 150–200ms ease-out. With reduced motion, nothing moves and everything still works.</p>
<div class="row"><div class="demo a"></div><div class="use">quick 180ms · calm 320ms · settle curve cubic-bezier(0.32, 0.72, 0, 1)</div></div>

<h2>Delivery checklist</h2>
<div class="card"><ul class="check">{checklist}</ul></div>
</main></body></html>
"""

VOICE = [
    ("Não conseguimos salvar o reajuste. Seus dados estão intactos; tente de novo em instantes.",
     "Erro 500: falha ao processar a requisição."),
    ("Carta pronta: 42 clientes, R$ 18.300 a mais por ano.", "Prontinho! 🎉 Sua carta foi gerada com sucesso!"),
    ("3 contatos novos esta semana. Marina, da Padaria Alvorada, marcou reunião para quinta.",
     "Bora vender mais! Seu funil está bombando 🚀"),
]
CHECKLIST = [
    "Every text pair measured: 4.5:1 (3:1 for icons and large text), in light and in dark",
    "Only tokens: no loose hex, no framework default palette",
    "Manrope, 12px or larger; figures in tabular numbers",
    "The logo is a file from assets/logo, at 16px or larger, with its clear space, on its matching ground",
    "Voice: você, number first, no humour, no emoji, glossary words (escritório, contato, reajuste de honorários, diagnóstico)",
    "Images: real screenshots or real customers only",
    "Works with prefers-reduced-motion: nothing moves, nothing breaks",
    "Nothing says Reforma as brand, nothing says grátis, nothing looks like government",
]


def plain(usage: str) -> str:
    """Usage without its written ratios: the page measures contrast live, per scheme."""
    return re.sub(r" ?\([^)]*:1[^)]*\)", "", usage)


def vars_css(tokens) -> str:
    return "".join(f"{t['name']}:{t['value']};" for t in tokens)


def page(data, blocks) -> str:
    light = {t["name"]: t for t in blocks["light"]}
    ramp = "".join(
        f'<div style="background:{light[f"--color-primary-{k}"]["value"]};color:{"#0f1f20" if int(k) < 400 else "#ffffff"}">{k}</div>'
        for k in ("50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"))
    names = ["--brand-teal", "--brand-mint", "--color-canvas", "--color-panel", "--color-panel-muted", "--color-heading",
             "--color-body", "--color-muted", "--color-subtle", "--color-line", "--color-line-strong"]
    swatches = "".join(
        f'<div class="card"><div class="sw" style="background:var({n})"></div><div class="tok">{n}</div>'
        f'<div class="ratio" data-c="{n}"></div><div class="use">{plain(light[n]["usage"])}</div></div>' for n in names)
    states = "".join(f'<div class="card"><div class="sw" style="background:{t["value"]}"></div><div class="tok">{t["name"]} {t["value"]}</div></div>'
                     for t in data["state"]["tokens"])
    type_ = "".join(f'<div style="font-size:{g["size"] if g["size"] != "inherit" else "28px"};font-weight:{g["weight"]};line-height:{g["line_height"]};'
                    f'color:var(--color-heading);margin:10px 0">{"R$ 18.300" if g["name"] == "figure" else "Escritório que cresce"} '
                    f'<span class="tok">{g["name"]} · {g["size"]} / {g["weight"]}</span></div>' for g in data["type"]["groups"])
    radius = "".join(f'<div class="card"><div style="height:56px;background:var(--color-primary-50);border:1px solid var(--color-primary-200);border-radius:{t["value"]}"></div><div class="tok">{t["name"]} {t["value"]}</div></div>'
                     for t in data["radius"]["tokens"])
    motion = "".join(f'<div class="card"><div class="tok">{t["name"]}</div><div class="ratio">{t["value"]}</div></div>' for t in data["motion"]["tokens"])
    voice = "".join(f'<div class="pair"><div class="yes">{y}</div><div class="no">{n}</div></div>' for y, n in VOICE)
    script = """<script>
function lum(h){h=h.trim().replace('#','');return [0,2,4].map(i=>{let c=parseInt(h.substr(i,2),16)/255;return c<=0.03928?c/12.92:((c+0.055)/1.055)**2.4}).reduce((a,c,i)=>a+c*[0.2126,0.7152,0.0722][i],0)}
function cr(a,b){let x=lum(a),y=lum(b);if(x<y)[x,y]=[y,x];return ((x+0.05)/(y+0.05)).toFixed(2)}
function paint(){const s=getComputedStyle(document.documentElement),bg=s.getPropertyValue('--color-canvas');
document.querySelectorAll('[data-c]').forEach(e=>{e.textContent=cr(s.getPropertyValue(e.dataset.c),bg)+':1 on canvas'})}
paint();new MutationObserver(paint).observe(document.documentElement,{attributes:true});
</script>"""
    motion_vars = vars_css([t for t in data["motion"]["tokens"]])
    return PAGE.format(
        light_vars=vars_css(blocks["light"]) + motion_vars,
        dark_vars=vars_css(blocks["dark"]),
        ramp=ramp, swatches=swatches, states=states, type=type_, radius=radius, motion=motion, voice=voice,
        checklist="".join(f"<li>{c}</li>" for c in CHECKLIST),
    ).replace("</main></body>", "</main>" + script + "</body>")


def main() -> None:
    blocks = parse_blocks(THEME.read_text())
    errors = check(blocks)
    if errors:
        sys.exit("balancia.css claims that do not hold:\n  " + "\n  ".join(errors))
    data = tokens_json(blocks, inherited())
    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    target = HERE / "tokens.json"
    if "--check" in sys.argv:
        if not target.exists() or target.read_text() != rendered:
            sys.exit("tokens.json is stale: run python3 brand/design-system/extract.py")
        print("tokens.json is current; all contrast claims and the ramp hold")
        return
    target.write_text(rendered)
    (HERE / "index.html").write_text(page(data, blocks))
    print(f"tokens.json + index.html written ({sum(len(t['tokens']) for t in data['color']['themes'])} colour tokens)")


if __name__ == "__main__":
    main()
