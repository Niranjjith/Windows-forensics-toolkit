from pathlib import Path
import json

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from modules.file_analyzer import analyze_file, analyze_directory


app = typer.Typer(
    help="Windows Digital Forensics Toolkit"
)

console = Console()


def show_banner():
    console.print(
        Panel.fit(
            "[bold cyan]WINDOWS FORENSICS TOOLKIT[/bold cyan]\n"
            "[white]Digital File Analysis & Evidence Hashing[/white]",
            border_style="cyan"
        )
    )


def display_file(data):
    """
    Display information about a file.
    """

    table = Table(
        title=f"File Analysis: {data['name']}",
        show_lines=True
    )

    table.add_column(
        "Property",
        style="cyan",
        no_wrap=True
    )

    table.add_column(
        "Value",
        style="white"
    )

    table.add_row("File Name", data["name"])
    table.add_row("Path", data["path"])
    table.add_row("File Type", data["extension"])
    table.add_row("Size", f"{data['size']:,} bytes")
    table.add_row("Created", data["created"])
    table.add_row("Modified", data["modified"])
    table.add_row("Accessed", data["accessed"])

    table.add_row(
        "MD5",
        data["md5"]
    )

    table.add_row(
        "SHA-1",
        data["sha1"]
    )

    table.add_row(
        "SHA-256",
        data["sha256"]
    )

    console.print(table)


def save_json_report(results, output_path):
    """
    Save forensic analysis results as JSON.
    """

    output_file = Path(output_path)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    console.print(
        f"\n[green]Report saved:[/green] {output_file}"
    )


@app.command()
def analyze(
    path: str = typer.Argument(
        ...,
        help="File or directory to analyze"
    ),
    output: str = typer.Option(
        "reports/forensic_report.json",
        "--output",
        "-o",
        help="JSON report output path"
    )
):
    """
    Analyze a file or directory.
    """

    show_banner()

    target = Path(path)

    if not target.exists():

        console.print(
            f"[bold red]ERROR:[/bold red] "
            f"Path does not exist: {target}"
        )

        raise typer.Exit(code=1)

    console.print(
        f"[bold]Evidence Path:[/bold] {target.resolve()}"
    )

    console.print()

    try:

        if target.is_file():

            results = [
                analyze_file(target)
            ]

        elif target.is_dir():

            results = analyze_directory(target)

        else:

            console.print(
                "[red]Unsupported path type.[/red]"
            )

            raise typer.Exit(code=1)

    except PermissionError:

        console.print(
            "[bold red]Permission denied.[/bold red]"
        )

        raise typer.Exit(code=1)

    except Exception as error:

        console.print(
            f"[bold red]Analysis failed:[/bold red] "
            f"{error}"
        )

        raise typer.Exit(code=1)

    console.print(
        f"[green]Files analyzed:[/green] "
        f"{len(results)}"
    )

    console.print()

    for result in results:

        display_file(result)

        console.print()

    save_json_report(
        results,
        output
    )

    console.print(
        "\n[bold green]Analysis completed successfully.[/bold green]"
    )


@app.command()
def version():
    """
    Display toolkit version.
    """

    console.print(
        "[cyan]Windows Forensics Toolkit v1.0.0[/cyan]"
    )


if __name__ == "__main__":
    app()