# Windows Forensics Toolkit

A Python-based Windows digital forensics toolkit for file analysis,
cryptographic hashing, timeline generation, artifact analysis,
and forensic reporting.

## Features

- File discovery
- File metadata analysis
- MD5 hashing
- SHA-1 hashing
- SHA-256 hashing
- Recursive directory analysis
- JSON forensic reports
- CLI interface
- Forensic logging

## Technologies

- Python
- Typer
- Rich
- Python-Magic

## Project Structure

```text
Windows-forensics-toolkit/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── modules/
│   ├── __init__.py
│   └── file_analyzer.py
│
├── utils/
│   ├── __init__.py
│   └── logger.py
│
├── evidence/
├── reports/
└── tests/
    ├── test_hashing.py
    └── test_file.txt