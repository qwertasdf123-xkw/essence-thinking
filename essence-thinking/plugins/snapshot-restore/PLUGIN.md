---
name: snapshot-restore
triggers: 新会话/新任务进入项目的第一步；或用户说"恢复上下文"、"继续上次的工作"
---
# snapshot-restore · 思维状态恢复引导

## 输入
项目工作区路径（`.essence/` 所在目录）。

## 输出
按 wiki 加载协议 L0→L2 的**应读取清单**（文件路径 + 估算 tokens + 读取顺序）到 stdout；文件缺失时明确报告。

## 预算
自身体积 <200 tok（不读文件内容，只列清单；内容读取由调用方按清单执行）。

## 与本体关系
依赖 wiki.md 渐进加载协议；本体没有它仍完整——它是加载协议的引导器。

## 用法
```bash
python scripts/restore.py --workspace <项目路径> [--level 2]
# level 0=只列 snapshot；1=+命中 moc；2=+patterns 与近期日志（默认全列）
```
