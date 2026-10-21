#!/usr/bin/env python3
"""et_log.py — essence-thinking 进化库写入工具。

用法:
  python et_log.py --workspace <工作区路径> --task "<任务名>" \
      [--stages "Explore,Strip,..."] [--chain "L1...|L2...|L3..."] \
      [--verdict PASS|REVISE|REJECT] [--hits "模式A,模式B"] [--patterns "新模式标题,..." ] \
      [--revision "框架修订说明"] [--trigger "用户请求摘要"]

行为:
  1. 在工作区创建 .essence/logs/YYYY-MM-DD-<slug>.md 思维日志
  2. 更新 .essence/evolution.md 进化总账（模式计数、日志计数、修订历史）
  3. 若指定 --patterns，将新模式骨架追加到 .essence/patterns.md（默认状态 active）
  4. 每次运行自动维护 wiki 层目录，并刷新 wiki/snapshots/latest.md（可用 --no-snapshot 关闭）
  5. 已存在当日同 slug 日志时自动追加序号，不覆盖
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

SNAPSHOT_TEMPLATE = """# 快照：{project} · {date}
## 当前阶段
{task}（红队判定：{verdict}）
## 框架版本
v1：（尚未记录框架修订）
## 活跃主题
- （待从 moc/ 归纳）
## 最近本质判断
- {date}：{chain}
## 下一步
（待补充）
"""


def slugify(text: str, limit: int = 40) -> str:
    s = re.sub(r"\s+", "-", text.strip())
    s = re.sub(r"[\\/:*?\"<>|]", "", s)
    return s[:limit].strip("-") or "task"


def ensure_tree(workspace: Path) -> dict:
    root = workspace / ".essence"
    logs = root / "logs"
    wiki = root / "wiki"
    logs.mkdir(parents=True, exist_ok=True)
    (wiki / "inbox").mkdir(parents=True, exist_ok=True)
    (wiki / "moc").mkdir(parents=True, exist_ok=True)
    (wiki / "snapshots").mkdir(parents=True, exist_ok=True)
    paths = {"root": root, "logs": logs, "wiki": wiki,
             "snapshot": wiki / "snapshots" / "latest.md",
             "patterns": root / "patterns.md",
             "evolution": root / "evolution.md"}
    if not paths["patterns"].exists():
        paths["patterns"].write_text(
            "# 共性模式库\n\n按 SKILL.md 的条目格式追加；过时模式打 [deprecated]，不删除。\n",
            encoding="utf-8")
    if not paths["evolution"].exists():
        paths["evolution"].write_text(
            "# 进化总账\n\n- 模式总数：0（active 0）\n- 思维日志数：0\n"
            "- 元模式数：0\n- 框架修订次数：0\n\n## 修订历史\n\n（暂无）\n",
            encoding="utf-8")
    return paths


def unique_log_path(logs: Path, date: str, slug: str) -> Path:
    candidate = logs / f"{date}-{slug}.md"
    i = 2
    while candidate.exists():
        candidate = logs / f"{date}-{slug}-{i}.md"
        i += 1
    return candidate


def build_log(args, date: str) -> str:
    def lst(items):
        return "、".join(items) if items else "无"

    chain = args.chain.replace("|", " → ") if args.chain else "（未记录）"
    revision = args.revision or "无"
    return f"""# 思维日志：{args.task}
- 日期：{date}
- 触发：{args.trigger or args.task}
- 阶段轨迹：{args.stages or "（未记录）"}
- 本质层级链：{chain}
- 红队判定：{args.verdict or "（未记录）"}
- 模式命中：{lst(args.hits)}
- 新模式：{lst(args.patterns)}
- 框架修订：{revision}
"""


def append_patterns(patterns_file: Path, titles: list, date: str, task: str) -> int:
    if not titles:
        return 0
    with patterns_file.open("a", encoding="utf-8") as f:
        for title in titles:
            f.write(f"\n### {title}｜来源：{date}-{slugify(task)}｜提出：{date}\n"
                    f"- 适用条件：（待补）\n"
                    f"- 本质：（待补，必须含关系）\n"
                    f"- 复用方式：（待补）\n"
                    f"- 状态：active\n")
    return len(titles)


def count_active_patterns(patterns_file: Path) -> int:
    text = patterns_file.read_text(encoding="utf-8")
    entries = re.findall(r"^###\s", text, flags=re.M)
    deprecated = re.findall(r"状态：\s*deprecated", text)
    return len(entries) - len(deprecated)


def update_evolution(evo_file: Path, new_patterns: int, revision: str | None) -> None:
    text = evo_file.read_text(encoding="utf-8")

    def bump(field, by=1):
        nonlocal text
        text = re.sub(rf"({field}：)(\d+)",
                      lambda m: f"{m.group(1)}{int(m.group(2)) + by}", text)

    bump("模式总数", new_patterns)
    bump("思维日志数")
    if revision:
        bump("框架修订次数")
    active = count_active_patterns(evo_file.parent / "patterns.md")
    text = re.sub(r"(active )\d+", rf"\g<1>{active}", text)
    date = datetime.date.today().isoformat()
    if revision:
        text = text.replace("## 修订历史\n\n（暂无）\n", "## 修订历史\n")
        text += f"\n- {date}：{revision}\n"
    evo_file.write_text(text, encoding="utf-8")


def refresh_snapshot(snapshot: Path, workspace: Path, args, date: str) -> None:
    chain = args.chain.replace("|", " → ") if args.chain else "（未记录）"
    verdict = args.verdict or "（未记录）"
    if snapshot.exists():
        text = snapshot.read_text(encoding="utf-8")
        import re as _re
        text = _re.sub(r"# 快照：.*? · \d{4}-\d{2}-\d{2}",
                       f"# 快照：{workspace.name} · {date}", text, count=1)
        new_entry = f"- {date}：{chain}"
        m = _re.search(r"## 最近本质判断\n(.*?)(?=\n## )", text, flags=_re.S)
        if m:
            lines = [new_entry] + [l for l in m.group(1).strip().splitlines() if l.strip()][:4]
            text = text[:m.start(1)] + "\n" + "\n".join(lines) + "\n" + text[m.end(1):]
        snapshot.write_text(text, encoding="utf-8")
    else:
        snapshot.write_text(SNAPSHOT_TEMPLATE.format(
            project=workspace.name, date=date, task=args.task,
            verdict=verdict, chain=chain), encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description="写入 essence-thinking 进化库")
    p.add_argument("--workspace", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--trigger", default="")
    p.add_argument("--stages", default="")
    p.add_argument("--chain", default="")
    p.add_argument("--verdict", choices=["PASS", "REVISE", "REJECT"], default=None)
    p.add_argument("--hits", nargs="*", default=[])
    p.add_argument("--patterns", nargs="*", default=[],
                   help="新模式标题列表（追加骨架到 patterns.md）")
    p.add_argument("--revision", default="")
    p.add_argument("--no-snapshot", action="store_true",
                   help="不刷新 wiki/snapshots/latest.md")
    args = p.parse_args()

    workspace = Path(args.workspace)
    if not workspace.is_dir():
        print(f"错误：工作区不存在：{workspace}", file=sys.stderr)
        return 1

    paths = ensure_tree(workspace)
    date = datetime.date.today().isoformat()
    slug = slugify(args.task)

    log_path = unique_log_path(paths["logs"], date, slug)
    log_path.write_text(build_log(args, date), encoding="utf-8")

    added = append_patterns(paths["patterns"], args.patterns, date, args.task)
    update_evolution(paths["evolution"], added, args.revision or None)
    if not args.no_snapshot:
        refresh_snapshot(paths["snapshot"], workspace, args, date)

    print(f"日志已写入：{log_path}")
    print(f"新模式骨架追加：{added} 条")
    print(f"进化总账已更新：{paths['evolution']}")
    if not args.no_snapshot:
        print(f"snapshot 已刷新：{paths['snapshot']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
