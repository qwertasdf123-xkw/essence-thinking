# Skill 路由层协议（能力发现 + 渐进加载 + 上下文预算）

本文定义路由层的四步协议与预算控制规则。当任务需要本 skill 之外的能力、需要决定调用哪个 skill、或上下文吃紧需要压缩时读取。

## 目录

1. 路由的本质
2. 四步路由协议
3. 路由决策速查表
4. 上下文预算表
5. 压缩检查清单
6. 无限叠加的安全性

## 1. 路由的本质

路由是公理 1 的反向应用：公理 1 说"按共性批量掌握知识"，路由说"**按共性定位能力**"。
- 不搜工具名，搜"这件事的本质操作是什么"（如"非结构化→结构化"、"多源→单一事实源"）。
- 委托不是认输，是闭环设计：本引擎保留 Strip/Stack 的判断权，把执行交给更专业的 skill（公理 5：各自处在闭环的正确位置）。

## 2. 四步路由协议

**① 判断（本引擎，Extract 段后）**
把需求改写成 1~2 个本质操作，输出："本任务需要的能力 = <本质操作>"。

**② 寻址（三级，逐级升级，命中即停）**
| 级 | 动作 | 成本 |
|---|---|---|
| R1 | 查当前会话 skills 索引的 description 做语义匹配 | ~0 |
| R2 | 调用 Agent / kimi-skills-finder 搜索："能完成 <本质操作> 的 skill" | 一次调用 |
| R3 | 查外部来源（插件市场、GitHub awesome 列表等），找到后由 skill-creator 固化 | 最贵，少见 |

金融数据类需求跳过 R2，直接按市场路由：A股/港股→ifind，美股→S&P/Gildata/SEC EDGAR，再兜底 Yahoo Finance。

**③ 加载（渐进式）**
- 只读被命中 skill 的 SKILL.md 主体。
- 其 references 按"当前阶段需要哪个读哪个"；scripts 不读、直接执行。
- 同时调用的 skill 不超过 3 个，超出说明任务没拆够（回到 Stack 段重新分层）。

**④ 回收（委托后必做）**
- 被委托 skill 的产出回到本引擎 Consolidate 段统一红队验证——路由出去的判断权，责任不外包。
- 委托过程写入日志的"阶段轨迹"，沉淀为模式（"X 类任务 → Y skill" 变成 patterns.md 条目）。

## 3. 路由决策速查表

| 本质操作 | 首选 | 备选 |
|---|---|---|
| 事实数据（中/美/宏观） | ifind / yahoo_finance | sec_edgar、igo_open_data、imf、world_bank |
| 文档产物 | docx / kimi-word / kimi-pdf / md-to-pdf | — |
| 演示产物 | pptx / kimi-slides / guizang-ppt-skill | — |
| 表格数据 | kimi-excel / xlsx | pandas（scripts） |
| 可视化 | seaborn-visualization | Widget（需持久展示时） |
| 网页操作 | kimi-webbridge | — |
| 学术调研 | scholar | kimi_search_v2 |
| 做网站/app | webapp-building | widget |
| 定时/看板 | automation / canvas / widget | — |
| 都不匹配 | 回 Network 段：把该能力设计成本次闭环要造的组件 | — |

## 4. 上下文预算表

实测口径：字符数 × 1.5 粗估；表格/代码块 token 效率更高，实际可能更低。

| 常驻项 | 预算 |
|---|---|
| 本 skill SKILL.md | ~1800 tok |
| snapshot (L0) | ≤500 tok |
| 命中 moc (L1) | ≤800 tok/个 |
| patterns.md (L2) | ≤1500 tok |
| 被委托 skill 的 SKILL.md | 每个 +≤2500 tok |
| **单任务总预算** | **≤12k tok（超出先压缩再继续）** |

## 5. 压缩检查清单（触发条件：总预算 80%）

压缩前逐项确认：
1. snapshot 已刷新到最新状态
2. 当前结论已写入 moc 或 patterns
3. 被委托 skill 的中间产物已落盘（文件形式），上下文里只留 1 行摘要
4. 未消化 inbox 已写盘
5. 原始查询/原始需求仍保留在 snapshot 或对话起点
6. 没有未保存的中间状态
7. 压缩后按 L0 重新加载继续

## 6. 无限叠加的安全性

叠加能力时的三条护栏：
- **闭环判据**：每接入一个新 skill，问"它在闭环的哪一环？拿掉会不会断？"（公理 5）答不出就不接。
- **共性优先**：两个 skill 能按共性合并使用时（如 docx 与 kimi-word），选其一，不同时加载。
- **沉淀回检**：新 skill 用满 3 次后，在 evolution.md 记一笔"接入评估"：值得常驻还是按需路由——防止索引膨胀（索引本身是上下文成本）。
