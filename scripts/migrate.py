"""
Run database migrations.

Usage:
  python scripts/migrate.py --local    # SQLite (instance/app.db)
  python scripts/migrate.py --prod     # PostgreSQL via DATABASE_URL in .env
"""

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_FLASK = os.path.join(ROOT, ".venv", "bin", "flask")


def run(env: dict):
    result = subprocess.run(
        [VENV_FLASK, "--app", "wsgi.py", "db", "upgrade"],
        cwd=ROOT,
        env={**os.environ, **env},
    )
    sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Run database migrations.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--local", action="store_true", help="Migrate local SQLite (instance/app.db)")
    group.add_argument("--prod",  action="store_true", help="Migrate production DB via DATABASE_URL in .env")
    args = parser.parse_args()

    if args.local:
        db_path = os.path.join(ROOT, "instance", "app.db")
        print(f"[migrate] target: SQLite → {db_path}")
        run({"DATABASE_URL": f"sqlite:///{db_path}"})
    else:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(ROOT, ".env"))
        db_url = os.environ.get("DATABASE_URL", "")
        if not db_url:
            print("[migrate] ERROR: DATABASE_URL not set in .env", file=sys.stderr)
            sys.exit(1)
        # Mask credentials for display
        display = db_url.split("@")[-1] if "@" in db_url else db_url
        print(f"[migrate] target: PostgreSQL → ...@{display}")
        run({"DATABASE_URL": db_url})


if __name__ == "__main__":
    main()
