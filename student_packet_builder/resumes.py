from typing import Optional
from pathlib import Path
from urllib.parse import urlparse
import json
import requests

RESUME_LOOKUP = {}


class InvalidFileSuffix(ValueError):
    pass


def get_url_path_file_suffix(url: str) -> str:
    """Get the file suffix from a URL."""

    return Path(urlparse(url).path).suffix


def build_outfile_name(full_name: str, url: str) -> str:
    """Build the name of the output file."""

    url_suffix = get_url_path_file_suffix(url)
    if not url_suffix:
        raise InvalidFileSuffix(f"URL `{url}` does not have a valid file suffix.")

    return f"{full_name}{url_suffix}"


def download_resume(url: str, outfile_name: Path):
    req = requests.get(f"https://{url}", stream=True)

    with open(outfile_name, "wb") as out:
        out.write(req.content)


def add_resume_to_cache(name: str, resume_filepath: Path):
    RESUME_LOOKUP[name] = resume_filepath


def load_resume_lookup(outdir: Path) -> dict:
    try:
        with open(outdir / "resume_lookup.json", "r") as f:
            RESUME_LOOKUP = {
                name: Path(resume) for name, resume in json.loads(f.read()).items()
            }

        return RESUME_LOOKUP
    except:
        pass


def get_resume_filepath(name: str) -> Optional[Path]:
    return RESUME_LOOKUP.get(name)


def write_resume_lookup(outdir: Path):
    with open(outdir / "resume_lookup.json", "w") as f:
        f.write(
            json.dumps({name: str(resume) for name, resume in RESUME_LOOKUP.items()})
        )
