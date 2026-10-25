---
name: release
triggers: 准备发布 skill 新版本时；或用户说"打包发布"、"出 release"
---
# release · 打包发布流水线（含硬校验清单）

## 输入
skill 目录（含 SKILL.md）、版本号。

## 输出
`<skill-name>.skill` 安装包（zip）+ SHA-256 + 发布前硬校验清单（stdout）。VERSION 文件自动更新。

## 预算
自身体积 <200 tok；包体积通常为几十 KB。

## 与本体关系
不依赖本体协议，是独立工具插件；其价值在于把 v1.0/v1.1 两次发布踩过的坑固化为**硬校验**（脚本强制，不靠记忆）。

## 硬校验清单（发布前必须全过）
1. SKILL.md 存在且 frontmatter 含非空 `name` 与 `description`
2. 目录名 == frontmatter `name`
3. `releases/v<版本>.md` 存在且**非空**（正文来源唯一指定）
4. 包 SHA-256 已计算并写入发布说明

## 用法
```bash
python scripts/package.py --version 1.1.1
# 校验通过后按 stdout 指引在 GitHub 建 release：tag=v<版本>、正文=releases/v<版本>.md、附件=生成的 .skill
```
