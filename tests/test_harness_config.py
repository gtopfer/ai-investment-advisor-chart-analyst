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


def test_ruff_excludes_non_app_paths():
    """Ruff não deve lintar venv/kit (fora do código de produção do app)."""
    cfg = ROOT / "ruff.toml"
    assert cfg.is_file()
    data = tomllib.loads(cfg.read_text(encoding="utf-8"))
    excluded = set(data.get("exclude") or []) | set(data.get("extend-exclude") or [])
    lint = data.get("lint") or {}
    excluded |= set(lint.get("exclude") or [])
    assert "venv" in excluded or ".venv" in excluded or any(
        "venv" in str(x) for x in excluded
    ), "ruff deve excluir venv do lint de produção"
    assert not any("devkit" in str(x) for x in excluded), (
        "DevKit removido do projeto — não deve restar exclude de devkit"
    )
    assert not (ROOT / "devkit").exists(), "binário/script DevKit não deve existir"


def test_ruff_application_packages_exist_for_review_scope():
    """Pacotes que o review deve cobrir (além de app.py e tests/)."""
    expected = [
        "ducks",
        "ducks/analysis",
        "ducks/market",
        "ducks/portfolio",
        "ducks/llm",
        "ducks/ui",
        "shared",
        "shared/config",
        "shared/models",
        "shared/utils",
    ]
    for name in expected:
        assert (ROOT / name).is_dir(), f"pacote ausente: {name}"
