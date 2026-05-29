"""
Set up Supabase table and upload sales data.

Steps:
1. Create a project at https://supabase.com
2. Copy Project URL ref from Settings -> General (e.g. abcdefghijklmnop)
3. Copy database password from Settings -> Database
4. Fill .env and run: python setup_supabase.py
"""

import sys

from sqlalchemy import text

from database import (
    SALES_TABLE,
    create_sales_table,
    get_connection_label,
    get_engine,
    load_csv_to_database,
)


def main():
    try:
        print(f"Connecting to {get_connection_label()}...")
        engine = get_engine()

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        print("Creating table if needed...")
        create_sales_table(engine)

        print("Uploading cleaned_sales_data.csv to Supabase...")
        rows = load_csv_to_database("cleaned_sales_data.csv", if_exists="replace")

        with engine.connect() as conn:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {SALES_TABLE}")).scalar()

        print(f"Done. {rows:,} rows uploaded. Supabase table '{SALES_TABLE}' has {count:,} rows.")
        print("Run dashboard: streamlit run app.py")
    except Exception as exc:
        print(f"Supabase setup failed: {exc}")
        print("\nCheck .env:")
        print("  SUPABASE_PROJECT_REF=your-project-ref")
        print("  SUPABASE_DB_PASSWORD=your-database-password")
        sys.exit(1)


if __name__ == "__main__":
    main()
