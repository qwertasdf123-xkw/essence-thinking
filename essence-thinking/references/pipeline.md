# Pipeline 集成详规

本文定义 essence-thinking 作为 pipeline 阶段（stage）被其他工作流调用时的完整协议。当你的 pipeline 需要调用本引擎、或需要判断 pipeline 是否闭环时读取。

## 目录

1. 角色模型：引擎为主 / 引擎为段
2. 阶段接口契约
3. 标准产物格式
4. 闭环判据详解
5. 与其他 skill 协作的委托清单
6. 与 dev-pipeline 互操作（实测映射）

## 1. 角色模型

### 引擎为主（orchestrator 模式）

ESSENCE 七段全部执行，具体"动手"环节委托：
| ESSENCE 阶段 | 可委托的领域 skill 示例 |
|---|---|
| Explore | github（查仓库/代码）、igo_open_data、scholar |
| Network 中的"做出来" | pptx、docx、kimi-webbridge、webapp-building |
| Consolidate | 领域 skill 自带的验证能力 + 本引擎红队自检 |

适用：开放式任务（"帮我做一个 X 系统"）。引擎先想清楚，再逐个调用领域 skill 执行。

### 引擎为段（stage 模式）

外部 pipeline 只调用所需段：
- 需要分析 → 调 `Explore + Strip + Stack`（返回本质层级链）
- 需要设计 → 调 `Extract + Network`（返回闭环方案）
- 需要收尾 → 调 `Consolidate + Evolve`（返回判定 + 沉淀）

适用：已有成熟 pipeline，只想把"思考质量"插进去。

## 2. 阶段接口契约

每个段：输入 = 上一段的标准产物 + 原始上下文；输出 = 标准产物（Markdown 片段）。无状态——所有状态显式写在产物里，任何段可独立重跑。

```
[上游任意来源] → Explore → 现象清单/约束清单
              → Strip   → 本质卡片（L1 + 关系描述）
              → Stack   → 本质层级链（L1→Ln + 行动含义）
              → Extract → 共性列表 + 框架图谱
              → Network → 闭环方案（含类比表、选型理由）
              → Consolidate → 红队判定（PASS / REVISE / REJECT + 理由）
              → Evolve  → 日志文件路径 + 新增模式条目数
```

## 3. 标准产物格式

### 本质卡片（Strip 产物）

```markdown
## 本质卡片：<任务名>
- 现象：<一句话>
- 决定性关系：<A> —<关系>→ <B>
- 第一层本质：<1~2 句>
- 可证伪性：<如果本质判断错误，会观察到什么>
```

### 本质层级链（Stack 产物）

```markdown
## 本质层级链：<任务名>
L1: ...（现象层）
L2: ...（构成 L1 的关系）
L3: ...
→ 行动含义：...
```

### 闭环方案（Network 产物）

```markdown
## 闭环方案：<任务名>
- 大方向：<一句话>
- 架构拼装：<组件 → 闭环位置 → 承担的本质变换>
- 类比表：候选方案｜类比来源｜本质矛盾｜特性边界
- 选型：<选择 + 理由（必须引用类比表）>
- 闭环判据自查：输入✓ 变换✓ 产出✓ 验证与沉淀✓
- 断环点：<拿掉哪一环闭环即断>
```

## 4. 闭环判据详解

一个 pipeline/workflow 是闭环，当且仅当四问都有非空答案：

1. **输入是什么**：触发条件、数据/材料来源、格式。
2. **经过哪些本质变换**：不是步骤清单，而是"这个 pipeline 对世界做的本质操作"（如：把非结构化变成结构化、把单点变成批量）。
3. **产出什么**：产物、产物去哪、谁消费。
4. **谁来验证、沉淀到哪**：质量门槛是什么；验证结果写回哪个进化库。

任一问为空 → 调本引擎 Network 段补设计；都答得出但 pipeline 实际断掉 → 调 Strip 段重新定位决定性关系。

## 5. 与其他 skill 协作的委托清单

原则（公理 1）：能用领域 skill 按共性批量解决的部分，不手写。
- 数据获取 → 优先 ifind / yahoo_finance / sec_edgar / igo_open_data（按市场选）
- 文件产物 → docx / kimi-pdf / pptx / kimi-excel
- 可视化 → seaborn-visualization；交互面 → widget / canvas（需要持久展示时）
- 浏览器操作 → kimi-webbridge
- 学术资料 → scholar

调用顺序：先跑完 Strip+Stack 想清楚需要什么，再一次性委托，避免边想边查导致的碎片化调用。

## 6. 与 dev-pipeline 互操作（实测映射）

本机已有两套 dev-pipeline（`~/.codex/skills/dev-pipeline` 与 `~/.dsh/skills/dev-pipeline-dsh`）：11 阶段（0 Inspiration → 10 Observe）+ L1/L2/L3 成熟度分级加载 + `.dev/` 状态文件（STATUS/decision-log/gate-report），L1 启动总预算约 890 tokens。两者**同构**：都是"状态外化 + 按预算分级加载"，协作是双向的。

### 结构映射表

| dev-pipeline | essence-thinking | 说明 |
|---|---|---|
| `.dev/STATUS.md` | `wiki/snapshots/latest.md` | 工程状态 ↔ 思维状态，两个快照互相引用 |
| `.dev/decision-log.md` | `patterns.md` + `evolution.md` 修订历史 | 工程决策 ↔ 思维框架版本 |
| `gate-report-0X.md`（approve 门禁） | Consolidate 段红队判定 | gate 未 approve = 判定 REVISE |
| `maturity/L1→L3` | wiki 加载协议 L0→L3 | 加载预算档位的两种实现 |
| `templates/state-preservation.md`（7 项压缩检查） | routing.md 压缩检查清单（7 项） | 压缩语义一致，可互相复用 |
| `.dev/subagents/` 落盘中间产物 | 路由层"回收"步骤 | 委托产物落盘、上下文只留摘要 |

### 注入点（引擎为段）

| dev-pipeline 阶段 | 注入的 essence 段 | 产物去向 |
|---|---|---|
| 0 Inspiration | Explore + Strip | 灵感进 wiki inbox，第一层本质写 inspiration-log |
| 1 Spec | Stack + Extract | 本质层级链附在 spec 的"根本原因"节 |
| 2 Design | Network | 闭环方案 + 类比表进 design 模板 |
| 8 Audit | Consolidate（红队） | 判定结果对照 gate-report |
| 任意阶段收尾 | Evolve | et_log.py 同步刷新两边快照 |

### 协作硬规则

1. dev-pipeline 的门禁规则优先（无 approve 不跨阶段），essence 的红队判定不绕过 gate。
2. essence 的进化库与 dev-pipeline 的 `.dev/` 不合并目录，用**互相引用**保持各自闭环（公理 5：两个闭环各自完整，靠链接协作）。
3. 加载预算取两者较严者：dev-pipeline L1（~890 tok）与本引擎 L0+L1 之和的较小值。
