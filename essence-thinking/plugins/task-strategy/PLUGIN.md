---
name: task-strategy
triggers: Explore 后需要选择 ESSENCE 路径、Wiki 检索视图或验证强度；新事实要求重路由；简单事实任务需要快速路径
---
# task-strategy · 任务策略编译器

## 输入
Explore 的现象、目标、约束与已知证据；调用方判断的主/辅场景、置信度和理由。

## 输出
符合 `references/task-routing.md` 的暂定策略契约；重路由时追加 revision/history。使用 `--out` 时写入指定 JSON 且 stdout 只给一行摘要，否则输出完整契约到 stdout。

## 预算
只加载命中的场景 JSON；每个场景 <500 tok。脚本直接执行，不读入上下文；不预加载其他策略。

## 与本体关系
实现本体的任务策略契约接口；本体没有它仍能按 ESSENCE 默认流程运行。它不替代 Wiki，也不选择具体 Skill。

## 用法
```bash
# 查看可选场景
python scripts/strategy.py --list

# 编译；--secondary 可省略或带多个场景
python scripts/strategy.py --task "设计 X" --scene design \
  --secondary research --confidence high --rationale "调研后选型" --out route.json

# 重路由；保留历史
python scripts/strategy.py --contract route.json --scene diagnosis \
  --confidence high --reason "新证据推翻初始场景" --out route.json
```

场景定义在 `strategies/<name>.json`，是文档与脚本的同一事实源。新增场景只增加 JSON，不改脚本；修改契约结构仍需改本体协议。
