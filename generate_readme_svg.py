#!/usr/bin/env python3
"""Generate terminal-style SVG for GitHub profile README."""

from pathlib import Path
from html import escape

# ── ASCII portrait (left panel) ──────────────────────────────────
PORTRAIT = r"""
                 .......::::........
             .:-=+++*********++=-:.
          .:=+++***************++-=:.
        .:=++++*****************+++=:.
      .:=++++++*****************++++=:.
     .-+++++++******************+++++-.
    .-++++++++*****+++++*******++++++-.
   .-++++++++*****+--=+*******+++++++-.
   :++++++++******-  .+*******+++++++=:
  .-++++++++*****-    :********++++++-.
  :+++++++++*****=    =********++++++=:
  .-+++++++++*****-  -*********++++++-.
   :+++++++++*******+**********++++++=:
   .-+++++++++*****************++++++-.
    .-+++++++++***************++++++-.
     .-+++++++++++++++++++++++++++-.
       :-++++++++++++++++++++++-:
         .-==================-.
            ...............
""".strip().splitlines()

# ── Profile data ─────────────────────────────────────────────────
DARK = {
    "bg": "#0B1120",
    "bg_alpha": "0.85",
    "panel_bg": "#0B1120",
    "panel_alpha": "0.35",
    "border_grad1": "#7C3AED",
    "border_grad2": "#22D3EE",
    "border_grad3": "#10B981",
    "ascii_grad1": "#22D3EE",
    "ascii_grad2": "#7C3AED",
    "ascii_grad3": "#38BDF8",
    "ascii_grad4": "#22D3EE",
    "head_fill": "#7C3AED",
    "key_fill": "#22D3EE",
    "value_fill": "#E5E7EB",
    "cc_fill": "#475569",
    "accent_fill": "#10B981",
    "term_fill": "#64748B",
    "scan_fill": "#F87171",
    "panel_title": "#38BDF8",
    "cursor_fill": "#22D3EE",
    "titlebar_bg": "#0B1120",
    "scan_opacity": "0.7",
    "scan_blend": "screen",
    "scanlines_fill": "#7DD3FC",
    "scanlines_opacity": "0.05",
    "border_alpha": "0.8",
    "border_anim_low": "0.5",
    "border_anim_high": "0.95",
    "panel_border_alpha": "0.35",
    "fill_opacity_55": "0.35",
}

LIGHT = {
    "bg": "#F8FAFC",
    "bg_alpha": "0.9",
    "panel_bg": "#FFFFFF",
    "panel_alpha": "0.55",
    "border_grad1": "#7C3AED",
    "border_grad2": "#0EA5E9",
    "border_grad3": "#059669",
    "ascii_grad1": "#4F46E5",
    "ascii_grad2": "#7C3AED",
    "ascii_grad3": "#0EA5E9",
    "ascii_grad4": "#4F46E5",
    "head_fill": "#7C3AED",
    "key_fill": "#0284C7",
    "value_fill": "#1E293B",
    "cc_fill": "#94A3B8",
    "accent_fill": "#059669",
    "term_fill": "#64748B",
    "scan_fill": "#DC2626",
    "panel_title": "#0284C7",
    "cursor_fill": "#0EA5E9",
    "titlebar_bg": "#FFFFFF",
    "scan_opacity": "0.8",
    "scan_blend": "multiply",
    "scanlines_fill": "#334155",
    "scanlines_opacity": "0.035",
    "border_alpha": "0.75",
    "border_anim_low": "0.45",
    "border_anim_high": "0.9",
    "panel_border_alpha": "0.4",
    "fill_opacity_55": "0.55",
}


def make_clip_paths(count, x=500, start_y=26, line_h=24, width=690,
                    start_delay=0.75, step=0.115, duration=0.38):
    paths = []
    for i in range(count):
        y = start_y + i * line_h
        delay = round(start_delay + i * step, 3)
        paths.append(
            f'<clipPath id="lc{i}">'
            f'<rect x="{x}" y="{y:.2f}" width="0" height="{line_h}">'
            f'<animate attributeName="width" from="0" to="{width}" '
            f'dur="{duration}s" begin="{delay}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )
    return paths


def make_lines(lines_data, x=520):
    result = []
    for i, item in enumerate(lines_data):
        kind = item[0]
        if kind == "head":
            text = item[1]
            result.append(
                f'<g clip-path="url(#lc{i})">'
                f'<text x="{x}" y="0" fill="#dbeafe">'
                f'<tspan x="{x}" y="{42}" class="head">{escape(text)}</tspan>'
                f'<tspan class="cc"> '
                f'-{"—" * 54}</tspan>'
                f'</text></g>'
            )
        elif kind == "sep":
            result.append(f'<g clip-path="url(#lc{i})"><text x="{x}" y="0" '
                          f'fill="#dbeafe"><tspan x="{x}" y="{42}" '
                          f'class="cc">.'
                          f'{" " * 68}</tspan></text></g>')
        elif kind == "field":
            key, val = item[1], item[2]
            dots = "." * (25 - len(key))
            result.append(
                f'<g clip-path="url(#lc{i})"><text x="{x}" y="0" fill="#dbeafe">'
                f'<tspan x="{x}" y="{42}" class="cc">. </tspan>'
                f'<tspan class="key">{escape(key)}</tspan>'
                f'<tspan class="cc">: {dots} </tspan>'
                f'<tspan class="value">{escape(val)}</tspan>'
                f'</text></g>'
            )
        elif kind == "empty":
            result.append(f'<g clip-path="url(#lc{i})"><text x="{x}" y="0" '
                          f'fill="#dbeafe"><tspan x="{x}" y="{42}" '
                          f'class="cc">.</tspan></text></g>')
    return result


def generate_svg(theme="dark"):
    t = DARK if theme == "dark" else LIGHT

    line_height = 24
    info_lines = [
        ("head", "nikola@iammistake"),
        ("field", "Name", "Nikola Jagurinoski"),
        ("field", "Location", "Macedonia"),
        ("field", "Age", "22"),
        ("field", "GitHub", "since 2020 · 29 repos"),
        ("field", "Status", "SWE · OSS · Rustacean"),
        ("empty",),
        ("head", "stack"),
        ("field", "Languages", "Rust, Python, TypeScript, Java"),
        ("field", "Editor", "Neovim"),
        ("field", "Shell", "zsh + tmux"),
        ("field", "WM/DE", "Hyprland"),
        ("field", "Tools", "Docker, Git, Neovim"),
        ("empty",),
        ("head", "vibes"),
        ("field", "Motto", "fast software, clean interfaces"),
        ("field", "Energy", "fAround/findOut > try/catch"),
    ]

    clip_paths = make_clip_paths(len(info_lines))
    info_svg = make_lines(info_lines)

    # ASCII portrait as tspans
    ascii_y_start = 79.98
    ascii_line_h = 7.55
    tspans = []
    for li, line in enumerate(PORTRAIT):
        y = ascii_y_start + li * ascii_line_h
        tspans.append(
            f'<tspan x="30" y="{y:.2f}" xml:space="preserve">'
            f'{escape(line)}</tspan>'
        )
    ascii_block = "\n".join(tspans)

    num_info = len(info_lines)
    cursor_y = 42 + (num_info - 1) * line_height
    cursor_delay = round(0.75 + (num_info - 1) * 0.115, 3)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610">
<defs>
  <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{t['ascii_grad1']}">
      <animate attributeName="stop-color" values="{t['ascii_grad1']};{t['ascii_grad2']};{t['ascii_grad3']};{t['ascii_grad1']}" dur="9s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="{t['ascii_grad2']}">
      <animate attributeName="stop-color" values="{t['ascii_grad2']};{t['ascii_grad3']};{t['ascii_grad1']};{t['ascii_grad2']}" dur="9s" repeatCount="indefinite"/>
    </stop>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{t['border_grad1']}"/>
    <stop offset="50%" stop-color="{t['border_grad2']}"/>
    <stop offset="100%" stop-color="{t['border_grad3']}"/>
  </linearGradient>
  <radialGradient id="bgGlow" cx="30%" cy="20%" r="80%">
    <stop offset="0%" stop-color="{t['bg']}"/>
    <stop offset="100%" stop-color="{t['bg']}" stop-opacity="0.6"/>
  </radialGradient>
  <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{t['ascii_grad2']}" stop-opacity="0"/>
    <stop offset="45%" stop-color="{t['ascii_grad2']}" stop-opacity="0.05"/>
    <stop offset="50%" stop-color="{t['cursor_fill']}" stop-opacity="0.65"/>
    <stop offset="55%" stop-color="{t['ascii_grad2']}" stop-opacity="0.05"/>
    <stop offset="100%" stop-color="{t['border_grad1']}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="{t['scanlines_fill']}" opacity="{t['scanlines_opacity']}"/>
  </pattern>
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
  <mask id="revealMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1180" height="620">
    <rect x="0" y="0" width="1180" height="0" fill="#fff">
      <animate attributeName="height" from="0" to="560" dur="2.6s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
    </rect>
  </mask>
  {chr(10).join(clip_paths)}
  <style>
    .ascii  {{ font-family: 'Courier New', Consolas, monospace; font-size: 7.4px; fill: url(#asciiGrad); letter-spacing: -0.2px; }}
    .key    {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {t['key_fill']}; font-weight: bold; }}
    .value  {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {t['value_fill']}; }}
    .cc     {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {t['cc_fill']}; }}
    .head   {{ font-family: 'Courier New', Consolas, monospace; font-size: 17px; fill: {t['head_fill']}; font-weight: bold; }}
    .accent {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {t['accent_fill']}; font-weight: bold; }}
    text, tspan {{ white-space: pre; }}
    .term-label {{ font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: {t['term_fill']}; letter-spacing: 0.5px; }}
    .scan-label {{ font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: {t['scan_fill']}; letter-spacing: 1px; }}
    .panel-title {{ font-family: 'Courier New', Consolas, monospace; font-size: 11px; fill: {t['panel_title']}; letter-spacing: 2px; opacity: 0.75; }}
    .cursor-blink {{ fill: {t['cursor_fill']}; }}
  </style>
</defs>

<rect width="1180" height="610" rx="18" fill="url(#bgGlow)"/>
<rect width="1180" height="610" rx="18" fill="url(#scanlines)"/>

<g id="titlebar">
  <rect x="3" y="3" width="1174" height="34" rx="16" fill="{t['titlebar_bg']}" fill-opacity="{t['bg_alpha']}"/>
  <text x="590" y="25" text-anchor="middle" class="term-label">nikola@iammistake ~ % cat about.json</text>
</g>

<g transform="translate(0,38)">
  <rect x="14" y="26" width="488" height="468" rx="14" fill="{t['panel_bg']}" fill-opacity="{t['panel_alpha']}" stroke="url(#borderGrad)" stroke-width="1" opacity="{t['panel_border_alpha']}"/>
  <rect x="508" y="10" width="655" height="500" rx="14" fill="{t['panel_bg']}" fill-opacity="{t['panel_alpha']}" stroke="url(#borderGrad)" stroke-width="1" opacity="{t['panel_border_alpha']}"/>
  <text x="30" y="24" class="panel-title">VISUAL.MAP</text>
  <text x="524" y="24" class="panel-title">SYSTEM.INFO</text>

  <g mask="url(#revealMask)">
  <text x="30" y="0" class="ascii">
{ascii_block}
  </text>
  </g>

  {chr(10).join(info_svg)}

  <rect x="522" y="{cursor_y}" width="9" height="16" class="cursor-blink" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0" keyTimes="0;0.01;0.02;0.3;0.5;0.7;0.85;1" dur="1.4s" begin="{cursor_delay}s" repeatCount="indefinite"/>
  </rect>
</g>

<rect x="0" y="-70" width="1180" height="70" fill="url(#scanGrad)" opacity="{t['scan_opacity']}" style="mix-blend-mode:{t['scan_blend']}">
  <animateTransform attributeName="transform" type="translate" from="0 -70" to="0 680" dur="4.2s" repeatCount="indefinite"/>
</rect>

<rect x="3" y="3" width="1174" height="604" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="{t['border_alpha']}">
  <animate attributeName="opacity" values="{t['border_anim_low']};{t['border_anim_high']};{t['border_anim_low']}" dur="3.2s" repeatCount="indefinite"/>
</rect>
</svg>'''
    return svg


if __name__ == "__main__":
    Path("light.svg").write_text(generate_svg("light"), encoding="utf-8")
    Path("dark.svg").write_text(generate_svg("dark"), encoding="utf-8")
    print("Generated light.svg and dark.svg")
