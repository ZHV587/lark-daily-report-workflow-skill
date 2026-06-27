# Weekly Report Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an OKR weekly report branch to the existing Feishu daily report workflow skill.

**Architecture:** Keep the current skill name and package, add weekly report routing and a focused `weekly-report-standard.md` reference. Weekly reports reuse `lark-cli` reads and manual Feishu submission, but summarize the week by KR progress, risk, method learnings, and next-week priorities instead of merging daily report prose.

**Tech Stack:** Codex skill Markdown, `lark-cli`, Python validation scripts, pytest.

---

### Task 1: Add Weekly Report Standards

**Files:**
- Create: `references/weekly-report-standard.md`
- Modify: `references/team-config.md`
- Modify: `scripts/check_team_config.py`

- [x] **Step 1:** Create a weekly standard reference with fields from the Feishu rules doc.
- [x] **Step 2:** Add weekly report config keys and field list to `team-config.md`.
- [x] **Step 3:** Update `check_team_config.py` so template validation covers weekly report section labels.

### Task 2: Route Weekly Report Intent

**Files:**
- Modify: `SKILL.md`
- Modify: `references/semantic-trigger.md`
- Modify: `references/conversation-protocol.md`
- Modify: `references/feishu-operations.md`
- Modify: `references/run-summary.md`

- [x] **Step 1:** Update frontmatter and top-level routing to include `WEEKLY_REPORT_REVIEW`.
- [x] **Step 2:** Add semantic triggers for 写周报、本周复盘、下周计划 and protect ordinary project summaries from accidental Feishu weekly mode.
- [x] **Step 3:** Add weekly opening, data sources, manual filling output, and structured write boundaries.

### Task 3: Add Acceptance Coverage And Release

**Files:**
- Modify: `references/scenario-acceptance.md`
- Modify: `version.json`

- [x] **Step 1:** Add weekly report acceptance scenarios.
- [x] **Step 2:** Run `quick_validate.py`, `check_team_config.py --template`, and `python -m pytest -q`.
- [ ] **Step 3:** Sync installed skill, commit, tag, push, and create a GitHub Release.
