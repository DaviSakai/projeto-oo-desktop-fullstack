# infra/json_store.py
# -------------------------------------------------------------
# Utilitário para leitura e escrita segura (thread-safe) de JSONs
# -------------------------------------------------------------
import json
from pathlib import Path
from threading import Lock
from typing import Any

# Dicionário global para garantir travas exclusivas por arquivo
_locks = {}


def _get_lock(path: Path) -> Lock:
    """
    Retorna (ou cria) um Lock associado a um caminho específico.
    Garante que apenas uma thread escreva no JSON por vez.
    """
    key = str(path.resolve())
    if key not in _locks:
        _locks[key] = Lock()
    return _locks[key]


def read_json(path: Path) -> Any:
    """
    Lê um arquivo JSON e retorna o conteúdo (dict/list/...).
    Se o arquivo não existir ou estiver corrompido, retorna None.
    """
    path.parent.mkdir(exist_ok=True)
    lock = _get_lock(path)
    with lock:
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None


def write_json(path: Path, data: Any) -> None:
    """
    Escreve dados em um arquivo JSON de forma atômica:
    1. Cria um arquivo temporário.
    2. Escreve os dados.
    3. Substitui o original apenas após sucesso.
    """
    path.parent.mkdir(exist_ok=True)
    lock = _get_lock(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with lock:
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(path)
