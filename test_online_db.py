"""Test Supabase online database connection."""

import sys

from sqlalchemy import text

from database import SALES_TABLE, get_connection_label, get_engine, table_exists


def main():
    try:
        print(f"Testing {get_connection_label()}...")
        engine = get_engine()

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Connection OK")

        if table_exists(engine):
            with engine.connect() as conn:
                count = conn.execute(text(f"SELECT COUNT(*) FROM {SALES_TABLE}")).scalar()
            print(f"Table '{SALES_TABLE}': {count:,} rows")
        else:
            print(f"Connected, but table '{SALES_TABLE}' not found. Run: python setup_supabase.py")
    except Exception as exc:
        print(f"Failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
