from pathlib import Path

import typer

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from database.database import initialize_database

from core.case_manager import (
    create_case as create_case_record,
    get_case,
    list_cases,
)

from core.evidence_manager import (
    add_evidence,
    get_evidence,
)

from core.artifact_engine import (
    collect_filesystem_artifacts,
)

from core.report_engine import (
    generate_json_report,
)


# ============================================================
# APPLICATION
# ============================================================

app = typer.Typer(
    help="Windows Digital Forensics Toolkit",
    add_completion=False,
)

console = Console()


# ============================================================
# BANNER
# ============================================================

def banner():
    console.print(
        Panel.fit(
            "[bold cyan]WINDOWS FORENSICS TOOLKIT[/bold cyan]\n"
            "Digital Evidence Analysis Platform",
            border_style="cyan",
        )
    )


# ============================================================
# VERSION
# ============================================================

@app.command()
def version():
    """
    Display toolkit version.
    """

    console.print(
        "[bold cyan]"
        "Windows Forensics Toolkit v2.0.0"
        "[/bold cyan]"
    )


# ============================================================
# CREATE CASE
# ============================================================

@app.command("create-case")
def create_case_command(
    case_id: str,
    name: str,
    investigator: str = typer.Option(
        "",
        "--investigator",
        "-i",
    ),
    description: str = typer.Option(
        "",
        "--description",
        "-d",
    ),
):
    """
    Create a new forensic investigation case.
    """

    try:

        case = create_case_record(
            case_id=case_id,
            name=name,
            investigator=investigator,
            description=description,
        )

        console.print(
            Panel(
                "[bold green]Case created successfully[/bold green]\n\n"
                f"Case ID      : {case['case_id']}\n"
                f"Case Name    : {case['name']}\n"
                f"Investigator : {case['investigator'] or '-'}\n"
                f"Description  : {case['description'] or '-'}\n"
                f"Created      : {case['created_at']}",
                title="FORENSIC CASE",
                border_style="green",
            )
        )

    except ValueError as error:

        console.print(
            Panel(
                f"[red]{error}[/red]",
                title="Case Creation Error",
                border_style="red",
            )
        )

    except Exception as error:

        console.print(
            Panel(
                f"[red]Unexpected error:[/red]\n\n"
                f"{error}",
                title="ERROR",
                border_style="red",
            )
        )

        raise typer.Exit(1)


# ============================================================
# LIST CASES
# ============================================================

@app.command("cases")
def cases():
    """
    List all forensic cases.
    """

    records = list_cases()

    if not records:

        console.print(
            Panel(
                "[yellow]No forensic cases found.[/yellow]",
                border_style="yellow",
            )
        )

        return

    table = Table(
        title="FORENSIC CASES",
        show_lines=True,
    )

    table.add_column(
        "Case ID",
        style="cyan",
    )

    table.add_column(
        "Name",
    )

    table.add_column(
        "Investigator",
    )

    table.add_column(
        "Created",
    )

    for case in records:

        table.add_row(
            case["case_id"],
            case["name"],
            case["investigator"] or "-",
            str(case["created_at"]),
        )

    console.print(table)


# ============================================================
# SHOW CASE
# ============================================================

@app.command("case-info")
def case_info(
    case_id: str,
):
    """
    Display information about a forensic case.
    """

    case = get_case(case_id)

    if case is None:

        console.print(
            f"[red]Case not found: {case_id}[/red]"
        )

        raise typer.Exit(1)

    console.print(
        Panel(
            f"Case ID      : {case['case_id']}\n"
            f"Name         : {case['name']}\n"
            f"Investigator : {case['investigator'] or '-'}\n"
            f"Description  : {case['description'] or '-'}\n"
            f"Created      : {case['created_at']}",
            title="CASE INFORMATION",
            border_style="cyan",
        )
    )


# ============================================================
# ADD EVIDENCE
# ============================================================

@app.command("evidence")
def evidence(
    case_id: str,
    path: str,
):
    """
    Register forensic evidence and calculate hashes.
    """

    case = get_case(case_id)

    if case is None:

        console.print(
            f"[red]Case not found: {case_id}[/red]"
        )

        raise typer.Exit(1)

    evidence_path = Path(path)

    if not evidence_path.exists():

        console.print(
            f"[red]Evidence path does not exist:[/red]\n"
            f"{evidence_path}"
        )

        raise typer.Exit(1)

    try:

        record = add_evidence(
            case_id,
            evidence_path,
        )

        console.print(
            Panel(
                "[bold green]Evidence registered successfully[/bold green]\n\n"
                f"Evidence ID : {record.evidence_id}\n"
                f"Case ID     : {record.case_id}\n"
                f"Name        : {record.name}\n"
                f"Path        : {record.path}\n"
                f"Size        : {record.size:,} bytes\n\n"
                f"[bold]MD5[/bold]\n"
                f"{record.md5}\n\n"
                f"[bold]SHA-1[/bold]\n"
                f"{record.sha1}\n\n"
                f"[bold]SHA-256[/bold]\n"
                f"{record.sha256}\n\n"
                f"[bold]SHA-512[/bold]\n"
                f"{record.sha512}",
                title="EVIDENCE INTEGRITY",
                border_style="green",
            )
        )

    except Exception as error:

        console.print(
            Panel(
                f"[red]Evidence registration failed:[/red]\n\n"
                f"{error}",
                title="ERROR",
                border_style="red",
            )
        )

        raise typer.Exit(1)


# ============================================================
# LIST EVIDENCE
# ============================================================

@app.command("list-evidence")
def list_evidence(
    case_id: str,
):
    """
    List evidence registered for a case.
    """

    case = get_case(case_id)

    if case is None:

        console.print(
            f"[red]Case not found: {case_id}[/red]"
        )

        raise typer.Exit(1)

    records = get_evidence(case_id)

    if not records:

        console.print(
            "[yellow]No evidence registered for this case.[/yellow]"
        )

        return

    table = Table(
        title=f"EVIDENCE — {case_id}",
        show_lines=True,
    )

    table.add_column(
        "Evidence ID",
        style="cyan",
    )

    table.add_column(
        "Name",
    )

    table.add_column(
        "Size",
    )

    table.add_column(
        "SHA-256",
    )

    for record in records:

        table.add_row(
            record.evidence_id,
            record.name,
            f"{record.size:,} bytes",
            record.sha256,
        )

    console.print(table)


# ============================================================
# ANALYZE
# ============================================================

@app.command("analyze")
def analyze(
    case_id: str,
    path: str,
):
    """
    Analyze files inside an evidence path.
    """

    case = get_case(case_id)

    if case is None:

        console.print(
            f"[red]Case not found: {case_id}[/red]"
        )

        raise typer.Exit(1)

    evidence_records = get_evidence(
        case_id
    )

    if not evidence_records:

        console.print(
            "[yellow]"
            "No evidence registered for this case. "
            "Add evidence first."
            "[/yellow]"
        )

        raise typer.Exit(1)

    target = Path(path)

    if not target.exists():

        console.print(
            f"[red]Path does not exist:[/red]\n"
            f"{target}"
        )

        raise typer.Exit(1)

    evidence_record = evidence_records[-1]

    console.print(
        Panel(
            f"Case       : {case_id}\n"
            f"Evidence   : {evidence_record.evidence_id}\n"
            f"Target     : {target}\n\n"
            "[cyan]Starting filesystem analysis...[/cyan]",
            title="FORENSIC ANALYSIS",
            border_style="cyan",
        )
    )

    try:

        results = collect_filesystem_artifacts(
            target,
            case_id,
            evidence_record.evidence_id,
        )

        console.print(
            f"[green]Files analyzed:[/green] "
            f"{len(results)}"
        )

        report = generate_json_report(
            case_id,
            results,
        )

        console.print(
            Panel(
                "[bold green]Analysis completed successfully[/bold green]\n\n"
                f"Files analyzed : {len(results)}\n"
                f"Report         : {report}",
                title="ANALYSIS RESULT",
                border_style="green",
            )
        )

    except PermissionError:

        console.print(
            "[red]Permission denied while accessing "
            "the evidence path.[/red]"
        )

        raise typer.Exit(1)

    except Exception as error:

        console.print(
            Panel(
                f"[red]Analysis failed:[/red]\n\n"
                f"{error}",
                title="ANALYSIS ERROR",
                border_style="red",
            )
        )

        raise typer.Exit(1)


# ============================================================
# TIMELINE
# ============================================================

@app.command("timeline")
def timeline(
    case_id: str,
    path: str,
):
    """
    Generate a filesystem forensic timeline.
    """

    case = get_case(case_id)

    if case is None:

        console.print(
            f"[red]Case not found: {case_id}[/red]"
        )

        raise typer.Exit(1)

    evidence_records = get_evidence(
        case_id
    )

    if not evidence_records:

        console.print(
            "[yellow]No evidence registered.[/yellow]"
        )

        raise typer.Exit(1)

    target = Path(path)

    if not target.exists():

        console.print(
            f"[red]Path does not exist:[/red]\n"
            f"{target}"
        )

        raise typer.Exit(1)

    from timeline.timeline import (
        generate_file_timeline,
    )

    try:

        events = generate_file_timeline(
            target,
            case_id,
            evidence_records[-1].evidence_id,
        )

        if not events:

            console.print(
                "[yellow]No timeline events found.[/yellow]"
            )

            return

        table = Table(
            title=f"FORENSIC TIMELINE — {case_id}",
            show_lines=True,
        )

        table.add_column(
            "Timestamp",
            style="cyan",
        )

        table.add_column(
            "Type",
        )

        table.add_column(
            "Source",
        )

        table.add_column(
            "Description",
        )

        for event in events:

            table.add_row(
                str(event["timestamp"]),
                event["event_type"],
                event["source"],
                event["description"],
            )

        console.print(table)

    except PermissionError:

        console.print(
            "[red]Permission denied while accessing "
            "the evidence path.[/red]"
        )

        raise typer.Exit(1)

    except Exception as error:

        console.print(
            Panel(
                f"[red]Timeline generation failed:[/red]\n\n"
                f"{error}",
                title="TIMELINE ERROR",
                border_style="red",
            )
        )

        raise typer.Exit(1)


# ============================================================
# HELP
# ============================================================

@app.command("info")
def info():
    """
    Display information about the toolkit.
    """

    console.print(
        Panel(
            "[bold cyan]Windows Forensics Toolkit v2.0.0[/bold cyan]\n\n"
            "A Python-based digital forensics platform "
            "for Windows evidence analysis.\n\n"
            "Current capabilities:\n"
            "• Case management\n"
            "• Evidence registration\n"
            "• MD5 / SHA-1 / SHA-256 / SHA-512\n"
            "• Filesystem analysis\n"
            "• Filesystem timeline generation\n"
            "• JSON forensic reports",
            title="ABOUT",
            border_style="cyan",
        )
    )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    # Create database tables if they do not exist.
    initialize_database()

    banner()

    app()