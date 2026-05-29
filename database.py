import os
from pathlib import Path
from typing import Union
from urllib.parse import quote_plus, urlparse

import pandas as pd
from sqlalchemy import create_engine, inspect, text

PROJECT_DIR = Path(__file__).resolve().parent


def _load_env_file() -> None:
    env_path = PROJECT_DIR / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ[key.strip()] = value.strip()


try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_DIR / ".env", override=True)
except ImportError:
    _load_env_file()

TABLE_NAME = os.getenv("SALES_TABLE", "sales_orders")
SALES_TABLE = TABLE_NAME


class DatabaseConfigError(RuntimeError):
    pass


def _parse_supabase_project_ref(raw: str) -> str:
    value = raw.strip()
    if "supabase.co" in value:
        value = value.split("//")[-1]
        value = value.split(".supabase.co")[0]
    if "=" in value:
        value = value.split("=")[-1]
        if "supabase.co" in value:
            value = value.split("//")[-1].split(".supabase.co")[0]
    return value.strip("/")

def build_supabase_url() -> str:
    password = os.getenv("SUPABASE_DB_PASSWORD", "").strip()
    project_ref = _parse_supabase_project_ref(os.getenv("SUPABASE_PROJECT_REF", ""))

    if not password or not project_ref:
        raise DatabaseConfigError(
            "Set SUPABASE_PROJECT_REF and SUPABASE_DB_PASSWORD in your .env file."
        )

    user = os.getenv("SUPABASE_DB_USER", "postgres")
    host = os.getenv("SUPABASE_DB_HOST", f"db.{project_ref}.supabase.co")
    port = os.getenv("SUPABASE_DB_PORT", "5432")
    dbname = os.getenv("SUPABASE_DB_NAME", "postgres")

    return (
        f"postgresql+psycopg2://{user}:{quote_plus(password)}"
        f"@{host}:{port}/{dbname}?sslmode=require"
    )


def build_database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if url:
        if url.startswith("sqlite"):
            raise DatabaseConfigError(
                "Local SQLite is disabled. Use Supabase (PostgreSQL) in .env."
            )
        if "sslmode=" not in url and url.startswith("postgresql"):
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}sslmode=require"
        return url

    if os.getenv("SUPABASE_PROJECT_REF") or os.getenv("SUPABASE_DB_PASSWORD"):
        return build_supabase_url()

    raise DatabaseConfigError(
        "Supabase is not configured. Add SUPABASE_PROJECT_REF and "
        "SUPABASE_DB_PASSWORD to .env (see .env.example)."
    )


def get_engine():
    url = build_database_url()
    connect_args = {"connect_timeout": 30}

    if url.startswith("postgresql"):
        connect_args["sslmode"] = "require"

    if url.startswith("mysql"):
        connect_args["ssl"] = {"ssl_disabled": False}

    return create_engine(url, connect_args=connect_args, pool_pre_ping=True)


def table_exists(engine=None) -> bool:
    engine = engine or get_engine()
    return inspect(engine).has_table(TABLE_NAME)


def create_sales_table(engine=None) -> None:
    engine = engine or get_engine()
    ddl = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        order_id VARCHAR(50) PRIMARY KEY,
        order_date TIMESTAMP,
        customer_id VARCHAR(50),
        segment VARCHAR(50),
        region VARCHAR(50),
        state VARCHAR(50),
        category VARCHAR(50),
        sub_category VARCHAR(50),
        sales DOUBLE PRECISION,
        quantity INTEGER,
        discount DOUBLE PRECISION,
        profit DOUBLE PRECISION,
        profit_margin DOUBLE PRECISION,
        calculated_cost_basis DOUBLE PRECISION
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))


def load_csv_to_database(
    csv_path: Union[str, Path] = "cleaned_sales_data.csv",
    if_exists: str = "replace",
) -> int:
    csv_path = Path(csv_path)
    if not csv_path.is_absolute():
        csv_path = PROJECT_DIR / csv_path
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    engine = get_engine()
    create_sales_table(engine)

    df = pd.read_csv(csv_path, parse_dates=["order_date"])
    if if_exists == "replace":
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE {TABLE_NAME}"))

    df.to_sql(TABLE_NAME, engine, if_exists="append", index=False, chunksize=1000)
    return len(df)


def fetch_sales_data() -> pd.DataFrame:
    engine = get_engine()

    if not table_exists(engine):
        raise RuntimeError(
            f"Table '{TABLE_NAME}' not found in Supabase. Run: python setup_supabase.py"
        )

    df = pd.read_sql(text(f"SELECT * FROM {TABLE_NAME}"), engine)
    df["order_date"] = pd.to_datetime(df["order_date"])

    if "year" not in df.columns:
        df["year"] = df["order_date"].dt.year

    if "profit_margin" not in df.columns and {"profit", "sales"}.issubset(df.columns):
        df["profit_margin"] = (df["profit"] / df["sales"]) * 100

    return df


def get_connection_label() -> str:
    if os.getenv("SUPABASE_PROJECT_REF"):
        return f"Supabase ({os.getenv('SUPABASE_PROJECT_REF')})"

    url = build_database_url()
    parsed = urlparse(url.replace("+psycopg2", "").replace("+pymysql", ""))
    host = parsed.hostname or "unknown-host"
    database = (parsed.path or "").lstrip("/").split("?")[0] or "postgres"
    return f"{host} / {database}"
