"""Teste do AuthManage: hash (generate/compare) e token (create/read).

Roda da raiz do projeto:  python -m src.tests.encode
Define um JWT_SECRET local só para o teste.
"""
import os
import time

#A variável precisa estar definida antes do AuthManage ler o ambiente
os.environ["JWT_SECRET"] = "segredo-local-de-teste"

from src.backend.auth.manage import AuthManage
from src.backend.exceptions import InvalidTokenError
from src.backend.logs import logger


def expect_invalid(auth: AuthManage, token) -> None:

    try:
        auth.read(token)
        raise AssertionError(f"deveria ter levantado InvalidTokenError para {token!r}")
    except InvalidTokenError:
        pass


def main() -> None:

    auth = AuthManage()
    assert auth.secret == "segredo-local-de-teste"
    assert auth.alg == "HS256"

    #hash: generate
    hashed = auth.generate("senha123")
    assert hashed != "senha123"
    assert hashed.startswith("$2b$")
    assert auth.generate("senha123") != hashed  # salt diferente a cada chamada

    #hash: compare
    assert auth.compare("senha123", hashed) is True
    assert auth.compare("outra", hashed) is False
    assert auth.compare("senha123", "hash-invalido") is False

    #token: create
    payload = {"sub": "1", "role": "admin"}
    token = auth.create(payload)
    assert isinstance(token, str) and token.count(".") == 2

    #token: read
    assert auth.read(token) == payload

    #token: erros viram InvalidTokenError
    expect_invalid(auth, "lixo.lixo.lixo")
    expect_invalid(auth, "")
    expect_invalid(auth, None)
    expect_invalid(auth, token[:-3] + "abc")  # assinatura adulterada

    other = AuthManage()
    other.secret = "outro-segredo"
    expect_invalid(other, token)  # assinatura de outro segredo

    expired = auth.create({"sub": "1", "exp": int(time.time()) - 10})
    expect_invalid(auth, expired)

    for bad_secret in (None, ""):
        broken = AuthManage()
        broken.secret = bad_secret
        try:
            broken.create(payload)
            raise AssertionError(f"create deveria falhar com secret {bad_secret!r}")
        except InvalidTokenError:
            pass

    #login completo: senha -> hash -> token -> leitura
    user_hash = auth.generate("minha-senha")
    if auth.compare("minha-senha", user_hash):
        assert auth.read(auth.create({"sub": "42"}))["sub"] == "42"

    logger.success("TODOS OS TESTES PASSARAM")


if __name__ == "__main__":
    main()
