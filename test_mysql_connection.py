"""Test MySQL connection and load CSV into the Sales database."""

import getpass
import os
import sys

from sqlalchemy import text

from database import DATABASE_URL, TABLE_NAME, build_database_url, get_engine, load_csv_to_database


def ensure_password() -> None:
    if os.getenv("MYSQL_PASSWORD") or os.getenv("DATABASE_URL"):
        return
    if not os.getenv("MYSQL_USER"):
        return
    password = getpass.getpass("MySQL password (root): ")
    os.environ["MYSQL_PASSWORD"] = password


def test_connection() -> None:
    ensure_password()
    url = build_database_url()
    print(f"Connecting to: {url.split('@')[-1] if '@' in url else url}")

    engine = get_engine()
    with engine.connect() as conn:
        db_name = conn.execute(text("SELECT DATABASE()")).scalar()
        version = conn.execute(text("SELECT VERSION()")).scalar()
        print(f"Connected! MySQL {version}, database: {db_name}")


def main() -> None:
    try:
        test_connection()
        rows = load_csv_to_database("cleaned_sales_data.csv", if_exists="replace")
        print(f"Loaded {rows:,} rows into table '{TABLE_NAME}'")
    except Exception as exc:
        err = str(exc)
        print(f"\nError: {err}")
        if "1045" in err or "Access denied" in err:
            print(
                "\nPassword galat hai. MySQL Workbench mein:"
                "\n  1. 'Sales Data' connection par right-click -> Edit Connection"
                "\n  2. 'Store in Vault' wala password dekho/copy karo"
                "\n  3. .env file mein MYSQL_PASSWORD=your_password likho"
                "\n  4. Phir run karo: python test_mysql_connection.py"
            )
        sys.exit(1)


if __name__ == "__main__":
    main()
