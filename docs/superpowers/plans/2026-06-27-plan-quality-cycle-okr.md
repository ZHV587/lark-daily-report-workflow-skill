# Plan Quality And Cycle OKR Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add plan quality checks, cycle-level OKR risk, personal recurring bias profiles, and plan-to-probability validation to the daily/weekly workflow.

**Architecture:** Keep the existing skill structure. Add concise rules to `SKILL.md`, detailed requirements to daily/weekly references, conversation prompts to `conversation-protocol.md`, runtime data requirements to `feishu-operations.md`, acceptance cases to `scenario-acceptance.md`, and version metadata to `version.json`.

**Tech Stack:** Markdown skill files, existing Python validation scripts, pytest, GitHub release.

---

### Task 1: Add Daily Plan Quality And Cycle Risk Rules

**Files:**
- Modify: `SKILL.md`
- Modify: `references/report-standard.md`
- Modify: `references/conversation-protocol.md`

- [x] Add a top-level rule that daily reports must check next-day plan executability, cycle-level OKR risk, and recurring personal execution bias.
- [x] Add daily report requirements for `明日计划可执行性检查`: capacity, dependency, acceptance standard, KR contribution, and whether the plan covers the minimum required progress.
- [x] Add daily report requirements for `OKR 周期累计风险`: cycle progress, remaining gap, current recovery path, and whether tomorrow can improve probability.
- [x] Add conversation guidance that asks one concise question when a plan is too vague, overloaded, or not enough to protect OKR.

### Task 2: Add Weekly Plan-To-Probability Validation

**Files:**
- Modify: `references/weekly-report-standard.md`
- Modify: `references/conversation-protocol.md`
- Modify: `references/run-summary.md`

- [x] Add `下周计划对 OKR 达成概率的提升判断`.
- [x] Require every major next-week plan to state expected KR movement and whether it can raise, maintain, or lower OKR probability.
- [x] If the next-week plan cannot protect OKR, require escalation, scope reduction, extra resource, method change, or target adjustment.
- [x] Include the judgment in the run summary.

### Task 3: Add Recurring Bias Profile And Acceptance Scenarios

**Files:**
- Modify: `references/report-standard.md`
- Modify: `references/weekly-report-standard.md`
- Modify: `references/scenario-acceptance.md`
- Modify: `references/exception-handling.md`

- [x] Add a lightweight `个人重复偏差画像` rule based on repeated evidence, not personality judgment.
- [x] Track patterns such as waiting on external dependencies, writing but not publishing, preparing without results, and non-OKR work crowding out core KR.
- [x] Require a concrete prevention action when a repeated bias appears.
- [x] Add acceptance cases for plan quality, cycle risk, plan-to-probability, and recurring bias.

### Task 4: Validate, Sync, Release

**Files:**
- Modify: `version.json`
- Copy changed files to installed skill directory.

- [x] Bump version to `0.1.9`.
- [x] Run skill validation, team config check, pytest, and diff check.
- [x] Sync installed skill.
- [ ] Commit, tag `v0.1.9`, push, and create GitHub release.
