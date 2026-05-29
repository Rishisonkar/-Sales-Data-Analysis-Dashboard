"""Upload local CSV rows into the online database table (optional admin script)."""

import sys

from database import TABLE_NAME, get_connection_label, load_csv_to_database


def main():
    try:
        rows = load_csv_to_database("cleaned_sales_data.csv", if_exists="replace")
    except Exception as exc:
        print(f"Upload failed: {exc}")
        sys.exit(1)

    print(f"Loaded {rows:,} rows into '{TABLE_NAME}' on {get_connection_label()}")


if __name__ == "__main__":
    main()
