---
name: context-guard
triggers: 单任务加载内容接近上下文预算阈值（默认 80%）；或用户问"还剩多少上下文预算"
---
# context-guard · 上下文预算守卫

## 输入
当前会话已加载的内容清单（skill 名/文件 + 估算 tokens），由调用方以参数或清单文件传入。

## 输出
预算状态（已用/总额/百分比）+ 超阈值时的压缩告警与 7 项压缩检查清单提醒。写到 stdout，不写文件。

## 预算
自身体积 <100 tok（脚本直接执行，不读入上下文）。

## 与本体关系
依赖 routing.md 预算表概念；本体没有它仍完整——它是预算数值的执行器，数值本身可调（软约束）。

## 用法
```bash
python scripts/budget.py --total 12000 --threshold 0.8 \
  --used "essence-thinking:1800" "snapshot:500" "moc-插件化:800" "某skill:2500"
# 或用清单文件（每行 "名称 tokens"）
python scripts/budget.py --manifest loaded.txt
```
