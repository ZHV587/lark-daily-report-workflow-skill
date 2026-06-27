"""只读检查 lark-daily-report-workflow 的团队配置结构。"""

from __future__ import annotations

import pathlib
import re
import sys


REQUIRED_TEXT = [
    "日报规范",
    "日报规则名称",
    "周报规范",
    "周报规则名称",
    "每周五",
    "本周目标回顾",
    "下周计划",
    "Asia/Shanghai",
    "周一到周六",
    "周日为常规休息日",
    "复盘反思 Base",
    "知识库节点",
    "多维表格标识",
    "数据表",
    "视图",
    "人员",
    "日期",
    "复盘反思经验",
    "错误类型",
]

REQUIRED_ID_PATTERNS = {
    "日报规则 ID": "`[0-9]{10,}`",
    "知识库节点": "`[A-Za-z0-9]{20,}`",
    "多维表格标识": "`[A-Za-z0-9]{20,}`",
    "数据表": "`tbl[A-Za-z0-9]+`",
    "视图": "`vew[A-Za-z0-9]+`",
    "字段 ID": "`fld[A-Za-z0-9]+`",
}


def validate(path: pathlib.Path, *, require_ids: bool = True) -> list[str]:
    content = path.read_text(encoding="utf-8")
    missing = [item for item in REQUIRED_TEXT if item not in content]
    if require_ids:
        for label, pattern in REQUIRED_ID_PATTERNS.items():
            if not re.search(pattern, content):
                missing.append(f"{label} ({pattern})")
    return missing


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) not in (1, 2):
        print("用法：check_team_config.py <team-config.md 路径> [--template]", file=sys.stderr)
        return 2

    template_mode = "--template" in args[1:]
    path = pathlib.Path(args[0])
    if not path.exists():
        print(f"失败：文件不存在：{path}", file=sys.stderr)
        return 1

    missing = validate(path, require_ids=not template_mode)
    if missing:
        print("失败：团队配置缺少必要配置：", file=sys.stderr)
        for item in missing:
            print(f"- {item}", file=sys.stderr)
        return 1

    if template_mode:
        print("通过：team-config.md 公共模板结构有效")
    else:
        print("通过：团队配置已包含日报和复盘 Base 的必要配置")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
