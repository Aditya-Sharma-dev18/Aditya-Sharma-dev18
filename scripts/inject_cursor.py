#!/usr/bin/env python3
"""
Injects into a freshly-downloaded gh-ascii SVG card:
  1. A line-by-line reveal animation on the ASCII portrait (left side)
  2. A blinking terminal-cursor prompt under the stats panel (right side)
  3. A fade-in on the outer card border

Usage: python3 scripts/inject_cursor.py dark_mode.svg
(edits the file in place)
"""
import re
import sys

PORTRAIT_BUILD_SECONDS = 2.2


def inject(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already injected (avoid double-injecting on re-runs)
    if 'id="blink-cursor"' in content:
        return

    # --- 1. Line-by-line portrait reveal ---
    pattern = re.compile(
        r'(<text x="28" y="[\d.]+" fill="#c9d1d9"[^>]*>)(.*?)(</text>)', re.DOTALL
    )
    matches = list(pattern.finditer(content))
    n = len(matches) or 1
    step = PORTRAIT_BUILD_SECONDS / n

    result = []
    last_end = 0
    for i, m in enumerate(matches):
        result.append(content[last_end:m.start()])
        open_tag, text_body, close_tag = m.group(1), m.group(2), m.group(3)
        open_tag_with_opacity = open_tag[:-1] + ' opacity="0">'
        begin = round(i * step, 3)
        dur = round(step * 1.4, 3)
        animate = (
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{begin}s" dur="{dur}s" fill="freeze"/>'
        )
        result.append(open_tag_with_opacity + text_body + animate + close_tag)
        last_end = m.end()
    result.append(content[last_end:])
    content = "".join(result)

    # --- 2. Blinking cursor prompt under the stats panel ---
    cursor_block = '''  <text x="482.4" y="470" font-family="'Consolas', 'Menlo', 'DejaVu Sans Mono', monospace" xml:space="preserve" font-size="16"><tspan fill="#58a6ff">$ </tspan><tspan fill="#c9d1d9">whoami</tspan></text>
  <rect id="blink-cursor" x="559" y="458" width="10" height="18" fill="#58a6ff">
    <animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.4;0.5;0.9;1" dur="1.2s" repeatCount="indefinite"/>
  </rect>
'''
    content = content.replace("</svg>", cursor_block + "</svg>")

    # --- 3. Fade the whole card in on load ---
    content = content.replace(
        '<rect x="0.5" y="0.5" width="1066" height="515.8" rx="8" fill="#0d1117" stroke="#30363d"/>',
        '<rect x="0.5" y="0.5" width="1066" height="515.8" rx="8" fill="#0d1117" stroke="#30363d">\n'
        '    <animate attributeName="opacity" values="0;1" dur="0.8s" fill="freeze"/>\n'
        "  </rect>",
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        inject(p)
        print(f"animated: {p}")