# essence-thinking · 本质思维引擎

[![Release](https://img.shields.io/github/v/release/qwertasdf123-xkw/essence-thinking)](https://github.com/qwertasdf123-xkw/essence-thinking/releases)

> **无限进化，你想即所得。**

将个人思维方法论工程化为可自进化的思考中枢：元体系闭环 + 状态外化 + 能力路由 + 无感知补丁，可与任意 skill / pipeline 无限叠加闭环。

A self-evolving thinking-orchestration skill: meta-layer closed loop, state externalization, skill routing and imperceptible self-patching. Stack it with any skill or pipeline to close the loop.

## 五大思维公理（Five Axioms）

1. **共性抽象** — 知识与知识之间有共性；把握整体关系即可批量掌握可复用知识。
2. **设计思维** — 架构演变 = 大方向 × 技术组合；类比对比 + 本质原理 + 特性分析得最优解。
3. **分层本质** — 逻辑思维的本质是事物间的关系；本质叠加，逐层下钻。
4. **思维进化** — 灵感来自思维过程；从事物本身出发；随时进化框架。
5. **拼装闭环** — 架构的作用不是复用功能，而是形成逻辑闭环。

**元原则**：事实是一切 · 辩证取舍（先正评，再攻击，后取舍）

## 核心机制

- **ESSENCE 七段循环**：探入 → 剥离 → 叠加 → 提炼 → 编织 → 验证（分级）→ 沉淀。任何任务统一思考协议。
- **元体系**（meta.md）：事实→元原则→元逻辑→方法→产物五层结构，层间双向闭环，越深层修订门槛越高。
- **知识 wiki 层**：`inbox/`（原料）→ `moc/`（主题索引）→ `snapshots/`（项目快照）。上下文是可丢弃缓存，思维状态永不丢。
- **无感知进化**（self-evolve.md）：结论经补丁队列延迟合并回本体——快速记录、批量应用、合并必有记录。
- **旁路沉淀**（side-channel.md）：分支思路 ≤20 秒捕获，主线停顿点批量消费——跃迁发生且无感知。
- **Skill 路由层**：判断 → 寻址 → 加载 → 预算 → 收割，按共性定位能力，越委托越强。
- **产出协议**（report.md）：思维报告三级模板，让人类协作方加入闭环。
- **软约束插件**（plugins/）：context-guard · snapshot-restore · router-scan · release。

## 目录结构

```
essence-thinking/
├── SKILL.md              # 主协议（七段循环 + 元原则 + 各层接口）
├── references/
│   ├── philosophy.md     # 五大公理展开
│   ├── meta.md           # 元体系：五层结构与闭环
│   ├── self-evolve.md    # 无感知进化协议（补丁队列）
│   ├── side-channel.md   # 旁路沉淀协议
│   ├── report.md         # 产出报告协议
│   ├── plugins.md        # 软约束插件化规范
│   ├── pipeline.md       # pipeline 集成 + dev-pipeline 互操作
│   ├── wiki.md           # wiki 层协议
│   ├── routing.md        # 路由层协议与上下文预算
│   └── evolution.md      # 自进化体系详规
├── plugins/              # P0 软约束插件（各含 PLUGIN.md + scripts/）
│   ├── context-guard/    # 上下文预算守卫
│   ├── snapshot-restore/ # 思维状态恢复引导
│   ├── router-scan/      # 本机 skill 索引扫描
│   └── release/          # 打包发布流水线
└── scripts/
    └── et_log.py         # 进化库写入工具（日志/模式/补丁/快照）
```

## 安装

下载 [最新 release](https://github.com/qwertasdf123-xkw/essence-thinking/releases) 中的 `essence-thinking.skill`，在 Kimi Work 中安装，或将 `essence-thinking/` 目录放入你的 skills 目录（如 `~/.kimi/skills/` 或项目 `.agents/skills/`）。

## 版本

- [v1.1.1](https://github.com/qwertasdf123-xkw/essence-thinking/releases/tag/v1.1.1) · 插件落地（2026-10-25）：P0 软约束插件四件套（context-guard / snapshot-restore / router-scan / release）
- [v1.1](https://github.com/qwertasdf123-xkw/essence-thinking/releases/tag/v1.1) · 越思考越强（2026-10-25）：元体系闭环、无感知补丁、辩证取舍、旁路沉淀、产出协议
- [v1.0](https://github.com/qwertasdf123-xkw/essence-thinking/releases/tag/v1.0) · 无限进化，你想即所得（2026-10-21）

## 协作生态

- [dev-pipeline-dsh](https://github.com/qwertasdf123-xkw/dev-pipeline-dsh) — 11 步开发流水线，与本案互操作映射见 `references/pipeline.md` §6
- [evolutionary-architecture-skill](https://github.com/qwertasdf123-xkw/evolutionary-architecture-skill) — 演进式架构设计

## 许可

MIT
