# Enterprise Sales Performance Analytics Dashboard

An interactive sales analytics dashboard built with **Streamlit** and **Plotly**. Despite the repository name, this project is a Python web application—not a Power BI (`.pbix`) report. It simulates enterprise retail sales data, runs lightweight ETL, and presents KPIs and multi-dimensional charts in a polished, Apple-inspired UI.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Data Model](#data-model)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Connect CSV to Live Database](#connect-csv-to-live-database)
- [Dashboard Layout](#dashboard-layout)
- [ETL Pipeline](#etl-pipeline)
- [Business Logic & Insights](#business-logic--insights)
- [Customization](#customization)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project demonstrates an end-to-end analytics workflow:

1. **Generate** synthetic sales order data (~10,500 records)
2. **Clean & enrich** records with derived metrics (profit margin, cost basis)
3. **Visualize** performance through KPI cards and interactive charts

The main entry point is `app.py`, which reads sales data from a **live database** (SQLite by default), caches it with Streamlit, and renders a wide-layout dashboard. CSV data is loaded into the database via `load_csv_to_db.py` or automatically at the end of `etl_pipeline.py`.

---

## Features

| Area | Description |
|------|-------------|
| **KPI metrics** | Total orders, average profit margin, units sold, average order value, gross revenue |
| **Segment analysis** | Donut chart of sales split by customer segment |
| **Trend analysis** | Stacked bar chart of revenue by year and product category |
| **Geographic insights** | Top 5 states by sales (horizontal bar chart) |
| **Volume vs. value** | Sales aggregated by order quantity |
| **Discount analysis** | Order density across discount tiers (0%, 10%, 20%, 50%) |
| **Product mix** | Top sub-categories by revenue |
| **Regional breakdown** | Stacked bar of sales by region and customer segment |
| **Premium UI** | Dark header banner, light canvas, rounded white chart cards, custom metric styling |
| **Performance** | `@st.cache_data` caches generated dataset across Streamlit reruns |

---

## Project Structure

```
power_bi-main/
├── app.py                  # Main Streamlit dashboard (reads from database)
├── database.py             # Database connection, CSV load, and query helpers
├── load_csv_to_db.py       # Import cleaned_sales_data.csv into the database
├── etl_pipeline.py         # ETL script; exports CSV and syncs to database
├── cleaned_sales_data.csv  # Pre-generated cleaned dataset (~10,500 rows)
├── sales.db                # Local SQLite database (created after first load)
├── .env.example            # Database connection template
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Ignores venv/, .env, *.db
```

---

## Tech Stack

| Technology | Role |
|------------|------|
| [Python 3](https://www.python.org/) | Core language |
| [Streamlit](https://streamlit.io/) | Web UI framework and app server |
| [Pandas](https://pandas.pydata.org/) | Data manipulation and aggregation |
| [NumPy](https://numpy.org/) | Random data generation and numerical ops |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Interactive charts |
| [SQLAlchemy](https://www.sqlalchemy.org/) | Database connection and CSV import |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Load database URL from `.env` |

### Dependencies

Listed in `requirements.txt`:

```
streamlit
pandas
plotly
sqlalchemy
python-dotenv
```

> **Note:** `numpy` is required by the code but not explicitly pinned in `requirements.txt`. It is installed automatically as a Pandas dependency. For reproducible environments, consider adding `numpy` with a version pin.

---

## Data Model

### Source Fields

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Unique order ID (format: `CA-2025-XXXXXX`) |
| `order_date` | datetime | Order date (range: ~2024–2025) |
| `customer_id` | string | Customer ID (format: `CS-XXXX`) |
| `segment` | categorical | `Consumer`, `Corporate`, or `Home Office` |
| `region` | categorical | `North`, `South`, `East`, or `West` |
| `state` | categorical | Indian state mapped to region |
| `category` | categorical | `Furniture`, `Office Supplies`, or `Technology` |
| `sub_category` | categorical | Product sub-category (e.g., Chairs, Paper, Phones) |
| `sales` | float | Net sales after discount |
| `quantity` | int | Units ordered (1–9) |
| `discount` | float | Discount rate (0.0, 0.1, 0.2, or 0.5) |
| `profit` | float | Order profit (can be negative for specific scenarios) |

### Derived Fields

| Column | Formula / Logic | Available In |
|--------|-----------------|--------------|
| `profit_margin` | `(profit / sales) × 100` | `app.py`, CSV |
| `year` | Extracted from `order_date` | `app.py` only |
| `calculated_cost_basis` | `sales - profit` | `etl_pipeline.py`, CSV |

### Dimensions & Hierarchies

- **Region → State:** Each region maps to four states (e.g., South → Karnataka, Tamil Nadu, Telangana, Kerala)
- **Category → Sub-category:** Each category has predefined sub-categories (e.g., Technology → Phones, Accessories, Copiers)

---

## Architecture

```
CSV (cleaned_sales_data.csv)
        │
        ▼
  load_csv_to_db.py  ──►  Live Database (SQLite / PostgreSQL / MySQL)
        │                          │
        │                          ▼
  etl_pipeline.py (auto-sync)   app.py (Streamlit dashboard)
```

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit App (app.py)                  │
├─────────────────────────────────────────────────────────────┤
│  1. Page config & custom CSS                                │
│  2. load_sales_data()  [@st.cache_data, ttl=60s]            │
│     └── fetch_sales_data() from database.py                 │
│  3. KPI metric row (5 columns)                              │
│  4. Middle charts (3 columns)                               │
│  5. Bottom charts (4 columns)                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Standalone ETL (etl_pipeline.py)               │
├─────────────────────────────────────────────────────────────┤
│  Generate data → Clean → Export CSV → Sync to database      │
└─────────────────────────────────────────────────────────────┘
```

The dashboard reads from the **live database**, not directly from the CSV file. Reload the CSV into the database whenever your file changes.

---

## Getting Started

### Prerequisites

- Python 3.8 or newer
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd power_bi-main
   ```

2. **Create and activate a virtual environment (recommended)**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Step 1 — Load CSV into the Database (first time)

```bash
python load_csv_to_db.py
```

This reads `cleaned_sales_data.csv` and stores all rows in the `sales_orders` table inside `sales.db` (SQLite).

### Step 2 — Run the Dashboard

```bash
streamlit run app.py
```

Streamlit opens the app in your browser (default: `http://localhost:8501`). The dashboard reads live data from the database and refreshes every 60 seconds.

### Generate Fresh Data (Optional)

```bash
python etl_pipeline.py
```

This generates new mock data, saves `cleaned_sales_data.csv`, and **automatically syncs it to the database**.

---

## Connect CSV to Live Database

### How it works

| Step | What happens |
|------|----------------|
| 1 | Your sales data lives in `cleaned_sales_data.csv` |
| 2 | `load_csv_to_db.py` imports the CSV into a database table (`sales_orders`) |
| 3 | `app.py` queries the database — not the CSV file directly |
| 4 | When the CSV updates, re-run `load_csv_to_db.py` (or `etl_pipeline.py`) to refresh the database |

This gives you a **single source of truth** in the database. The dashboard always shows what's in the DB, and you can connect other tools (Power BI, Excel, etc.) to the same database.

### Default: SQLite (easiest — no server install)

SQLite is a file-based database. After running `load_csv_to_db.py`, you'll see `sales.db` in the project folder. No extra setup required.

### Use PostgreSQL or MySQL (production)

1. Copy the environment template:

   ```bash
   copy .env.example .env
   ```

2. Edit `.env` with your connection string:

   ```env
   # PostgreSQL
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/sales_db

   # MySQL
   DATABASE_URL=mysql+pymysql://username:password@localhost:3306/sales_db
   ```

3. Install the driver:

   ```bash
   pip install psycopg2-binary   # PostgreSQL
   pip install pymysql           # MySQL
   ```

4. Load your CSV:

   ```bash
   python load_csv_to_db.py
   ```

5. Run the dashboard:

   ```bash
   streamlit run app.py
   ```

### Update data when CSV changes

Whenever you replace or edit `cleaned_sales_data.csv`, reload it:

```bash
python load_csv_to_db.py
```

The dashboard cache refreshes within 60 seconds, or restart Streamlit for an immediate update.

---

## Dashboard Layout

### Header

- Title: **Enterprise Sales Performance Analytics**
- Subtitle: Metrics Overview | Multi-Dimensional Canvas Analysis
- Dark banner with blue accent border

### Row 1 — KPI Metrics (5 cards)

| Metric | Calculation |
|--------|-------------|
| Total Orders Tracked | Unique count of `order_id` |
| Avg Profit Margin | Mean of `profit_margin` (%) |
| Total Units Sold | Sum of `quantity` |
| Avg Order Value | Mean of `sales` ($) |
| Gross Revenue Return | Sum of `sales`, displayed in millions ($M) |

### Row 2 — Primary Charts (3 panels)

1. **Sales Split by Customer Segment** — Donut chart (`px.pie`, hole=0.6)
2. **Historical Revenue Inflow Trend & Categories Stack** — Stacked bar by `year` and `category`
3. **Top Performing States Growth Engine** — Top 5 states by sales (horizontal bar)

### Row 3 — Deep-Dive Charts (4 panels)

1. **Volume Clusters vs Value Return** — Sales by `quantity`
2. **Order Densities across Discount Tiers** — Order count by `discount`
3. **Revenue Return by Product Sub-Category** — Top 6 sub-categories
4. **Regional Contribution and Segment Leakage** — Stacked bar by `region` and `segment`

All charts use Plotly with a consistent blue color palette (`#3182ce`, `#63b3ed`, `#90cdf4`, etc.).

---

## ETL Pipeline

`etl_pipeline.py` performs the following steps:

1. **Generate** 10,500 synthetic records (`np.random.seed(42)` for reproducibility)
2. **Introduce missing values** — Sets ~1% of `discount` values to `NaN` (simulated data quality issue)
3. **Clean**
   - Drop rows with missing `order_id` or `sales`
   - Fill missing `discount` with `0.0`
   - Parse `order_date` as datetime
4. **Engineer features**
   - `profit_margin`
   - `calculated_cost_basis`
5. **Export** to `cleaned_sales_data.csv`

The in-app ETL in `app.py` follows similar generation and cleaning logic but skips the intentional missing-value injection and CSV export.

---

## Business Logic & Insights

### Simulated Profit Anomaly

Orders for **Tables** in the **South** region are assigned **negative profit** (10–40% of sales). This models a real-world scenario where certain product–region combinations underperform and helps surface loss-making segments in the dashboard.

### Discount Distribution

| Discount | Approx. Share |
|----------|---------------|
| 0% | 60% |
| 10% | 20% |
| 20% | 10% |
| 50% | 10% |

### Customer Segments

| Segment | Approx. Share |
|---------|---------------|
| Consumer | 50% |
| Corporate | 30% |
| Home Office | 20% |

### Categories

| Category | Approx. Share |
|----------|---------------|
| Office Supplies | 40% |
| Furniture | 30% |
| Technology | 30% |

---

## Customization

### Connect the Dashboard to CSV

The dashboard no longer reads CSV directly. Use `load_csv_to_db.py` to import your file into the database first.

### Change Record Count

Update `n_records` in both `app.py` and `etl_pipeline.py` (default: `10500`).

### Adjust Styling

Custom CSS is injected via `st.markdown(..., unsafe_allow_html=True)` at the top of `app.py`. Modify colors, fonts, and card styles in the `<style>` blocks.

### Add Filters

Streamlit widgets (e.g., `st.selectbox`, `st.date_input`) can be added above the KPI row to filter `df` before aggregations.

---

## Limitations

- **Cloud Warehousing Layer (Supabase PostgreSQL):** Secure relational cloud data management. Serves as the high-availability core database repository handling complex query operations.
- **No authentication** — Dashboard is open to anyone with access to the running server
- **Manual CSV reload** — Database does not auto-watch the CSV file; re-run `load_csv_to_db.py` after CSV changes
- **No automated tests** — Manual verification only

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to your branch
5. Open a pull request

Suggestions for improvements:

- Extract shared data generation into a `data_generator.py` module
- Add Streamlit sidebar filters (date range, region, segment)
- Pin all dependencies with versions in `requirements.txt`
- Add unit tests for ETL transformations
- Provide a sample Power BI template that consumes `cleaned_sales_data.csv`

---

## License

No license file is included in this repository. Contact the repository owner for usage terms.

---

## Author

Initial commits by **Rishi Sonkar** — Data Analysis project.
