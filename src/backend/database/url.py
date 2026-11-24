"Decide se vai suar a url do banco de dados local ou não"
from src.backend.config import settings
from pathlib import Path

def get_url() -> str:

    url = settings.envs["URL_DB"]

    if url is None:

        url = f"sqlite+aiosqlite:///{settings.DATA / "data.db"}"

    return url


        



