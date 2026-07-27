"""SPEC-006: configuração de harness (pytest path + ruff + review)."""

from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]


def test_pytest_ini_sets_pythonpath_to_project_root():
    ini = ROOT / "pytest.ini"
    assert ini.is_file(), "pytest.ini deve existir para coleta de módulos locais"
    text = ini.read_text(encoding="utf-8")
    assert "pythonpath" in text.lower()
    assert "." in text


def test_ruff_excludes_devkit_cli_script():
    cfg = ROOT / "ruff.toml"
    assert cfg.is_file()
    data = tomllib.loads(cfg.read_text(encoding="utf-8"))
    # exclude / extend-exclude
    excluded = set(data.get("exclude") or []) | set(data.get("extend-exclude") or [])
    # also accept nested under lint
    lint = data.get("lint") or {}
    excluded |= set(lint.get("exclude") or [])
    assert "devkit" in excluded or any("devkit" in str(x) for x in excluded), (
        "ruff deve excluir o script CLI devkit do lint de produção"
    )


def test_ruff_application_packages_exist_for_review_scope():
    """Pacotes que o review deve cobrir (além de app.py e tests/)."""
    expected = [
        "analysis",
        "allocator",
        "ui",
        "llm",
        "portfolio",
        "config",
        "data_fetcher",
        "models",
        "utils",
    ]
    for name in expected:
        assert (ROOT / name).is_dir(), f"pacote ausente: {name}"
