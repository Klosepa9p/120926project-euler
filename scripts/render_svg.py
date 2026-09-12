#!/usr/bin/env python3
"""
data/solved.json içindeki listeye göre euler-progress.svg üretir.
Project Euler'e hiç bağlanmaz — tamamen yerel veriden çalışır.
"""
import json
import os

CELL = 22
GAP = 2
BLOCK_PAD = 8
BLOCK_GAP = 18
BLOCKS_PER_ROW = 4
HEADER_H = 46
FOOTER_H = 26

COLOR_BG = "#0d1117"
COLOR_SOLVED = "#1fb6c9"
COLOR_SOLVED_TEXT = "#04262b"
COLOR_UNSOLVED = "#21262d"
COLOR_UNSOLVED_TEXT = "#7d8590"
COLOR_BORDER = "#30363d"
COLOR_TITLE = "#e6edf3"
COLOR_SUB = "#8b949e"


def build_svg(solved_set: set[int], max_n: int, username: str) -> str:
    solved_count = len(solved_set)
    n_blocks = (max_n + 99) // 100
    block_w = 10 * CELL + 9 * GAP + 2 * BLOCK_PAD
    block_h = block_w
    n_rows = (n_blocks + BLOCKS_PER_ROW - 1) // BLOCKS_PER_ROW
    width = BLOCKS_PER_ROW * block_w + (BLOCKS_PER_ROW - 1) * BLOCK_GAP
    height = HEADER_H + n_rows * block_h + (n_rows - 1) * BLOCK_GAP + FOOTER_H

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Segoe UI, Helvetica, Arial, sans-serif">',
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="10" fill="{COLOR_BG}"/>',
    ]
    title = f"Project Euler Progress — {username}" if username else "Project Euler Progress"
    parts.append(f'<text x="16" y="28" fill="{COLOR_TITLE}" font-size="17" font-weight="600">{title}</text>')

    for b in range(n_blocks):
        row, col = divmod(b, BLOCKS_PER_ROW)
        bx = col * (block_w + BLOCK_GAP)
        by = HEADER_H + row * (block_h + BLOCK_GAP)
        parts.append(
            f'<rect x="{bx}" y="{by}" width="{block_w}" height="{block_h}" rx="6" '
            f'fill="none" stroke="{COLOR_BORDER}" stroke-width="1"/>'
        )
        for i in range(100):
            n = b * 100 + i + 1
            if n > max_n:
                break
            r, c = divmod(i, 10)
            x = bx + BLOCK_PAD + c * (CELL + GAP)
            y = by + BLOCK_PAD + r * (CELL + GAP)
            solved = n in solved_set
            fill = COLOR_SOLVED if solved else COLOR_UNSOLVED
            text_fill = COLOR_SOLVED_TEXT if solved else COLOR_UNSOLVED_TEXT
            font_size = 9.5 if n < 1000 else 7.6
            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="4" fill="{fill}">'
                f"<title>Problem {n} — {'Solved' if solved else 'Unsolved'}</title></rect>"
            )
            parts.append(
                f'<text x="{x + CELL / 2}" y="{y + CELL / 2 + 3.5}" text-anchor="middle" '
                f'font-size="{font_size}" fill="{text_fill}">{n}</text>'
            )

    footer_y = HEADER_H + n_rows * block_h + (n_rows - 1) * BLOCK_GAP + 18
    parts.append(
        f'<text x="16" y="{footer_y}" fill="{COLOR_SUB}" font-size="12">'
        f"Solved {solved_count} / {max_n}</text>"
    )
    parts.append("</svg>")
    return "".join(parts)


def main() -> None:
    with open("data/solved.json", encoding="utf-8") as f:
        data = json.load(f)

    solved_set = set(data.get("solved", []))
    max_n = int(data.get("max_n", 1010))
    username = data.get("username", "")

    svg = build_svg(solved_set, max_n, username)

    with open("euler-progress.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Yazıldı: euler-progress.svg ({len(solved_set)}/{max_n})")


if __name__ == "__main__":
    main()
