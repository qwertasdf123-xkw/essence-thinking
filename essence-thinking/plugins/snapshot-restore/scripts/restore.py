#!/usr/bin/env python3
"""restore.py — 思维状态恢复引导。

按 wiki 加载协议输出应读取清单（不读内容，只列计划）。
用法: restore.py --workspace <路径> [--level 0|1|2]
退出码：0=清单完整；2=无 .essence（新项目）。
"""
import argparse
import glob
import os
import sys

EST = {"snapshot": 500, "moc": 800, "patterns": 1500, "log": 400}


def main() -> int:
    ap = argparse.ArgumentParser(description="思维状态恢复引导")
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--level", type=int, default=2, choices=[0, 1, 2])
    args = ap.parse_args()

    root = os.path.join(args.workspace, ".essence")
    wiki = os.path.join(root, "wiki")
    snap = os.path.join(wiki, "snapshots", "latest.md")

    if not os.path.isdir(root):
        print("未找到 .essence/ —— 新项目，无需恢复（首次 Evolve 后自动建立）")
        return 2

    print("=== 应读取清单（按序执行，每级有明确理由再升级）===")

    if os.path.isfile(snap):
        print(f"L0 [{EST['snapshot']} tok] {snap}\n    ↑ 永远先读：项目当前状态")
    else:
        print("L0 （无 snapshot —— 项目尚无沉淀）")

    if args.level >= 1:
        mocs = sorted(glob.glob(os.path.join(wiki, "moc", "*.md")))
        for m in mocs:
            print(f"L1 [+{EST['moc']} tok] {m}")
        if not mocs:
            print("L1 （无 moc 索引）")

    if args.level >= 2:
        p = os.path.join(root, "patterns.md")
        if os.path.isfile(p):
            print(f"L2 [+{EST['patterns']} tok] {p}")
        logs = sorted(glob.glob(os.path.join(root, "logs", "*.md")),
                      key=os.path.getmtime, reverse=True)[:3]
        for l in logs:
            print(f"L2 [+{EST['log']} tok] {l}（近期日志）")

    inbox = glob.glob(os.path.join(wiki, "inbox", "*.md"))
    print(f"\n旁路：inbox 有 {len(inbox)} 条未消化分支（≥20 需清空仪式）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
