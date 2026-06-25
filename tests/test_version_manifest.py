from pathlib import Path
import json
import re


def test_version_manifest_exists_and_has_version():
    data = json.loads(Path("version.json").read_text(encoding="utf-8"))
    assert re.fullmatch(r"\d+\.\d+\.\d+", data["version"])
    assert data["release_tag"] == f"v{data['version']}"
