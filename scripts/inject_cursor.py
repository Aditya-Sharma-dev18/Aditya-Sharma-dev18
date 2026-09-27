#!/usr/bin/env python3
"""
Injects a blinking terminal-cursor prompt and a card fade-in animation
into a freshly-downloaded gh-ascii SVG card.

Usage: python3 scripts/inject_cursor.py dark_mode.svg
(edits the file in place)
"""
import sys

def inject(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already injected (avoid double-injecting on re-runs)
    if 'id="blink-cursor"' in content:
        return

    cursor_block = '''  <text x="482.4" y="470" font-family="'Consolas', 'Menlo', 'DejaVu Sans Mono', monospace" xml:space="preserve" font-size="16"><tspan fill="#58a6ff">$ </tspan><tspan fill="#c9d1d9">whoami</tspan></text>
  <rect id="blink-cursor" x="559" y="458" width="10" height="18" fill="#58a6ff">
    <animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.4;0.5;0.9;1" dur="1.2s" repeatCount="indefinite"/>
  </rect>
'''
    content = content.replace("</svg>", cursor_block + "</svg>")

    # Fade the whole card in on load
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
