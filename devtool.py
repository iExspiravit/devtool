import argparse
import json
from pathlib import Path


def count_py_files_and_lines(root: Path) -> tuple[int, int]:
    py_files = []
    total_lines = 0

    for file_path in root.rglob("*.py"):
        # ignore venvs and common junk dirs
        if ".venv" in file_path.parts or "__pycache__" in file_path.parts:
            continue

        py_files.append(file_path)

        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                for _ in f:
                    total_lines += 1
        except Exception:
            continue

    return len(py_files), total_lines


def build_report(root: Path) -> dict:
    py_count, line_count = count_py_files_and_lines(root)
    return {
        "path": str(root),
        "python_files": py_count,
        "total_lines": line_count,
    }


def format_text_report(report: dict) -> str:
    return (
        f"Analyzing: {report['path']}\n"
        f"Python files: {report['python_files']}\n"
        f"Total lines : {report['total_lines']}\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="DevTool – Simple project analysis CLI")
    parser.add_argument("path", help="Path to the project directory")
    parser.add_argument("--out", help="Write report to a file (text)")
    parser.add_argument("--json", action="store_true", help="Print report as JSON")

    args = parser.parse_args()
    root = Path(args.path).expanduser().resolve()

    if not root.exists():
        print(f"Error: path does not exist: {root}")
        raise SystemExit(2)
    if not root.is_dir():
        print(f"Error: path is not a directory: {root}")
        raise SystemExit(2)

    report = build_report(root)

    if args.json:
        output = json.dumps(report, indent=2)
    else:
        output = format_text_report(report)

    print(output)

    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_path.write_text(output, encoding="utf-8")
        print(f"Wrote report to: {out_path}")


if __name__ == "__main__":
    main()

