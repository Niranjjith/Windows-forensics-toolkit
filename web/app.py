from pathlib import Path

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database.database import initialize_database

from core.case_manager import (
    create_case,
    get_case,
    list_cases,
)

from core.evidence_manager import (
    add_evidence,
    get_evidence,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

EVIDENCE_DIR = PROJECT_DIR / "evidence"

EVIDENCE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# DATABASE
# ============================================================

initialize_database()


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Windows Forensics Toolkit",
    description="Digital Forensics Investigation Platform",
    version="2.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


templates = Jinja2Templates(
    directory=TEMPLATE_DIR
)


# ============================================================
# DASHBOARD
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def dashboard(
    request: Request,
):

    cases = list_cases()

    total_cases = len(cases)

    total_evidence = 0

    for case in cases:

        records = get_evidence(
            case["case_id"]
        )

        total_evidence += len(records)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "cases": cases,
            "total_cases": total_cases,
            "total_evidence": total_evidence,
        },
    )


# ============================================================
# CASES
# ============================================================

@app.get(
    "/cases",
    response_class=HTMLResponse
)
async def cases_page(
    request: Request,
):

    cases = list_cases()

    return templates.TemplateResponse(
        "cases.html",
        {
            "request": request,
            "cases": cases,
        },
    )


# ============================================================
# CREATE CASE PAGE
# ============================================================

@app.get(
    "/cases/create",
    response_class=HTMLResponse
)
async def create_case_page(
    request: Request,
):

    return templates.TemplateResponse(
        "case_detail.html",
        {
            "request": request,
            "case": None,
            "evidence": [],
        },
    )


# ============================================================
# CREATE CASE
# ============================================================

@app.post(
    "/cases/create"
)
async def create_case_web(
    case_id: str = Form(...),
    name: str = Form(...),
    investigator: str = Form(""),
    description: str = Form(""),
):

    try:

        create_case(
            case_id=case_id,
            name=name,
            investigator=investigator,
            description=description,
        )

    except ValueError:

        return RedirectResponse(
            "/cases?error=case_exists",
            status_code=303,
        )

    return RedirectResponse(
        f"/cases/{case_id}",
        status_code=303,
    )


# ============================================================
# CASE DETAILS
# ============================================================

@app.get(
    "/cases/{case_id}",
    response_class=HTMLResponse
)
async def case_details(
    request: Request,
    case_id: str,
):

    case = get_case(case_id)

    if case is None:

        return RedirectResponse(
            "/cases",
            status_code=303,
        )

    evidence = get_evidence(
        case_id
    )

    return templates.TemplateResponse(
        "case_detail.html",
        {
            "request": request,
            "case": case,
            "evidence": evidence,
        },
    )


# ============================================================
# UPLOAD EVIDENCE
# ============================================================

@app.post(
    "/cases/{case_id}/evidence"
)
async def upload_evidence(
    case_id: str,
    file: UploadFile = File(...),
):

    case = get_case(case_id)

    if case is None:

        return RedirectResponse(
            "/cases",
            status_code=303,
        )

    case_dir = (
        EVIDENCE_DIR / case_id
    )

    case_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = (
        case_dir / file.filename
    )

    contents = await file.read()

    destination.write_bytes(
        contents
    )

    try:

        add_evidence(
            case_id,
            destination,
        )

    except Exception as error:

        print(
            f"Evidence error: {error}"
        )

    return RedirectResponse(
        f"/cases/{case_id}",
        status_code=303,
    )


# ============================================================
# EVIDENCE
# ============================================================

@app.get(
    "/cases/{case_id}/evidence",
    response_class=HTMLResponse
)
async def evidence_page(
    request: Request,
    case_id: str,
):

    case = get_case(case_id)

    if case is None:

        return RedirectResponse(
            "/cases",
            status_code=303,
        )

    evidence = get_evidence(
        case_id
    )

    return templates.TemplateResponse(
        "evidence.html",
        {
            "request": request,
            "case": case,
            "evidence": evidence,
        },
    )


# ============================================================
# TIMELINE
# ============================================================

@app.get(
    "/cases/{case_id}/timeline",
    response_class=HTMLResponse
)
async def timeline_page(
    request: Request,
    case_id: str,
):

    case = get_case(case_id)

    if case is None:

        return RedirectResponse(
            "/cases",
            status_code=303,
        )

    evidence = get_evidence(
        case_id
    )

    events = []

    if evidence:

        try:

            from timeline.timeline import (
                generate_file_timeline
            )

            latest = evidence[-1]

            events = generate_file_timeline(
                Path(latest.path),
                case_id,
                latest.evidence_id,
            )

        except Exception as error:

            print(
                f"Timeline error: {error}"
            )

    return templates.TemplateResponse(
        "timeline.html",
        {
            "request": request,
            "case": case,
            "evidence": evidence,
            "events": events,
        },
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
async def health():

    return {
        "status": "online",
        "application": "Windows Forensics Toolkit",
        "version": "2.0.0",
    }