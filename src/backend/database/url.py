"Decide se vai suar a url do banco de dados local ou não"
from pathlib import Path
def get_url(url:str|None=None, is_async:bool=True) -> str:

    BASE_DIR = Path(__file__).resolve().parent.parent.parent / "data"

    if url is None:

        url = f"sqlite+aiosqlite:///{BASE_DIR / "data.db"}" if is_async else f"sqlite:///{BASE_DIR / "data.db"}"

    else:

        url = url.replace("postgresql://", "postgresql+asyncpg://") if not "asyncpg" in url and is_async else url

    return url


        



