from pathlib import Path
import csv
import os

import typer
from rich import print

from .resumes import (
    download_resume,
    InvalidFileSuffix,
    build_outfile_name,
    add_resume_to_cache,
    load_resume_lookup,
    write_resume_lookup,
    RESUME_LOOKUP,
)
from .packet_builder import populate_page_lookup_for_pdf, PAGE_LOOKUP, write_pdf

__version__ = "0.1.0"

OUTDIR = "out"
STUDENTS = []

app = typer.Typer()


@app.command()
def get_resumes(
    csv_filepath: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    outdir: Path = typer.Option(OUTDIR),
):
    """Download resumes from a CSV file.

    The CSV file should have two columns: `full_name` and `url`.
    """

    with open(csv_filepath, encoding="utf-8-sig") as csvf:
        csv_reader = csv.DictReader(csvf)
        data = list(csv_reader)

    try:
        os.mkdir(outdir)
    except:
        pass

    for row in data:
        full_name, url = row["full_name"], row["url"]

        STUDENTS.append(full_name)

        try:
            outfile_name = build_outfile_name(full_name, url)

            try:
                outfile_path = Path(outdir) / outfile_name
                download_resume(url, outfile_path)
                add_resume_to_cache(full_name, outfile_path)

                print(
                    f"[bold green]Success:[/bold green] Downloaded resume for [bold]{full_name}[/bold]."
                )
            except Exception as e:
                print(f"[bold red]Error:[/bold red] {e}")
                print(e)

        except InvalidFileSuffix:
            print(
                f"[bold yellow]Warning:[/bold yellow] [bold]{full_name}[/bold] did not upload a valid resume."
            )

    write_resume_lookup(Path(outdir))


@app.command()
def stitch_resumes(
    packet_pdf_filepath: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    outfile: str = typer.Argument(...),
    outdir: Path = typer.Option(OUTDIR),
):
    """Stitch resumes into the student packet PDF."""

    resumes = load_resume_lookup(Path(outdir))
    populate_page_lookup_for_pdf(packet_pdf_filepath)

    write_pdf(Path(outfile), resumes)
    print(f"[bold green]Success:[/bold green] Wrote PDF to [bold]{outfile}[/bold].")
