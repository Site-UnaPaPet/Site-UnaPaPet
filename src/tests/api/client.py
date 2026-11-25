"""Cliente HTTP dos testes da API: so faz a requisicao em localhost e levanta erro se o status for >= 400.

Simula o navegador: o Session guarda os cookies que a API manda (access_token e refresh_token) e os envia sozinho
nas chamadas seguintes. Quem precisa de login usa um Client que ja chamou login(); sem token no cabecalho."""
import os
import time
import uuid
import requests

#A API roda em localhost (API_URL só existe para mudar a porta, se precisar)
BASE_URL = os.getenv("API_URL", "http://localhost:8000")

#Identifica esta rodada: deixa e-mails, RAs e nomes únicos para o teste poder rodar várias vezes seguidas
RUN = uuid.uuid4().hex[:8]


class ApiError(Exception):
    pass


class Client:

    def __init__(self) -> None:

        #o Session guarda os cookies (refresh token) entre as chamadas
        self.session = requests.Session()

    #Entra na conta: a API grava os cookies (access_token e refresh_token) neste cliente, igual ao navegador
    def login(self, credentials: dict):

        return self.call("POST", "/auth/login", json=credentials)

    #Faz a requisição e devolve o corpo (JSON). Se o status for >= 400, levanta ApiError mostrando o erro
    def call(self, method: str, path: str, json=None, token: str | None = None, **params):

        url = f"{BASE_URL}{path}"
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        for attempt in range(3):

            response = self.session.request(method, url, json=json, headers=headers, params=params or None, timeout=10)

            #o rate limit pode barrar uma rodada grande de testes: espera o tempo que a API pediu e tenta de novo
            if response.status_code == 429 and attempt < 2:

                wait = int(response.headers.get("Retry-After", "1"))
                print(f"WAIT  429 em {method} {path}, esperando {wait}s")
                time.sleep(wait)
                continue

            break

        try:
            body = response.json() if response.content else None
        except ValueError:
            body = response.text

        if response.status_code >= 400:
            raise ApiError(f"{method} {url} -> {response.status_code}: {body}")

        print(f"{response.status_code}  {method} {path}")

        return body
