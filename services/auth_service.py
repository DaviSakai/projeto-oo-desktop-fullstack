# services/auth_service.py
# -------------------------------------------------------------
# Serviço de autenticação: hash de senhas e controle de sessões.
# Armazena as sessões em JSON (sessions.json).
# -------------------------------------------------------------
import os
import hmac
import base64
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from config import (
    HASH_NAME,
    HASH_ITER,
    SALT_BYTES,
    SESSION_SECRET,
    SESSIONS_JSON,
)
from infra.json_store import read_json, write_json


# =============================================================
# 🔐 Funções de hash de senha (PBKDF2)
# =============================================================
def hash_password(password: str) -> str:
    """
    Gera um hash seguro para a senha usando PBKDF2-HMAC-SHA256.
    Retorna no formato: pbkdf2$ITERACOES$SAL$HASH
    """
    salt = os.urandom(SALT_BYTES)
    dk = hashlib.pbkdf2_hmac(HASH_NAME, password.encode(), salt, HASH_ITER)
    return f"pbkdf2${HASH_ITER}${salt.hex()}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """
    Verifica se a senha informada corresponde ao hash armazenado.
    Retorna True se for válida, False caso contrário.
    """
    try:
        scheme, iters, hex_salt, hex_hash = stored.split("$")
        assert scheme == "pbkdf2"
        iters = int(iters)
        salt = bytes.fromhex(hex_salt)
        esperado = bytes.fromhex(hex_hash)
        dk = hashlib.pbkdf2_hmac(HASH_NAME, password.encode(), salt, iters)
        return hmac.compare_digest(dk, esperado)
    except Exception:
        return False


# =============================================================
# 💾 Classe de controle de sessões (SessionStore)
# =============================================================
class SessionStore:
    """
    Gerencia sessões de login armazenadas em JSON (sessions.json).
    Cada sessão contém: token, user_id, expiração e assinatura HMAC.
    """

    def __init__(self, path=SESSIONS_JSON, ttl_minutes: int = 60):
        self.path = path
        self.ttl = ttl_minutes
        self._ensure()

    # ---------------------------------------------------------
    # Garante que o arquivo sessions.json exista
    # ---------------------------------------------------------
    def _ensure(self):
        data = read_json(self.path)
        if data is None:
            write_json(self.path, {"sessions": {}})

    # ---------------------------------------------------------
    # Lê e salva o conteúdo do JSON
    # ---------------------------------------------------------
    def _load(self) -> Dict[str, Any]:
        return read_json(self.path)

    def _save(self, data: Dict[str, Any]):
        write_json(self.path, data)

    # ---------------------------------------------------------
    # Cria uma nova sessão (gera token aleatório)
    # ---------------------------------------------------------
    def create(self, user_id: int) -> str:
        """
        Cria uma nova sessão para o usuário informado.
        Retorna o token gerado.
        """
        token = base64.urlsafe_b64encode(os.urandom(24)).decode().rstrip("=")
        agora = datetime.now(timezone.utc)
        expira_em = agora + timedelta(minutes=self.ttl)

        data = self._load()
        data["sessions"][token] = {
            "user_id": user_id,
            "exp": expira_em.isoformat(),
            # Assinatura para evitar adulteração do token
            "sig": hmac.new(
                SESSION_SECRET.encode(), token.encode(), hashlib.sha256
            ).hexdigest(),
        }
        self._save(data)
        return token

    # ---------------------------------------------------------
    # Busca e valida uma sessão a partir do token do cookie
    # ---------------------------------------------------------
    def get(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Retorna os dados da sessão se o token for válido e não expirado.
        Caso contrário, retorna None.
        """
        data = self._load()
        sess = data.get("sessions", {}).get(token)
        if not sess:
            return None

        # Valida assinatura HMAC
        assinatura_ok = hmac.new(
            SESSION_SECRET.encode(), token.encode(), hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(assinatura_ok, sess.get("sig", "")):
            return None

        # Valida expiração
        try:
            exp = datetime.fromisoformat(sess["exp"])
        except Exception:
            return None

        if datetime.now(timezone.utc) > exp:
            # Sessão expirada → remove automaticamente
            self.delete(token)
            return None

        return sess

    # ---------------------------------------------------------
    # Apaga uma sessão (logout)
    # ---------------------------------------------------------
    def delete(self, token: str) -> None:
        """
        Remove o token de sessão do JSON (logout).
        """
        data = self._load()
        if token in data.get("sessions", {}):
            del data["sessions"][token]
            self._save(data)
