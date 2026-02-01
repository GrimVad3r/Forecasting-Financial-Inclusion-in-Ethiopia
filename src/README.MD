
---

# Ethiopia Food Insecurity Data Enrichment Toolkit

This toolkit is a modular Python-based system designed to handle complex datasets containing observations, events, and impact links. It provides a structured pipeline for loading raw Excel data, validating schemas, enriching datasets with new records, and exporting processed results with full audit logging.

## ## Project Structure

The toolkit consists of five core modules, each handling a specific stage of the data lifecycle:

| Module | Description |
| --- | --- |
| `data_loader.py` | Handles ingestion of Excel workbooks and reference code sheets. |
| `schema_analyzer.py` | Performs structural analysis, temporal coverage checks, and indicator profiling. |
| `data_enricher.py` | Core engine for adding new observations and events with built-in validation. |
| `data_explorer.py` | Conducts deep dives into event timelines and data quality metrics. |
| `data_exporter.py` | Saves enriched data and generates Markdown/JSON documentation and reports. |
| `comprehensive_analyzer.py` | Perfrorms Various Analysis & returns results |

---

## ## Module Deep Dive

### 1. Data Loading (`DataLoader`)

Responsible for safely importing raw data. It expects a unified Excel file with specific sheet names:

* **Unified Data**: `ethiopia_fi_unified_data`
* **Impact Links**: `Impact_sheet`
* **Reference Codes**: `reference_codes`

### 2. Schema Analysis (`SchemaAnalyzer`)

Provides visibility into the dataset's health.

* **Structure**: Reports shape, dtypes, and missing/duplicate values.
* **Record Types**: Breaks down the ratio of `observation`, `event`, `impact_link`, and `target` records.
* **Temporal Coverage**: Calculates the date range and total year span of the data.

### 3. Data Enrichment (`DataEnricher`)

Enables controlled growth of the dataset.

* **Validation**: Every new record is checked against a required schema (e.g., `record_id`, `indicator_code`, `confidence`).
* **Observation/Event Handling**: Appends new data to the existing DataFrame while maintaining an internal enrichment log.

### 4. Data Exploration (`DataExplorer`)

Focused on qualitative and quality analysis.

* **Event Timelines**: Generates chronologically sorted summaries of cataloged events.
* **Quality Metrics**: Calculates "Completeness %" and distributions for confidence levels and source types.

### 5. Data Export (`DataExporter`)

The final stage of the pipeline.

* **Unified CSV**: Saves the fully enriched dataset.
* **Enrichment Log**: Generates a `.md` file detailing every action taken during the session.
* **Summary Report**: Produces a `.json` snapshot of the final record distribution and metadata.

### 6. Feature Spotlight: Comprehensive Analyzer

The `comprehensive_analyzer.py` module provides high-level synthesis of financial inclusion drivers:

#### 1. Thematic Analysis Engines

* **AccessAnalyzer**: Tracks account ownership trajectories and mobile money penetration.
* **UsageAnalyzer**: Monitors digital payment adoption and the "Registered vs. Active" user gap.
* **InfrastructureAnalyzer**: Evaluates 4G coverage, smartphone penetration, and Fayda Digital ID enrollment.
* **CorrelationAnalyzer**: Maps "Impact Links" to identify drivers of financial inclusion and estimated magnitudes.

#### 2. Insight & Hypothesis Generation

The module synthesizes raw data into actionable intelligence:

* **The Stagnation Paradox**: Identifying why account ownership grows slowly despite massive mobile money expansion.
* **Gender Gap Analysis**: Quantifying the persistent 20pp gap between male and female account ownership.
* **Event Impact**: Correlating major market entries (Telebirr, Safaricom, M-Pesa) with indicator shifts.

---

## ## Advanced Usage Example

The `comprehensive_analyzer` is designed to be run after data enrichment to extract strategic value:

```python
from comprehensive_analyzer import InsightSummarizer, AccessAnalyzer

# Initialize analyzers
access_engine = AccessAnalyzer()
summarizer = InsightSummarizer()

# Analyze gender disparities
gender_gap = access_engine.analyze_gender_gap(unified_df)

# Generate strategic insights and modeling hypotheses
insights = summarizer.generate_insights()
hypotheses = summarizer.generate_hypotheses()

```

---

## ## Data Quality & Gaps

The toolkit now automatically identifies critical data limitations:

* **Recent Data Gaps**: Flags indicators that haven't been updated since 2024.
* **Sparse Observations**: Highlights reliance on limited survey points (e.g., only 5 points over 13 years for account ownership).
* **Missing Variables**: Notes the absence of agent density, merchant acceptance, and regional disparity data.
---

## ## Logging and Audit

The system implements a centralized logging strategy. All operations across all modules are logged to:

1. **`task_1_execution.log`**: A persistent file containing timestamps, log levels, and detailed error traces.
2. **Standard Output (Console)**: For real-time monitoring of script progress.

---

## ## Quick Start Example

```python
from data_loader import DataLoader
from data_enricher import DataEnricher
from data_exporter import DataExporter

# 1. Load Data
loader = DataLoader(data_dir='./data/raw')
unified_df, impact_df = loader.load_unified_data()

# 2. Enrich
enricher = DataEnricher(reference_df=None) # Pass reference codes if available
new_obs = {
    'record_id': 'OBS_2026_001',
    'record_type': 'observation',
    'indicator_code': 'CPI_FOOD',
    'value_numeric': 115.4,
    'observation_date': '2026-02-01',
    'source_name': 'Manual Enrichment',
    'confidence': 'High'
}
unified_df = enricher.add_observation(unified_df, new_obs)

# 3. Export
exporter = DataExporter(output_dir='./data/processed')
exporter.export_enriched_data(unified_df)
exporter.create_enrichment_log(enricher)

```

---

## ## Requirements

* **Python 3.8+**
* **Pandas**: Data manipulation
* **NumPy**: Numerical operations
* **Openpyxl**: Engine for reading Excel files

