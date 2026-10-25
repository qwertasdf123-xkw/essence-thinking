#!/usr/bin/env python3
"""package.py — skill 打包发布流水线（含硬校验）。

用法: package.py [--skill-dir <路径>] --version <X.Y.Z>

硬校验（任一失败即退出 1）：
  1. SKILL.md 存在且 frontmatter 含非空 name/description
  2. 目录名 == frontmatter name
  3. releases/v<版本>.md 存在且非空
通过后：更新 VERSION → 打包 .skill → 计算 SHA-256 → 输出发布指引。
"""
import argparse
import hashlib
import os
import re
import sys
import zipfile

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def fail(msg: str) -> None:
    print(f"✗ 硬校验失败：{msg}")
    sys.exit(1)


def main() -> int:
    ap = argparse.ArgumentParser(description="skill 打包发布流水线")
    ap.add_argument("--skill-dir", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    ap.add_argument("--version", required=True)
    args = ap.parse_args()

    skill_dir = os.path.abspath(args.skill_dir)
    name_dir = os.path.basename(skill_dir)
    skill_md = os.path.join(skill_dir, "SKILL.md")

    if not os.path.isfile(skill_md):
        fail(f"SKILL.md 不存在：{skill_md}")

    text = open(skill_md, encoding="utf-8").read()
    m = FM_RE.match(text)
    if not m:
        fail("SKILL.md 缺少 YAML frontmatter")
    fm = m.group(1)
    name_m = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc_m = re.search(r"^description:\s*(.+)$", fm, re.M)
    name = name_m.group(1).strip() if name_m else ""
    desc = desc_m.group(1).strip() if desc_m else ""
    if not name or not desc:
        fail("frontmatter 的 name/description 必须非空")
    if name != name_dir:
        fail(f"目录名 '{name_dir}' ≠ frontmatter name '{name}'")

    candidates = [f"v{args.version}.md"]
    if args.version.endswith(".0"):
        candidates.append(f"v{args.version[:-2]}.md")
    notes = next((os.path.join(skill_dir, "releases", c) for c in dict.fromkeys(candidates)
                  if os.path.isfile(os.path.join(skill_dir, "releases", c))), None)
    if notes is None:
        fail(f"发布说明不存在：releases/v{args.version}.md（正文唯一来源；也尝试了 {candidates}）")
    if not open(notes, encoding="utf-8").read().strip():
        fail(f"发布说明为空：{notes}（v1.1 教训：正文非空是硬校验）")

    with open(os.path.join(skill_dir, "VERSION"), "w", encoding="utf-8") as f:
        f.write(args.version + "\n")

    out = os.path.join(os.path.dirname(skill_dir), f"{name}.skill")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(skill_dir):
            for fn in files:
                p = os.path.join(root, fn)
                z.write(p, os.path.relpath(p, os.path.dirname(skill_dir)))

    digest = hashlib.sha256(open(out, "rb").read()).hexdigest()
    size = os.path.getsize(out)

    print(f"✓ 硬校验全部通过（name/description/目录名/发布说明非空）")
    print(f"✓ 包已生成：{out}")
    print(f"  版本 v{args.version} · {size/1024:.1f} KB")
    print(f"  SHA-256: {digest}")
    print(f"\n发布指引（GitHub Web，约 1 分钟）：")
    print(f"  1. Tag: v{args.version}")
    print(f"  2. 标题/正文: 必须等于 {os.path.relpath(notes, skill_dir)} 内容（禁止手贴其他文件，v1.0 教训）")
    print(f"  3. 附件: 上传上面的 .skill（发布后到 assets 校验 sha256 = {digest[:16]}…）")
    print(f"  4. 发布后跑验证：gh release view v{args.version} --json assets,body")
    return 0


if __name__ == "__main__":
    sys.exit(main())
