
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

