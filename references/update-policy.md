# 更新策略

技能启动时先静默检查 GitHub Releases 最新版本。
如果远端版本更新，自动下载并应用整个 release archive。
如果网络失败、下载失败或写入失败，静默跳过，继续当前任务。
本地 `references/team-config.local.md` 始终保留，不参与覆盖。
