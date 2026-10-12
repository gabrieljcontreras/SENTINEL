"""Apply bundled SQL migrations once, then optionally seed a fresh demo database."""
import argparse
from pathlib import Path

from app.db import connect
from app.demo_org import DEMO_ORGANIZATION_ID
from app.services.ingest import ingest_kit

ROOT = Path(__file__).resolve().parents[2]


def migrate() -> None:
    with connect() as conn:
        # Serialize schema changes when deployments overlap.
        conn.execute("SELECT pg_advisory_xact_lock(73636842)")
        conn.execute("CREATE SCHEMA IF NOT EXISTS sentinel")
        conn.execute("""CREATE TABLE IF NOT EXISTS sentinel.schema_migrations (
            name TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )""")
        applied = {row["name"] for row in conn.execute("SELECT name FROM sentinel.schema_migrations")}
        for path in sorted((ROOT / "database").glob("[0-9]*.sql")):
            if path.name in applied:
                continue
            conn.execute(path.read_text())
            conn.execute("INSERT INTO sentinel.schema_migrations (name) VALUES (%s)", (path.name,))
            print(f"Applied {path.name}", flush=True)
        conn.commit()


def seed_demo() -> None:
    with connect() as conn:
        exists = conn.execute(
            "SELECT 1 FROM sentinel.missions WHERE organization_id = %s AND source = 'kit' LIMIT 1",
            (DEMO_ORGANIZATION_ID,),
        ).fetchone()
    if exists:
        print("Challenge data already loaded; leaving records unchanged.", flush=True)
        return
    data_dir = ROOT / "SPOT_KnightHacks_Challenge_Kit Part One" / "02_DATA"
    batch = ingest_kit(data_dir)
    print(f"Loaded {len(batch.missions)} missions and {len(batch.actions)} actions.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-demo", action="store_true")
    args = parser.parse_args()
    migrate()
    if args.seed_demo:
        seed_demo()
