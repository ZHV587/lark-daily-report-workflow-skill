from pathlib import Path
import json


def test_version_manifest_exists_and_has_version():
    data = json.loads(Path("version.json").read_text(encoding="utf-8"))
    assert data["version"] == "0.1.0"
    assert data["release_tag"] == "v0.1.0"
