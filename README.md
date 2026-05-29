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

The main entry point is `app.py`, which generates data in memory, caches it with Streamlit, and renders a wide-layout dashboard. A standalone script, `etl_pipeline.py`, can export the same dataset to CSV for offline analysis or use in other BI tools (including Power BI).

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
├── app.py                  # Main Streamlit dashboard application
├── etl_pipeline.py         # Standalone ETL script; exports cleaned_sales_data.csv
├── cleaned_sales_data.csv  # Pre-generated cleaned dataset (~10,500 rows)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Ignores venv/
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

### Dependencies

Listed in `requirements.txt`:

```
streamlit
pandas
plotly
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
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit App (app.py)                  │
├─────────────────────────────────────────────────────────────┤
│  1. Page config & custom CSS (dark header, card layout)   │
│  2. generate_and_clean_data()  [@st.cache_data]             │
│     └── NumPy random generation → Pandas DataFrame          │
│  3. KPI metric row (5 columns)                              │
│  4. Middle charts (3 columns)                               │
│  5. Bottom charts (4 columns)                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Standalone ETL (etl_pipeline.py)               │
├─────────────────────────────────────────────────────────────┤
│  Generate data → Introduce missing discounts (1%) → Clean   │
│  → Feature engineering → Export cleaned_sales_data.csv      │
└─────────────────────────────────────────────────────────────┘
```

**Important:** The dashboard (`app.py`) generates its own in-memory dataset and does **not** read `cleaned_sales_data.csv`. The CSV is produced separately by `etl_pipeline.py` for external use.

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

### Run the Dashboard

```bash
streamlit run app.py
```

Streamlit opens the app in your browser (default: `http://localhost:8501`).

### Generate Cleaned CSV (Optional)

```bash
python etl_pipeline.py
```

This creates or overwrites `cleaned_sales_data.csv` in the project root. You can import this file into Excel, Power BI, Tableau, or other analytics tools.

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

To use the exported file instead of in-memory generation, replace the data load in `app.py`:

```python
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_sales_data.csv', parse_dates=['order_date'])
    df['year'] = df['order_date'].dt.year
    return df

df = load_data()
```

### Change Record Count

Update `n_records` in both `app.py` and `etl_pipeline.py` (default: `10500`).

### Adjust Styling

Custom CSS is injected via `st.markdown(..., unsafe_allow_html=True)` at the top of `app.py`. Modify colors, fonts, and card styles in the `<style>` blocks.

### Add Filters

Streamlit widgets (e.g., `st.selectbox`, `st.date_input`) can be added above the KPI row to filter `df` before aggregations.

---

## Limitations

- **Synthetic data only** — No live database or API integration
- **No authentication** — Dashboard is open to anyone with access to the running server
- **Data source split** — `app.py` and `etl_pipeline.py` duplicate generation logic; they are not synchronized via a shared module
- **No automated tests** — Manual verification only
- **Repository naming** — Named "power_bi" but implements Streamlit; use `cleaned_sales_data.csv` if you need Power BI integration

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
