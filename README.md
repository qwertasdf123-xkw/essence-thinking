# essence-thinking · 本质思维引擎

[![Release](https://img.shields.io/github/v/release/qwertasdf123-xkw/essence-thinking)](https://github.com/qwertasdf123-xkw/essence-thinking/releases)

> **无限进化，你想即所得。**

将个人思维方法论（五大思维公理）工程化为可自进化的思考中枢：统一思考协议 + 状态外化 + 能力路由，可与任意 skill / pipeline 无限叠加闭环。

A self-evolving thinking-orchestration skill: unified thinking protocol + state externalization + skill routing. Stack it with any skill or pipeline to close the loop.

## 五大思维公理（Five Axioms）

1. **共性抽象** — 知识与知识之间有共性；把握整体关系即可批量掌握可复用知识。
2. **设计思维** — 架构演变 = 大方向 × 技术组合；类比对比 + 本质原理 + 特性分析得最优解。
3. **分层本质** — 逻辑思维的本质是事物间的关系；本质叠加，逐层下钻。
4. **思维进化** — 灵感来自思维过程；从事物本身出发；随时进化框架。
5. **拼装闭环** — 架构的作用不是复用功能，而是形成逻辑闭环。

## 核心机制

- **ESSENCE 七段循环**：探入 → 剥离 → 叠加 → 提炼 → 编织 → 验证 → 沉淀。任何任务统一思考协议。
- **知识 wiki 层**：`inbox/`（原料）→ `moc/`（主题索引）→ `snapshots/`（项目快照）。上下文是可丢弃缓存，思维状态永不丢。
- **Skill 路由层**：判断 → 寻址 → 加载 → 回收，按共性定位能力，按 token 预算渐进加载。
- **自进化体系**：`.essence/` 进化库（模式库 + 思维日志 + 进化总账），越用越强。

## 安装

下载 [最新 release](https://github.com/qwertasdf123-xkw/essence-thinking/releases) 中的 `essence-thinking.skill`，在 Kimi Work 中安装，或将 `essence-thinking/` 目录放入你的 skills 目录（如 `~/.kimi/skills/` 或项目 `.agents/skills/`）。

## 目录结构

```
essence-thinking/
├── SKILL.md              # 主协议
├── references/
│   ├── philosophy.md     # 五大公理展开
│   ├── pipeline.md       # pipeline 集成 + dev-pipeline 互操作
│   ├── wiki.md           # wiki 层协议
│   ├── routing.md        # 路由层协议与上下文预算
│   └── evolution.md      # 自进化体系详规
└── scripts/
    └── et_log.py         # 进化库写入工具
```

## 版本

- [v1.0](https://github.com/qwertasdf123-xkw/essence-thinking/releases/tag/v1.0) · 无限进化，你想即所得（2026-10-21）

## 协作生态

- [dev-pipeline-dsh](https://github.com/qwertasdf123-xkw/dev-pipeline-dsh) — 11 步开发流水线，与本案互操作映射见 `references/pipeline.md` §6
- [evolutionary-architecture-skill](https://github.com/qwertasdf123-xkw/evolutionary-architecture-skill) — 演进式架构设计

## 许可

MIT
