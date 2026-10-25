---
name: essence-thinking
description: 本质思维引擎——将用户的五大思维公理（共性抽象、设计思维、分层本质、思维进化、拼装闭环）工程化为可复用的思考流程，内置知识 wiki 层（inbox/MOC/snapshot）、skill 路由、上下文预算控制、无感知自我进化与旁路沉淀机制。当用户面对复杂问题需要拆解、做架构/方案设计需要找最优解、需要把多个知识/能力拼装成闭环、复盘一次任务沉淀可复用模式、需要为项目建立可渐进加载的思维索引、需要产出给人协作的报告，或任何其他 skill / pipeline（如 dev-pipeline）需要一个"思考中枢"来串联阶段时使用。Use when the user says "用本质思维分析"、"拆解一下这个问题"、"这套架构的本质是什么"、"帮我把这些能力拼成闭环"、"复盘并沉淀模式"、"帮我找合适的skill来处理这个任务"、"出一份思维报告"，或当任意工作流需要统一的分析、设计、验证、路由、产出与沉淀阶段。
---

# 本质思维引擎 (Essence Thinking Engine)

这是一个"思考中枢"型 skill：它不解决某个具体领域的问题，而是给任何任务提供**统一的思考协议**，并能与任意其他 skill / pipeline 无缝拼接成闭环。

## 核心：五大思维公理（不可裁剪）

这是本 skill 的灵魂，任何流程都是它们的工程化展开：

1. **共性抽象** —— 知识与知识之间有共性。充分理解架构、把握整体关系、形成框架图谱后，即可按共性掌握多种相关的、可复用的知识。
2. **设计思维** —— 架构演变 = 一个大方向 × 一种或多种技术。通过类比对比、本质与原理、特性分析，得到符合逻辑的最优解。
3. **分层本质** —— 逻辑思维的本质是事物与事物的关系。抓住当前现象的可能性 → 看到第一层本质；本质叠加、思维构建 → 看到下一层本质。
4. **思维进化** —— 思维不是固化的，灵感来自思维过程本身；从事物本身出发而非空想；认知与抓本质能力越强，思考随时可进化。
5. **拼装闭环** —— 架构的作用不是复用功能，而是形成一套逻辑上的完整闭环。同一个组件（如 wiki）换一条主线串联，可以是知识库，也可以是思维过程。

**元原则（高于公理的裁决准则）**：
- **事实是一切** —— 任何结论必须经得起推敲：能指回观察、文档、数据或代码行；经不起推敲的判断不许沉淀、不许进本体。
- **辩证取舍** —— 不立即否定任何结论。先正评（优势与适用条件），再红队（劣势与攻击面），最后取舍（保留什么、放弃什么、为什么）。模型越思考越强，每个结论都是进化的原料。

元原则、元逻辑、方法、产物构成五层元体系，层间闭环与修订梯度见 [references/meta.md](references/meta.md)。

## 主流程：ESSENCE 七段循环

任何任务进入本引擎，都走这七段。简单任务可跳过部分阶段，但顺序不可乱。

```
E 探入 Explore      → 收集现象、材料、约束（不问对错，先全量感知）
S 剥离 Strip        → 剥离表象，定位"事物之间的关系"，给出第一层本质假设
S 叠加 Stack        → 对第一层本质继续追问"它的本质是什么"，逐层下钻（默认 2~3 层，复杂问题加深）
E 提炼 Extract      → 跨层、跨对象找共性，输出框架图谱（概念 + 关系，不是功能清单）
N 编织 Network      → 按公理 2 做架构拼装：大方向 × 技术选型，给出逻辑闭环方案；对照公理 5 检验"闭环是否完整"
C 验证 Consolidate  → 辩证取舍：先正评（优势与适用条件）→ 再攻击（强度按推翻代价×新颖度分级：有旧思路铺垫的做论证链追溯+抽样，全新的全量红队）→ 后取舍（保留/放弃/理由）
E 沉淀 Evolve       → 新共性、新模式写回进化库与 wiki 层；结论若触及本体，生成 skill 补丁提案（无感知进化）
```

**每段输出物：**

| 阶段 | 输出 | 最小形式 |
|---|---|---|
| Explore | 现象清单 + 约束清单 | bullet list |
| Strip | 第一层本质（1~2 句）+ 关系图（文字版） | 本质卡片 |
| Stack | 本质层级链 L1→L2→L3 | 层级链 |
| Extract | 共性列表 + 框架图谱 | graph 描述 |
| Network | 闭环架构方案（含选型理由与类比依据） | 方案 + 类比表 |
| Consolidate | 辩证取舍表：优势/劣势/取舍结论 | 辩证表 + 判定 |
| Evolve | 模式条目 + 日志 + snapshot 刷新 + 补丁提案（如有） | 追加到进化库 |

## 知识 wiki 层（LLM-wiki 思维过程具象化）

知识 = 我们对事物的了解 = 思维过程的产物。wiki 层把"知识与知识的连接"落成项目内的真实文件结构，让**上下文成为可丢弃缓存，思维状态永不丢**：

```
<项目>/.essence/wiki/
├── inbox/            # 原料箱：未处理的观察、剪藏、灵感（一条一文件，定期清空到 moc）
├── moc/              # 多主题索引（Map of Content）：每个主题一个 moc-<主题>.md，互相链接
└── snapshots/        # 项目快照：当前思维状态的浓缩摘要，进项目先读它即可重建上下文
    └── latest.md
```

- **读写时机**：思考中产生的碎片进 inbox；主题成形后提炼为 moc 并回链相关条目；每轮 Evolve 后刷新 `snapshots/latest.md`。
- **加载协议（渐进式）**：新会话进项目只读 `snapshots/latest.md`（约 300~500 tokens）→ 按任务命中再读对应 `moc/` → 只有需要原始依据时才下钻 inbox/日志。详见 [references/wiki.md](references/wiki.md)。

## 无感知进化（skill 本体自我优化）

思维结论不止沉淀为模式——当一条结论的**普适性和稳定性足够**时，它应该回流到 skill 本体，让本体随使用越变越强，而使用者无需感知修改过程：

- 触发时机：Evolve 段判断沉淀物是否触及本体（新公理级判断、流程缺陷、冗余发现）。
- 提案通道：写入 `.essence/patches/<日期>.md`（`et_log.py --patch` 自动落盘），**不直接改本体**。
- 应用规则：提案积累后由用户一句话批量应用；低风险类（措辞、示例、模式条目）可自动应用，协议类（改七段流程、公理、红线）必须人工确认。
- 版本纪律：每次本体变更记入 `evolution.md` 框架修订历史，GitHub 仓库同步打版本。详见 [references/self-evolve.md](references/self-evolve.md)。
- **主线不中断**：大任务执行中冒出的分支思路，按 [references/side-channel.md](references/side-channel.md) 捕获进 inbox（≤20 秒、一句话），在主线 Consolidate/Evolve 停顿点批量消费——跃迁发生，但无感知。

## 软约束插件化

本体只保留**协议骨架**（七段流程、公理、红线、接口约定）；一切**软约束**——预算数值、检查清单、报告格式、发布流程——一律通过插件实现，可独立增删、独立进化：

- 插件形态：`plugins/<场景>/PLUGIN.md`（触发条件 + 接口声明）+ scripts/，由路由层按命中渐进加载。
- 判定标准：改它不需要动 SKILL.md 的，就是插件；需要动 SKILL.md 的，才是本体。
- 待办与规范见 [references/plugins.md](references/plugins.md)。

## 产出协议（人机协作报告）

思考的最终产物必须**人能看懂、能参与、能挑错**——报告不是装饰，是让人类协作方加入闭环的接口：

- 标准产物：**思维报告**（本质层级链 + 辩证取舍表 + 闭环方案 + 事实锚点引用）， Consolidate 段后生成，给人类协作方审阅。
- 去向：项目内 `.essence/reports/`（随 snapshot 引用），需要分享时经路由层委托 docx/kimi-pdf 等 skill 出正式文档。
- 模板与分级（简版/完整版）见 [references/report.md](references/report.md)。

## Skill 路由层（能力发现、委托与收割）

任务经 Extract 明确"需要什么能力"后，由路由层决定调用谁，实现工作流的无限叠加：

1. **判断**：把需求表述为共性（"需要把非结构化数据变结构化"），而非具体工具名。
2. **寻址**：先查当前 skills 索引的 description 做语义匹配；不确定时调用 Agent / kimi-skills-finder 搜索；涉及事实数据时按市场路由到 ifind / yahoo_finance / sec_edgar 等。
3. **加载**：只加载被命中 skill 的 SKILL.md，其 references/scripts 按"用到才读"渐进拉取。
4. **预算**：全程遵守上下文预算表，超限先压缩再加载（预算数值本身是软约束，可在插件中调）。
5. **收割**：被委托 skill 的可复用方法论（思路、模式、约定）提炼进 `patterns.md`——他人的优点成为自身思维的跃迁养料，越用越强。详见 [references/routing.md](references/routing.md)。

## 与其他 skill / pipeline 的闭环集成协议

- **输入约定**：任何上游（用户请求、其他 skill、文件、代码、数据）都先经 `Explore` 段规范化，形成统一的现象清单，下游阶段只消费该清单。
- **输出约定**：每个阶段输出标准产物（Markdown 片段），可被下游 skill 直接读取作为输入。
- **两种集成姿势**：
  1. **引擎为主**：完整跑 ESSENCE 七段，把具体执行委托给路由层选中的领域 skill —— 引擎负责"想清楚"，领域 skill 负责"做出来"。
  2. **引擎为段**：别人的 pipeline 在任意节点调用 `Strip`+`Stack`（分析段）、`Network`（设计段）或 `Evolve`（沉淀段），只取所需阶段，产物回流原 pipeline。
- **闭环判据（公理 5 工程化）**：一个 pipeline 是闭环，当且仅当它能回答——输入是什么、经过哪些本质变换、产出什么、谁来验证、验证结果沉淀到哪。缺一环即调用本引擎的 Network 段补设计。
- **与 dev-pipeline 协作**：dev-pipeline（11 阶段 + L1/L2/L3）是工程侧外化协议的成熟实现，两者同构——把 essence 的思考段注入其 stage 0~2，用其 gate/STATUS/decision-log 承载 essence 产物。映射表见 [references/pipeline.md](references/pipeline.md)。

## 自进化体系

进化库位于工作区的 `.essence/` 目录（首次使用时创建）：

```
.essence/
├── patterns.md      # 共性模式库：所有复用的唯一事实源（带来源任务与适用条件）
├── patches/         # 本体补丁提案（无感知进化的待应用队列）
├── logs/            # 思维日志：每次 ESSENCE 循环的结构化记录
│   └── YYYY-MM-DD-<slug>.md
├── evolution.md     # 进化总账：模式数量、修订历史、能力叠加记录
├── reports/         # 思维报告（人机协作产物）
└── wiki/            # 知识 wiki 层（inbox/ + moc/ + snapshots/）
```

- 每次完整跑完循环，`Evolve` 段必须调用 `scripts/et_log.py` 写日志并刷新 snapshot，并判断是否有值得沉淀的**新模式**；有则追加进 `patterns.md`。
- **能力叠加**：后续任何任务开始时，先读 `.essence/wiki/snapshots/latest.md` 与 `patterns.md`，把已有模式作为思维起点（公理 1）；任务结束再沉淀——形成"越用越强"的正循环。
- **模式条目格式**：`### 模式名｜来源｜适用条件｜本质一句话｜复用方式`。详细规范见 [references/evolution.md](references/evolution.md)。

## 分场景速查

- **分析类任务**（"帮我看懂 X / 拆解 X"）：重点跑 Explore→Strip→Stack→Extract，产出本质卡片 + 层级链。
- **设计类任务**（"设计 X 方案 / 架构"）：重点跑 Extract→Network→Consolidate，必须给类比表与选型理由（公理 2）。
- **拼装类任务**（"把 A+B+C 拼成闭环"）：直接进 Network，用闭环判据检验；参照公理 5，尝试为同一组组件给出第二种拼装主线。
- **复盘类任务**（"复盘这次任务"）：跑 Explore（回放事实）→Strip（成败的第一层本质）→Consolidate（辩证取舍）→Evolve（沉淀）。
- **指导学习类任务**（"我要学 X"）：用 Extract 为该领域构建框架图谱，按共性安排学习顺序。
- **协作类任务**（"给团队出份报告"）：Consolidate 后走产出协议，出思维报告。
- **能力不够时**（"这事该用什么做"）：走路由层——判断→寻址→加载→预算→收割，不硬扛。

## 思维质量红线

- **事实是一切**：每个结论必须有事实锚点（观察/文档/数据/代码行），经不起推敲的判断不许沉淀、不许进本体。
- **辩证取舍**：禁止一上来否定结论——先列优势与适用条件，再攻击劣势，最后给取舍理由。
- 禁止跳过 Strip 直接给结论（那是空想，违反公理 4）。
- 每个"本质"都必须能指认它描述了**哪两个事物之间的什么关系**（公理 3）。
- 每个架构选型必须给出一个类比依据（公理 2）。
- 每个闭环方案必须指出"如果拿掉哪一环，闭环就断"（公理 5）。
- 每次进项目先读 snapshot 再动手；加载文件超出预算先压缩（见 routing.md 预算表）。
- 复杂参考内容按需读取：[references/philosophy.md](references/philosophy.md)（公理展开与示例）、[references/pipeline.md](references/pipeline.md)（pipeline 与 dev-pipeline 集成详规）、[references/wiki.md](references/wiki.md)（wiki 层协议）、[references/routing.md](references/routing.md)（路由与预算）、[references/self-evolve.md](references/self-evolve.md)（无感知进化协议）、[references/report.md](references/report.md)（产出报告协议）、[references/plugins.md](references/plugins.md)（软约束插件化规范）、[references/meta.md](references/meta.md)（元体系：五层结构与闭环）、[references/side-channel.md](references/side-channel.md)（旁路沉淀：不打断主线的思路跃迁）。
