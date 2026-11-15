# 任务策略路由协议（任务 → 思维与知识策略契约）

当 Explore 后需要选择 ESSENCE 路径、Wiki 视图、检索组合或验证强度时读取。本文只定义稳定接口；具体场景策略位于 `plugins/task-strategy/`。

## 目录

1. 职责边界
2. 策略契约
3. 编译与重路由
4. 简单任务快速路径
5. 验证与进化回流

## 1. 职责边界

任务策略路由回答“应该怎样思考、获取知识和验证”，不直接执行领域任务，也不预选具体 skill。

```text
Explore → 任务策略契约 → 选定 ESSENCE 路径 → Extract 能力缺口
        → Skill 能力路由 → Consolidate → Evolve / 路由反馈
```

- 场景是可撤销假设，不是任务永久标签。
- 复合任务使用主场景＋附属场景；子任务目标差异明显时分别编译契约。
- Wiki 仍只有一套；契约只选择本次视图与下钻条件。
- 路由不确定时先补充事实或提问，不进入重型流程。

## 2. 策略契约

```yaml
scene:
  primary: design
  secondary: [research]
  confidence: high | medium | low
  rationale: 为什么选择该场景，哪些事实仍未知
essence_path: [Explore, Strip, Extract, Network, Consolidate, Evolve]
wiki_view:
  entry: L0
  mocs: [主题名]
  max_level: L0 | L1 | L2 | L3
  drill_down_when: [需要原始依据、摘要冲突等]
retrieval:
  strategy: [共性模式、类比案例、反例等]
  sources: [本次实际来源]
  stop_when: [继续检索不再改变行动等]
verification:
  profile: 验证档位名
  required_evidence: [事实锚点、边界、反例等]
reroute_when: [会改变主场景或路径的新事实]
budget:
  profile: default
status: tentative
revision: 0
history: []
```

`revision/history` 记录策略修正；`sources` 只记录实际使用的来源，不把计划当成事实。

## 3. 编译与重路由

1. 根据任务认知结构选择主场景，必要时添加附属场景，并写明理由。
2. 加载主、辅场景策略，合并 ESSENCE 阶段、检索组合、证据要求和重路由条件；ESSENCE 顺序不可改变。
3. 验证强度取各子场景最高档，不能因主场景较简单而降低附属高风险任务的验证。
4. `confidence=low` 时强制降级为 Explore→Strip、Wiki L0，并优先补充事实或提问。
5. 新事实改变任务结构、检索反驳初始假设、验证失败指向错误场景时，重新编译；保留修订历史，不覆盖旧判断。

脚本只负责合并、降级、校验和留痕，语义场景判断由调用方完成：

```bash
python plugins/task-strategy/scripts/strategy.py \
  --task "设计 X" --scene design --secondary research \
  --confidence high --rationale "包含技术调研与方案选型" --out route.json

python plugins/task-strategy/scripts/strategy.py \
  --contract route.json --scene diagnosis --confidence high \
  --reason "新证据表明问题是既有系统故障" --out route.json
```

## 4. 简单任务快速路径

简单事实查询使用 `fact` 策略：Explore→一行 Strip（对象与属性/关系）→Consolidate，跳过无行动价值的重型推理；只有产生可复用模式时才 Evolve。

快速路径不豁免事实锚点、来源时效和工具结果核对。

## 5. 验证与进化回流

Consolidate 同时验证任务结论和策略是否合适，至少记录：

- 初始/最终场景、置信度、重路由次数与原因；
- 人工纠正、实际加载层级和上下文成本；
- 验证结果，以及哪条证据支持或推翻策略。

日志只形成证据，不自动改写策略。同类纠正反复出现后，按 `self-evolve.md` 生成策略插件补丁；修改契约字段或主流程则属于协议类补丁，必须人工确认。
