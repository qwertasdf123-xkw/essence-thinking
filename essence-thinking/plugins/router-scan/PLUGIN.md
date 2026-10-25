---
name: router-scan
triggers: 路由层 R1 寻址前索引缺失或过期；或用户说"扫描一下本机有哪些 skill"
---
# router-scan · 本机 skill 索引扫描

## 输入
skills 根目录列表（默认：~/.codex/skills、~/.dsh/skills、~/.kimi/skills、<workspace>/.agents/skills）。

## 输出
技能索引 Markdown（name + description 摘要 + 所在根目录），写到 `<workspace>/.essence/index/skills-index.md`；同时输出摘要到 stdout。

## 预算
自身体积 ~300 tok（索引文件按需读取，不常驻）；扫描耗时与 skill 数量线性。

## 与本体关系
依赖路由协议 R1 级寻址；本体没有它仍完整——它是 R1 的索引构建器，索引过期时 R1 降级为 R2（Agent 搜索）也能工作。

## 用法
```bash
python scripts/scan_skills.py --workspace <项目路径> [--roots <dir1> <dir2> ...]
```
