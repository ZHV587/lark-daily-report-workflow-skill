"""规范化日报复盘记录，用于精确重复校验。"""

from __future__ import annotations

import argparse
import json
import re
from typing import Iterable


def normalize_text(value: str) -> str:
    """去除首尾空白，并把连续空白压缩为一个空格。"""
    return re.sub(r"\s+", " ", value.strip())


def normalize_error_types(values: Iterable[str] | None) -> list[str]:
    """清理、去重并排序错误类型。"""
    if not values:
        return []
    normalized = {normalize_text(value) for value in values if normalize_text(value)}
    return sorted(normalized)


def build_duplicate_key(
    *,
    person: str,
    date: str,
    reflection: str,
    error_types: Iterable[str] | None = None,
) -> str:
    payload = {
        "person": normalize_text(person),
        "date": normalize_text(date),
        "reflection": normalize_text(reflection),
        "error_types": normalize_error_types(error_types),
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser(description="生成复盘记录的精确重复校验键。")
    parser.add_argument("--person", required=True, help="人员标识")
    parser.add_argument("--date", required=True, help="日报日期")
    parser.add_argument("--reflection", required=True, help="复盘反思经验文本")
    parser.add_argument("--error-type", action="append", default=[], help="错误类型，可重复传入")
    args = parser.parse_args()

    print(
        build_duplicate_key(
            person=args.person,
            date=args.date,
            reflection=args.reflection,
            error_types=args.error_type,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
