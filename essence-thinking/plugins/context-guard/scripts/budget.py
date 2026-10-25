#!/usr/bin/env python3
"""budget.py — 上下文预算守卫。

用法:
  budget.py [--total N] [--threshold 0.8] [--used "名称:tokens" ...] [--manifest 文件]

manifest 文件格式：每行 "名称 tokens"（tokens 为整数）。
退出码：预算内 0；达阈值 1（告警，需压缩后继续）。
"""
import argparse
import sys

CHECKLIST = [
    "1. snapshot 已刷新到最新状态",
    "2. 当前结论已写入 moc 或 patterns",
    "3. 被委托 skill 的中间产物已落盘，上下文只留 1 行摘要",
    "4. 未消化 inbox 已写盘",
    "5. 原始查询/需求仍保留",
    "6. 没有未保存的中间状态",
    "7. 压缩后按 L0 重新加载",
]


def parse_manifest(path: str) -> list[tuple[str, int]]:
    items = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        name, _, tok = line.rpartition(" ")
        if tok.isdigit():
            items.append((name.strip(), int(tok)))
    return items


def parse_used(pairs: list[str]) -> list[tuple[str, int]]:
    items = []
    for p in pairs:
        name, _, tok = p.rpartition(":")
        if not tok.isdigit():
            print(f"警告：无法解析 '{p}'，跳过（应为 名称:tokens）", file=sys.stderr)
            continue
        items.append((name.strip(), int(tok)))
    return items


def main() -> int:
    ap = argparse.ArgumentParser(description="上下文预算守卫")
    ap.add_argument("--total", type=int, default=12000)
    ap.add_argument("--threshold", type=float, default=0.8)
    ap.add_argument("--used", nargs="*", default=[])
    ap.add_argument("--manifest", default="")
    args = ap.parse_args()

    items = parse_used(args.used)
    if args.manifest:
        items += parse_manifest(args.manifest)

    used = sum(n for _, n in items)
    pct = used / args.total if args.total else 1.0
    limit = int(args.total * args.threshold)

    print(f"上下文预算：{used} / {args.total} tok（{pct:.0%}，阈值 {args.threshold:.0%} = {limit} tok）")
    if items:
        print("明细（按占用排序）：")
        for name, n in sorted(items, key=lambda x: -x[1]):
            print(f"  {n:>6}  {name}")

    if used >= limit:
        print("\n⚠ 已达阈值：压缩后再加载。检查清单：")
        for line in CHECKLIST:
            print("  " + line)
        return 1
    print(f"\n✓ 余量 {args.total - used} tok，可继续加载")
    return 0


if __name__ == "__main__":
    sys.exit(main())
