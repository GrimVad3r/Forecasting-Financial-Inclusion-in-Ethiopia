# Forecasting Financial Inclusion in Ethiopia

This project builds a forecasting system that tracks Ethiopia’s digital financial transformation using time series and event‑impact methods.

***

## Project Overview

This repository contains code, data, and documentation for forecasting Ethiopia’s financial inclusion progress on two Global Findex core dimensions:

- **Access** – Account Ownership Rate (share of adults 15+ with an account at a financial institution or who used mobile money in the past 12 months).
- Usage – Digital Payment Adoption Rate (share of adults 15+ who made or received a digital payment or used an account to pay bills or shop online in the past 12 months).

You act as a Data Scientist at Selam Analytics, supporting a consortium including development finance institutions, mobile money operators, and the National Bank of Ethiopia.

Key questions addressed:

- What drives financial inclusion in Ethiopia?
- How do policies, product launches, and infrastructure investments affect inclusion outcomes?
- How did inclusion change by 2025, and what does the outlook for 2026–2027 look like?

***

## Repository Structure

The project follows the standard Week 10 challenge structure.

```text
ethiopia-fi-forecast/
├── .github/
│   └── workflows/
│       └── unittests.yml         # CI pipeline for tests
├── data/
│   ├── raw/
│   │   ├── ethiopiafiunifieddata.csv   # Starter unified dataset
│   │   └── referencecodes.csv          # Valid categorical codes
│   └── processed/
│       └── ...                         # Cleaned / enriched datasets
├── notebooks/
│   ├── task1_data_enrichment.ipynb     # Task 1: schema, EDA-lite, enrichment
│   ├── task2_eda.ipynb                 # Task 2: exploratory data analysis
│   ├── task3_impact_modeling.ipynb     # Task 3: event impact modeling
│   └── task4_forecasting.ipynb         # Task 4: forecasting Access & Usage
├── src/
│   ├── __init__.py
│   ├── data/
│   │   └── loaders.py                  # IO utilities for raw/processed data
│   ├── features/
│   │   └── engineering.py              # Feature construction & transformations
│   ├── models/
│   │   ├── impact_models.py            # Event–indicator impact logic
│   │   └── forecasting.py              # Forecast models & scenario logic
│   └── visualization/
│       └── plots.py                    # Reusable plotting utilities
├── dashboard/
│   ├── app.py                          # Streamlit dashboard entry point
│   └── config.py                       # Dashboard configuration & constants
├── tests/
│   ├── __init__.py
│   ├── test_data.py                    # Data loading & schema tests
│   ├── test_models.py                  # Impact / forecast model tests
│   └── test_dashboard.py               # Basic dashboard checks
├── reports/
│   ├── figures/                        # Generated plots for reports & README
│   └── final_report.md                 # Medium-style final report draft
├── README.md                           # Project overview & instructions
├── requirements.txt                    # Python dependencies
└── .gitignore
```

If your actual repository layout differs, keep the spirit of this structure (separation of raw/processed data, notebooks, src, tests, and dashboard) while adapting paths accordingly.

***

## Data

### 1. Unified Starter Dataset

- `data/raw/ethiopiafiunifieddata.csv` – unified schema combining observations, events, impact links, and targets.

Key fields:

- `recordtype` – one of:
  - `observation` (measured values from surveys, operator reports, infrastructure data)
  - `event` (policies, product launches, market entries, milestones)
  - `impactlink` (modeled relationships between events and indicators)
  - `target` (official policy goals)
- `pillar` – conceptual pillar where applicable (e.g., Access vs Usage).
- `indicator`, `indicatorcode` – human‑readable name and code.
- `valuenumeric` – numeric value for observations.
- `observationdate` or `eventdate` – temporal reference.
- `sourcename`, `sourceurl`, `sourcetype` – data provenance.
- `confidence` – qualitative confidence rating.

Design principle: events are categorized by type (policy, productlaunch, infrastructure, etc.) but are not pre‑assigned to pillars; their effects are encoded via separate `impactlink` records.

### 2. Reference Codes

- `data/raw/referencecodes.csv` – enumerations and valid values for all categorical fields (e.g., record types, indicator codes, pillars, event categories).

### 3. Enriched / Processed Data

Task 1 generates enriched datasets saved under `data/processed/`, for example:

- `ethiopiafiunifieddata_enriched.csv` – starter dataset plus new observations, events, impact links, and targets.
- `impact_matrix.csv` – event–indicator association matrix used in Task 3.

All additions must be documented in `data/dataenrichmentlog.md`, including `sourceurl`, `originaltext`, `confidence`, `collectedby`, `collectiondate`, and `notes`.

***

## Tasks and Expected Artifacts

### Task 1 – Data Exploration and Enrichment

Goal: understand the schema, explore coverage, and enrich the unified dataset.

Main steps:

- Load and explore `ethiopiafiunifieddata.csv` and `referencecodes.csv`.
- Summarize records by `recordtype`, `pillar`, `sourcetype`, and `confidence`.
- Identify temporal coverage and list all unique indicators and their coverage.
- Add:
  - New observations (e.g., disaggregations, infrastructure series).
  - New events (policies, launches, milestones).
  - New impactlinks (linking events to specific indicators via `parentid`).
- Follow the unified schema strictly when adding rows.
- Document all additions in `dataenrichmentlog.md`.

Branch & Git workflow minimums:

- Create branch `task-1`.
- Commit progress with descriptive messages.
- Merge into `main` via Pull Request.

Artifacts:

- Updated unified dataset under `data/processed/`.
- `data/dataenrichmentlog.md` describing all changes.

### Task 2 – Exploratory Data Analysis (EDA)

Goal: analyze patterns and drivers of financial inclusion.

Main analyses:

- Dataset overview by `recordtype`, `pillar`, `sourcetype`.
- Temporal coverage visualization by indicator.
- Data quality assessment (distribution of `confidence`, gaps).
- Access analysis:
  - Plot account ownership trajectory (2011–2024) and growth rates.
  - Analyze gender and urban–rural gaps where data exists.
  - Investigate slowdown from 2021–2024.
- Usage analysis:
  - Mobile money account penetration 2014–2024.
  - Digital payment adoption trends and, where possible, use cases.
- Infrastructure and enablers:
  - Explore 4G coverage, mobile penetration, ATM density, etc.
  - Identify potential leading indicators of Findex outcomes.
- Event timeline:
  - Visual timeline of events overlaid on key indicator trends (e.g., Telebirr 2021, M‑Pesa 2023).
- Correlation analysis:
  - Correlations between candidate drivers and Access/Usage.
  - Insights from existing impactlinks.

Deliverables:

- Branch `task-2`, merged via PR.
- `notebooks/task2_eda.ipynb` with visualizations.
- Summary of at least 5 key insights with supporting evidence.
- Data quality assessment.

### Task 3 – Event Impact Modeling

Goal: model how events affect financial inclusion indicators.

Main steps:

- Load impactlinks and join to events via `parentid`.
- Build an event–indicator matrix:
  - Rows: events.
  - Columns: key indicators (e.g., `ACCOWNERSHIP`, `ACCMMACCOUNT`, `USGDIGITALPAYMENT`).
  - Values: estimated effect (direction, magnitude, lag).
- Translate impactlinks into a time‑series model that accumulates event effects.
- Use comparable country evidence where local data is sparse.
- Validate against history (e.g., Telebirr 2021 → mobile money accounts 4.7 → 9.45).
- Refine impact estimates, documenting assumptions and confidence.

Deliverables:

- Branch `task-3`, merged via PR.
- Impact modeling notebook.
- Event–indicator association matrix (table or heatmap).
- Documentation of:
  - Methodology and functional forms.
  - Sources for impact estimates.
  - Validation results.
  - Key assumptions and uncertainties.

### Task 4 – Forecasting Access and Usage (2025–2027)

Goal: forecast Account Ownership (Access) and Digital Payment Usage for 2025–2027 under multiple scenarios.

Approach options:

- Trend regression (linear or log).
- Event‑augmented models (trend + event effects).
- Scenario analysis (optimistic, base, pessimistic).

Required outputs:

- Baseline trend forecast.
- Event‑adjusted forecasts incorporating expected developments.
- Scenario ranges with explicit uncertainty (confidence intervals or ranges).
- Interpretation of results, including:
  - Drivers of forecasted changes.
  - Events with largest potential impact.
  - Main uncertainties.

Deliverables:

- Branch `task-4`, merged via PR.
- Forecasting notebook.
- Forecast table with confidence intervals.
- Scenario visualization(s).
- Written interpretation (for use in the final report and dashboard).

### Task 5 – Dashboard Development

Goal: create an interactive dashboard (Streamlit recommended) for stakeholders.

Entry point: `dashboard/app.py`.

Sections:

- Overview:
  - Key metrics summary cards (current values, recent trends).
  - P2P‑to‑ATM crossover ratio.
  - Growth highlights.
- Trends:
  - Interactive time‑series plots with date range selector.
  - Channel comparison views.
- Forecasts:
  - Visual forecasts with confidence bands.
  - Model or scenario selector.
  - Key projected milestones.
- Inclusion Projections:
  - Progress toward policy targets (e.g., 60 percent account ownership).
  - Scenario selector (optimistic/base/pessimistic).
  - Answers to consortium’s core questions.

Technical minimums:

- At least 4 interactive visualizations.
- Clear labels and textual explanations.
- Data download functionality.
- Local run instructions in this README.

Deliverables:

- Working Streamlit app.
- Clear documentation for running locally and understanding dashboard pages.

***

## How to Run the Project

### 1. Setup Environment

```bash
# Clone repository
git https://github.com/GrimVad3r/Forecasting-Financial-Inclusion-in-Ethiopia.git
cd ethiopia-fi-forecast

# Create and activate virtual environment (example: venv)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Requirements include standard data science libraries (pandas, numpy, matplotlib, seaborn, statsmodels, scikit‑learn), plus Streamlit and Plotly (or equivalent) for the dashboard.

### 2. Run Unit Tests

```bash
pytest
```

GitHub Actions runs `unittests.yml` on every push/PR to ensure code quality.

### 3. Run Notebooks

Open notebooks in Jupyter or VS Code and run in order:

1. `task1_data_enrichment.ipynb`
2. `task2_eda.ipynb`
3. `task3_impact_modeling.ipynb`
4. `task4_forecasting.ipynb`

Make sure paths point to `data/raw/` and `data/processed/` appropriately.

### 4. Launch Dashboard

From the project root:

```bash
streamlit run dashboard/app.py
```

Then open the local URL printed in your terminal (usually `http://localhost:8501`).

***

## Git Workflow

The project uses a branch‑based workflow aligned with weekly tasks.

- `main` – stable branch, always passing tests.
- Feature branches:
  - `task-1`, `task-2`, `task-3`, `task-4`, `task-5`.

Workflow per task:

1. Create task branch from `main`.
2. Commit changes frequently with descriptive messages.
3. Open PR into `main`, request review if applicable.
4. Ensure all tests pass.
5. Merge via PR.

***

## Methodology (High Level)

- Unified schema for all records (observations, events, impactlinks, targets) to enable consistent modeling.
- Event impact modeling via association matrices and time‑distributed effects.
- Forecasting under data scarcity using trend, event‑augmented, and scenario‑based approaches.
- Explicit treatment of data quality, uncertainty, and assumptions throughout.

See `reports/final_report.md` for a full narrative on data sources, methods, results, and limitations.

***

## Data Quality, Assumptions, and Uncertainty

Guiding principles:

- Document all added data sources and transformations.
- Use wide, honest uncertainty ranges, given only a handful of Findex survey points.
- Make all modeling assumptions explicit, especially around event timing and lag structures.
- Highlight key data gaps and how they affect interpretation.

***

## References

Core frameworks and suggested sources include the Global Findex Database, IMF Financial Access Survey, GSMA, National Bank of Ethiopia, Ethio Telecom, EthSwitch, Fayda Digital ID, and high‑quality research on financial inclusion and mobile money.