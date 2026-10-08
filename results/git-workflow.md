# Git 与 GitHub 实际操作记录

仓库：https://github.com/victoriamitsu28/Robo-Education-Recruitment

可见性：Public。所有操作均于 2026 年 10 月 8 日完成。

## 内容与操作

1. 在本地开发目录执行 `git init -b main`，用 `git add`、`git commit` 分别提交内训方案，以及课件、代码与验证记录。
2. 通过 Git Credential Manager 的设备授权完成 GitHub 登录，确认账号为 `victoriamitsu28`，创建上述空白公开仓库。
3. 使用 `git clone` 将远程空仓库克隆至新的本地目录；通过 `git fetch 本地开发仓库 main` 导入已完成的两次提交，再切换至 main。这样保留资料编写时的实际提交，而不是重新制造一次性上传记录。
4. 使用 `git push -u origin main` 将两次内容提交推送至 GitHub。
5. 在 `improve-class-preflight` 分支提交 Python 版本建议修正和课前环境检查程序，并用 `git push -u origin improve-class-preflight` 上传。
6. 创建 [Pull Request #1：修正 Python 版本要求并补充课前环境检查](https://github.com/victoriamitsu28/Robo-Education-Recruitment/pull/1)，检查改动与实际环境输出后合并。此次为个人任务中的流程演示，没有声称经过其他成员审核。
7. 使用 `git fetch origin` 与 `git merge --ff-only origin/main` 同步本地 main，补充 README 和本操作记录，再提交与推送。

## 可核对的提交

| 提交 | 实际内容 |
|---|---|
| `050c1a5` | 内训选题、学习目标、实施安排与 README |
| `941f2ae` | 10 分钟课件、演示代码、合成样例与验证记录 |
| `9cb0091` | 修正 Python 最低版本，增加课前环境检查及运行输出 |
| `cbb1d75` | 合并 Pull Request #1，保留分支提交历史 |

最终 README 与操作记录另以文档提交保存，可在仓库 Commits 页面查看。

## 遇到的问题

- 非交互认证没有输出：终止该次尝试，改用交互终端完成正式设备授权。
- Git HTTPS 请求停滞，而系统网络请求正常：检查系统代理后，为本次 Git 命令显式指定现有代理，再完成 clone 和 push；未修改全局网络配置。
- NumPy 固定版本与最初的 Python 建议不一致：检查包元数据，将最低版本修正为 3.11，推荐已实际验证的 3.12，并通过分支和 PR 保存改进过程。

不在本记录中保存访问令牌、设备授权码或个人认证信息。
