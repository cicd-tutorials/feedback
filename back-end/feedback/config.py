from os import getenv
from pathlib import Path
from secrets import token_urlsafe


def get_home_directory() -> Path:
    return Path(getenv("FEEDBACK_HOME", Path.home() / ".feedback"))


def write_to_home_directory(
        filename: str,
        content: str,
        end: str = "\n") -> int:
    home = get_home_directory()
    home.mkdir(parents=True, exist_ok=True)

    with open(home / filename, "w+") as f:
        return f.write(content) + f.write(end)


def get_secret_key() -> str:
    try:
        with open(get_home_directory() / "secret_key") as f:
            return f.read().strip()
    except FileNotFoundError:
        pass

    key = token_urlsafe(64)
    write_to_home_directory("secret_key", key)

    return key
