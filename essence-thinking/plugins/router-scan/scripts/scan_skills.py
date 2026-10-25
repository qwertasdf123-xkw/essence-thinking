#!/usr/bin/env python3
"""scan_skills.py — 本机 skill 索引扫描。

扫描各 skills 根目录下的 SKILL.md，提取 name/description，
生成 .essence/index/skills-index.md 供路由层 R1 语义匹配。
用法: scan_skills.py --workspace <路径> [--roots <dir> ...]
"""
import argparse
import os
import re
import sys
from datetime import date

DEFAULT_ROOTS = [
    os.path.expanduser(r"~\.codex\skills"),
    os.path.expanduser(r"~\.dsh\skills"),
    os.path.expanduser(r"~\.kimi\skills"),
]

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def parse_frontmatter(path: str) -> tuple[str, str]:
    text = open(path, encoding="utf-8", errors="replace").read(8192)
    m = FM_RE.match(text)
    if not m:
        return "", ""
    name = desc = ""
    for line in m.group(1).splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
        elif line.startswith("description:"):
            desc = line.split(":", 1)[1].strip()
    return name, desc


def main() -> int:
    ap = argparse.ArgumentParser(description="本机 skill 索引扫描")
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--roots", nargs="*", default=None)
    args = ap.parse_args()

    roots = args.roots if args.roots else DEFAULT_ROOTS + [
        os.path.join(args.workspace, ".agents", "skills")]
    entries = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for sub in sorted(os.listdir(root)):
            skill_md = os.path.join(root, sub, "SKILL.md")
            if os.path.isfile(skill_md):
                name, desc = parse_frontmatter(skill_md)
                entries.append((root, name or sub, desc))

    if not entries:
        print("未发现任何 skill（检查 --roots 路径）")
        return 1

    out_dir = os.path.join(args.workspace, ".essence", "index")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "skills-index.md")

    lines = [f"# 本机 Skill 索引 · {date.today().isoformat()}",
             "\n> 由 router-scan 插件生成，供路由层 R1 语义匹配。索引过期时 R1 降级 R2。\n"]
    cur_root = None
    for root, name, desc in entries:
        if root != cur_root:
            lines.append(f"\n## {root}\n")
            cur_root = root
        short = desc[:150] + ("…" if len(desc) > 150 else "")
        lines.append(f"- **{name}** — {short}")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")

    print(f"索引完成：{len(entries)} 个 skill → {out}")
    for root, name, _ in entries:
        print(f"  [{os.path.basename(root)}] {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
