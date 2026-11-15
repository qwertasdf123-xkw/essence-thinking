#!/usr/bin/env python3
"""编译、校验和重路由 essence-thinking 任务策略契约。"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ESSENCE_ORDER = ["Explore", "Strip", "Stack", "Extract", "Network", "Consolidate", "Evolve"]
LEVEL_ORDER = ["L0", "L1", "L2", "L3"]
STRATEGY_DIR = Path(__file__).resolve().parent.parent / "strategies"


def unique(items):
    return list(dict.fromkeys(items))


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"无法读取 JSON：{path}：{exc}") from exc


def load_strategy(name):
    path = STRATEGY_DIR / f"{name}.json"
    if not path.is_file():
        available = ", ".join(p.stem for p in sorted(STRATEGY_DIR.glob("*.json")))
        raise ValueError(f"未知场景 '{name}'；可选：{available}")
    data = load_json(path)
    validate_strategy(data, path)
    return data


def validate_strategy(data, path="策略", require_consolidate=True):
    required = {"essence_path", "wiki", "retrieval", "verification", "reroute_when"}
    missing = required - set(data)
    if missing:
        raise ValueError(f"{path} 缺字段：{sorted(missing)}")
    path_set = set(data["essence_path"])
    required_stages = {"Explore", "Consolidate"} if require_consolidate else {"Explore"}
    if not path_set <= set(ESSENCE_ORDER) or not required_stages <= path_set:
        raise ValueError(f"{path} 的 essence_path 缺少必需阶段或使用非法阶段")
    if data["essence_path"] != [s for s in ESSENCE_ORDER if s in path_set]:
        raise ValueError(f"{path} 的 ESSENCE 阶段顺序错误")
    if data["wiki"].get("max_level") not in LEVEL_ORDER:
        raise ValueError(f"{path} 的 Wiki 层级非法")
    if not data["retrieval"].get("stop_when"):
        raise ValueError(f"{path} 必须声明检索停止条件")
    if not data["verification"].get("required_evidence"):
        raise ValueError(f"{path} 必须声明证据要求")


def compile_contract(args):
    previous = load_json(args.contract) if args.contract else None
    if previous:
        validate_contract(previous)
    primary = args.scene or (previous and previous["scene"]["primary"])
    if not primary:
        raise ValueError("首次编译必须提供 --scene")
    task = args.task or (previous and previous["task"])
    if not task:
        raise ValueError("首次编译必须提供 --task")

    secondary = args.secondary
    if secondary is None:
        secondary = previous["scene"]["secondary"] if previous else []
    secondary = [s for s in secondary if s != primary]
    strategies = [load_strategy(primary)] + [load_strategy(s) for s in secondary]

    stages = unique(s for data in strategies for s in data["essence_path"])
    stages = [s for s in ESSENCE_ORDER if s in stages]
    max_level = max((data["wiki"]["max_level"] for data in strategies), key=LEVEL_ORDER.index)
    strongest = max(strategies, key=lambda d: d["verification"].get("strength", 0))
    confidence = args.confidence or (previous and previous["scene"]["confidence"]) or "low"
    rationale = args.rationale or (previous and previous["scene"]["rationale"])
    if previous and args.reason:
        rationale = args.reason
    if not rationale:
        raise ValueError("必须提供 --rationale（重路由时也可用 --reason）")

    old_mocs = previous["wiki_view"]["mocs"] if previous else []
    old_sources = previous["retrieval"]["sources"] if previous else []
    contract = {
        "schema_version": 1,
        "route_id": previous["route_id"] if previous else new_route_id(task),
        "task": task,
        "scene": {
            "primary": primary,
            "secondary": secondary,
            "confidence": confidence,
            "rationale": rationale,
        },
        "essence_path": stages,
        "wiki_view": {
            "entry": "L0",
            "mocs": unique(old_mocs + args.moc),
            "max_level": max_level,
            "drill_down_when": unique(x for d in strategies for x in d["wiki"]["drill_down_when"]),
        },
        "retrieval": {
            "strategy": unique(x for d in strategies for x in d["retrieval"]["strategy"]),
            "sources": unique(old_sources + args.source),
            "stop_when": unique(x for d in strategies for x in d["retrieval"]["stop_when"]),
        },
        "verification": {
            "profile": strongest["verification"]["profile"],
            "required_evidence": unique(x for d in strategies for x in d["verification"]["required_evidence"]),
        },
        "reroute_when": unique(x for d in strategies for x in d["reroute_when"]),
        "budget": {"profile": args.budget or (previous and previous["budget"]["profile"]) or strategies[0].get("budget_profile", "default")},
        "status": "tentative",
        "revision": previous["revision"] + 1 if previous else 0,
        "history": previous["history"] if previous else [],
        "clarification_required": False,
    }
    if previous:
        contract["history"] = previous["history"] + [{
            "revision": previous["revision"],
            "scene": previous["scene"],
            "reason": args.reason or "重新编译策略",
            "at": datetime.now(timezone.utc).isoformat(),
        }]
    if confidence == "low":
        contract.update({
            "essence_path": ["Explore", "Strip"],
            "clarification_required": True,
            "reroute_when": unique(contract["reroute_when"] + ["补足关键事实或用户澄清后重新编译"]),
        })
        contract["wiki_view"]["max_level"] = "L0"
        contract["retrieval"]["stop_when"] = ["先补足关键事实；不做重型检索"]
    validate_contract(contract)
    return contract


def new_route_id(task):
    digest = hashlib.sha256(task.encode("utf-8")).hexdigest()[:8]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"route-{stamp}-{digest}"


def validate_contract(data):
    required = {"route_id", "task", "scene", "essence_path", "wiki_view", "retrieval", "verification", "reroute_when", "revision", "history"}
    missing = required - set(data)
    if missing:
        raise ValueError(f"契约缺字段：{sorted(missing)}")
    if data["scene"]["confidence"] not in {"low", "medium", "high"}:
        raise ValueError("confidence 必须为 low/medium/high")
    validate_strategy({
        "essence_path": data["essence_path"],
        "wiki": data["wiki_view"],
        "retrieval": data["retrieval"],
        "verification": data["verification"],
        "reroute_when": data["reroute_when"],
    }, "任务策略契约", require_consolidate=not data.get("clarification_required", False))


def main():
    ap = argparse.ArgumentParser(description="任务策略契约编译器")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--contract", help="已有契约；提供后执行重路由")
    ap.add_argument("--task")
    ap.add_argument("--scene")
    ap.add_argument("--secondary", nargs="*", default=None)
    ap.add_argument("--confidence", choices=["low", "medium", "high"])
    ap.add_argument("--rationale")
    ap.add_argument("--reason", help="重路由原因")
    ap.add_argument("--moc", action="append", default=[])
    ap.add_argument("--source", action="append", default=[])
    ap.add_argument("--budget")
    ap.add_argument("--out")
    args = ap.parse_args()
    if args.list:
        for path in sorted(STRATEGY_DIR.glob("*.json")):
            data = load_json(path)
            print(f"{path.stem}: {data.get('description', '')}")
        return 0
    if args.contract and not args.reason:
        ap.error("重路由必须提供 --reason")
    try:
        contract = compile_contract(args)
        rendered = json.dumps(contract, ensure_ascii=False, indent=2) + "\n"
        if args.out:
            out = Path(args.out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(rendered, encoding="utf-8")
            print(f"✓ {out}｜{contract['scene']['primary']}｜revision {contract['revision']}｜{' → '.join(contract['essence_path'])}")
        else:
            print(rendered, end="")
        return 0
    except ValueError as exc:
        print(f"策略编译失败：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
