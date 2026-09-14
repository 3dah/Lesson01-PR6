"""Run full export pipeline: diagrams → PDF → PPTX → preview renders."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(name: str):
    print(f"\n=== {name} ===")
    subprocess.check_call([sys.executable, str(SCRIPTS / name)], cwd=str(ROOT))


def main():
    run("generate_diagrams.py")
    run("build_pdf.py")
    run("build_pptx.py")
    print("\nDone. Outputs in exports/")


if __name__ == "__main__":
    main()
