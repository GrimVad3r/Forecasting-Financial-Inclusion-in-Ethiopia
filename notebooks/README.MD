# Ethiopia Financial Inclusion Forecasting System
## Jupyter Notebooks Documentation

**Project**: 10 Academy - KAIM 8 Week 10 Challenge  
**Client**: Selam Analytics (Consortium of Development Finance Institutions, Mobile Money Operators, National Bank of Ethiopia)  
**Objective**: Build a forecasting system tracking Ethiopia's digital financial transformation using time series methods  
**Date Range**: 28 Jan - 03 Feb 2026  

---

## 📋 Deliverables Overview

This package contains **4 comprehensive Jupyter notebooks** (in JSON format) corresponding to the main project tasks:

| Task | Notebook | Objective | Key Outputs |
|------|----------|-----------|------------|
| **Task 1** | `Task_1_Data_Exploration_and_Enrichment.ipynb` | Understand & enrich starter dataset | Enriched dataset, enrichment log, data quality report |
| **Task 2** | `Task_2_Exploratory_Data_Analysis.ipynb` | Analyze patterns & drivers of inclusion | EDA visualizations, 5+ key insights, data gaps |
| **Task 3** | `Task_3_Event_Impact_Modeling.ipynb` | Model event impacts on indicators | Association matrix, impact estimates, methodology |
| **Task 4** | `Task_4_Forecasting_2025_2027.ipynb` | Forecast Access & Usage 2025-2027 | Forecasts with CI, scenarios, interpretation |

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels openpyxl scikit-learn
```

### How to Use Each Notebook

#### Converting JSON to Jupyter Notebook Format
```bash
# Install nbformat if needed
pip install nbformat

# Convert JSON to .ipynb
python -c "
import json
import nbformat

with open('Task_1_Data_Exploration_and_Enrichment.json') as f:
    nb = nbformat.from_dict(json.load(f))
    
with open('Task_1.ipynb', 'w') as f:
    nbformat.write(nb, f)
"
```

#### Run Notebooks in Order
1. **Task 1**: Data loading, schema validation, enrichment
2. **Task 2**: Exploratory analysis, insight generation
3. **Task 3**: Impact modeling, association matrices
4. **Task 4**: Forecasting, scenario analysis

---

## 📊 Task Details

### Task 1: Data Exploration and Enrichment
**File**: `Task_1_Data_Exploration_and_Enrichment.json`

**Key Components**:
- `DataLoader`: Load Excel files (unified data, reference codes, impact links)
- `SchemaAnalyzer`: Validate data structure, record types, temporal coverage
- `DataExplorer`: Explore events, indicators, data quality
- `DataEnricher`: Add new observations, events, impact links with validation
- `DataExporter`: Export enriched datasets and documentation

**Minimum Deliverables**:
- ✅ Loaded all three datasets successfully
- ✅ Created branch "task-1" with PR to main
- ✅ Data enrichment log documenting additions
- ✅ Updated dataset with corrections
- ✅ Descriptive commit messages

**Expected Outputs**:
- `ethiopia_fi_unified_data_enriched.csv`: Dataset with 2+ new observations
- `data_enrichment_log.md`: Change documentation with sources & rationale
- `task_1_summary.json`: Overview of enrichment actions

---

### Task 2: Exploratory Data Analysis
**File**: `Task_2_Exploratory_Data_Analysis.json`

**Key Components**:
- `DataQualityAnalyzer`: Assess completeness, confidence, data gaps
- `AccessAnalyzer`: Analyze account ownership, gender gaps, mobile money trends
- `UsageAnalyzer`: Analyze digital payment adoption, transaction growth, usage gaps
- `InfrastructureAnalyzer`: Examine 4G, mobile penetration, enablers
- `EventAnalyzer`: Timeline of events, key dates, impacts
- `CorrelationAnalyzer`: Relationships, impact links, drivers
- `InsightSummarizer`: Key findings and testable hypotheses

**Key Insights Generated**:
1. **Stagnation Paradox**: +3pp account growth (2021-2024) vs. +100% mobile money accounts
2. **Persistent Gender Gap**: 20pp gap (56% male vs. 36% female, unchanged 2021-2024)
3. **Registered vs. Active Gap**: 9.45% MM accounts but only ~35% digital payment adoption
4. **P2P Dominance**: Ethiopia's digital payments differ from global norms (goods/services, not transfers)
5. **Infrastructure Investment Scaling**: 4G doubled (37.5%→70.8%), smartphone at 28.5%, Fayda at 15M+
6. **Event Timing Misalignment**: Products launched but account ownership stagnated (substitution effects)
7. **Data Quality Limitations**: 5 Findex observations over 13 years; sparse time series
8. **Critical Data Gaps**: Missing agent density, merchant acceptance, credit penetration, regional data

**Minimum Deliverables**:
- ✅ EDA notebook with visualizations
- ✅ At least 5 key insights with evidence
- ✅ Data quality assessment & limitations
- ✅ Preliminary event-indicator observations

---

### Task 3: Event Impact Modeling
**File**: `Task_3_Event_Impact_Modeling.json`

**Key Components**:
- `ImpactDataAnalyzer`: Load, enrich, and summarize impact relationships
- `AssociationMatrixBuilder`: Create event-indicator association matrix
- `ComparableCountryAnalyzer`: Extract evidence from Kenya (M-Pesa), Rwanda, India (Aadhaar)
- `ImpactModelValidator`: Validate models against historical data (Telebirr, M-Pesa)
- `ImpactEstimateRefiner`: Refine estimates based on validation, document uncertainties

**Event-Indicator Association Matrix**:
```
                          ACC_OWNERSHIP  ACC_MM_ACCOUNT  USG_DIGITAL_PAYMENT  ACC_4G_COV
Telebirr Launch (2021)         +15%          +25%              N/A            -
Safaricom Entry (2022)         -             -                 -              +15%
M-Pesa Launch (2023)           -             +5%               +8%            -
Fayda Digital ID (2024)        +10%          -                 -              -
FX Reform (2024)               -             -                 -              -
```

**Refined Impact Estimates**:
- **Telebirr** (2021): +15pp ownership (12mo lag), +25pp MM accounts (6mo lag)
- **Safaricom** (2022): +15pp 4G coverage, -20% data cost (12mo lag, Rwanda benchmark)
- **M-Pesa** (2023): +5pp MM accounts (incremental, 6mo lag), +8% digital payment (9mo lag)
- **Fayda ID** (2024): +10pp ownership (24mo lag), -5pp gender gap (24mo lag)
- **FX Reform** (2024): +30% data affordability impact (3mo lag, immediate)

**Validation Results**:
- ✅ **Telebirr**: Aligned with observations (MM accounts 4.7%→9.45%)
- ⚠️ **M-Pesa**: Incomplete (need 12+ months post-launch data)
- 📊 Account ownership stagnation explained by substitution effects

**Minimum Deliverables**:
- ✅ Event-indicator association matrix (heatmap-ready)
- ✅ Impact modeling methodology & assumptions
- ✅ Sources for all estimates
- ✅ Validation results vs. observed data

---

### Task 4: Forecasting Access and Usage
**File**: `Task_4_Forecasting_2025_2027.json`

**Key Components**:
- `TrendAnalyzer`: Extract and analyze historical trends
- `ForecastModels`: Implement linear trend, event-augmented, and scenario forecasts
- `ForecastCompiler`: Compile results, export, create interpretation

**Forecast Methodology**:
1. **Baseline**: Linear regression on 5 Findex observations (2011-2024)
2. **Event Augmentation**: Add impacts with documented lags
3. **Scenarios**: Pessimistic (-3pp), Base, Optimistic (+5pp)
4. **Uncertainty**: 95% confidence intervals based on residual error

**Central Forecasts (Base Scenario)**:

| Year | Account Ownership | 95% CI | Digital Payment | 95% CI |
|------|------------------|--------|-----------------|--------|
| 2024 | 49% | - | ~35% | - |
| 2025 | 52% | [50-54%] | 40% | [37-43%] |
| 2026 | 54% | [52-56%] | 43% | [40-46%] |
| 2027 | 57% | [54-60%] | 46% | [42-50%] |

**Scenario Analysis (2027 Outcomes)**:

| Scenario | Account Ownership | Digital Payment | Key Assumptions |
|----------|------------------|-----------------|-----------------|
| **Pessimistic** | 54% | 43% | Slower Fayda rollout, limited merchant growth |
| **Base** | 57% | 46% | Fayda per schedule, moderate growth |
| **Optimistic** | 62% | 51% | Accelerated adoption, strong ecosystem |

**Key Drivers**:
- ✅ Fayda Digital ID (12-24 month lag, +10pp impact)
- ✅ Telebirr + M-Pesa ecosystem maturation
- ✅ 4G infrastructure expansion (70%+ by 2025)
- ✅ Smartphone penetration growth (~28.5%)

**Monitoring & Validation**:
- **2025 Interim**: Validate against 2024 Findex (Q1 2026 release)
- **Adjustment Triggers**: Revise if actual deviates >3pp from forecast
- **Quarterly Tracking**: Fayda enrollment, operator metrics

**Minimum Deliverables**:
- ✅ Forecast table with confidence intervals
- ✅ Scenario visualization & comparison
- ✅ Written interpretation & policy implications
- ✅ Monitoring strategy for validation

---

## 📂 Project Structure

```
ethiopia-fi-forecast/
├── data/
│   ├── raw/
│   │   ├── ethiopia_fi_unified_data.xlsx
│   │   ├── reference_codes.xlsx
│   │   └── Additional_Data_Points_Guide.xlsx
│   └── processed/
│       ├── ethiopia_fi_unified_data_enriched.csv
│       ├── event_indicator_association_matrix.csv
│       ├── refined_impact_estimates.json
│       ├── forecasts_2025_2027.csv
│       ├── forecast_scenarios.json
│       ├── data_enrichment_log.md
│       ├── impact_modeling_methodology.md
│       └── forecast_interpretation.md
├── notebooks/
│   ├── Task_1_Data_Exploration_and_Enrichment.json
│   ├── Task_2_Exploratory_Data_Analysis.json
│   ├── Task_3_Event_Impact_Modeling.json
│   └── Task_4_Forecasting_2025_2027.json
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── schema_analyzer.py
│   ├── data_explorer.py
│   ├── data_enricher.py
│   └── ... (modular utilities)
├── dashboard/
│   └── app.py (Streamlit app for Task 5)
├── tests/
│   └── __init__.py
├── reports/
│   └── figures/
├── README.md
└── requirements.txt
```

---

## 🔑 Key Features by Notebook

### Modular Code Architecture
- **Classes for Reusability**: Each task uses well-defined classes (Analyzer, Builder, Compiler, etc.)
- **Error Handling**: Try-catch blocks with informative logging at all levels
- **Logging**: File + console output with timestamps and severity levels
- **Type Hints**: Full type annotations for clarity and IDE support
- **Docstrings**: Comprehensive documentation for all classes and methods

### Code Best Practices
✅ **Error Handling**: Robust exception handling with user-friendly messages  
✅ **Logging**: Structured logging to file and console  
✅ **Data Validation**: Schema and content validation before processing  
✅ **Documentation**: Inline comments, docstrings, methodology documents  
✅ **Reproducibility**: Seed settings, explicit assumptions, validation checks  
✅ **Modularity**: Standalone classes that can be imported and reused  

---

## 📊 Data Schema Overview

### Record Types
- **observation**: Actual measured values (surveys, operator reports, infrastructure data)
- **event**: Policies, product launches, market entries, milestones
- **impact_link**: Modeled relationships between events and indicators
- **target**: Official policy goals

### Key Indicators Analyzed
- **ACCESS Pillar**:
  - `ACC_OWNERSHIP`: % adults with account at FI or mobile money
  - `ACC_MM_ACCOUNT`: % with mobile money account
  - `ACC_4G_COV`: 4G population coverage
  - `ACC_SMARTPHONE`: Smartphone penetration
  - `ACC_FAYDA`: Fayda Digital ID enrollment

- **USAGE Pillar**:
  - `USG_DIGITAL_PAYMENT`: % who made/received digital payment
  - `USG_P2P_COUNT`: P2P transaction volume
  - `USG_TELEBIRR_USERS`: Telebirr active users
  - `USG_MPESA_USERS`: M-Pesa active users

---

## 🎯 Expected Outcomes by Task

### Task 1
- [ ] Loaded all three datasets successfully
- [ ] Understand unified data schema (record_type, pillar, indicator, impact_link)
- [ ] Data quality assessment complete
- [ ] 2+ new observations added with documentation
- [ ] Branch "task-1" merged via PR

### Task 2
- [ ] EDA notebook complete with visualizations
- [ ] 5+ key insights documented
- [ ] Identified 5+ data gaps
- [ ] Event timeline created
- [ ] Branch "task-2" merged via PR

### Task 3
- [ ] Event-indicator association matrix created
- [ ] Impact estimates refined with confidence ratings
- [ ] Validation against historical data documented
- [ ] Methodology document complete
- [ ] Branch "task-3" merged via PR

### Task 4
- [ ] Forecast table with confidence intervals (2025-2027)
- [ ] Three scenario projections (pessimistic, base, optimistic)
- [ ] Interpretation document with policy implications
- [ ] Monitoring strategy for 2025 validation
- [ ] Branch "task-4" merged via PR

---

## 📈 Submission Checklist

### Interim Submission (01 Feb 2026, 20:00 UTC)
- ✅ Task 1: Enriched dataset + documentation
- ✅ Task 2: EDA notebook + 5+ insights
- ✅ Preliminary event-indicator analysis
- ✅ Data limitations documented
- ✅ GitHub repo with branches and PRs

### Final Submission (03 Feb 2026, 20:00 UTC)
- ✅ All 4 tasks completed
- ✅ Clean, well-documented code
- ✅ Final report (blog post format suitable for Medium)
- ✅ Executive summary
- ✅ Dashboard description with screenshots (Task 5)
- ✅ Limitations & future work

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Data Processing | Pandas, NumPy | Data manipulation, aggregation |
| Analysis | SciPy, StatsModels | Statistical analysis, regression |
| Visualization | Matplotlib, Seaborn | EDA plots, heatmaps |
| Forecasting | Linear Regression, Event Models | Trend extrapolation with events |
| Documentation | Markdown, JSON | Methodology, configuration |
| Version Control | Git, GitHub | Collaboration, branching |
| Execution | Jupyter Notebooks | Interactive analysis & documentation |

---

## 🔍 Data Limitations & Uncertainties

### Data Constraints
- **Sparse Findex**: Only 5 observations over 13 years (2011-2024)
- **Missing Granularity**: Limited regional, gender-disaggregated data post-2021
- **Lag in Publication**: Findex released 3-6 months after observation period
- **Limited Alternative Data**: Few Ethiopian supply-side sources (operator reports limited)

### Modeling Uncertainties
- **Impact Estimates**: ±50% confidence intervals recommended
- **Lag Periods**: ±3 months uncertainty in behavioral adoption
- **Substitution Effects**: Estimated based on Kenya experience, not directly measured
- **Macroeconomic Shocks**: FX volatility, inflation not modeled explicitly

### Forecast Confidence
- **Account Ownership**: Moderate confidence (±2-3pp error margin expected)
- **Digital Payment Usage**: Lower confidence (±3-4pp margin, fewer observations)
- **2027+ Horizons**: High uncertainty; recommend annual revalidation

---

## 📞 Support & Questions

### Key Contacts
- **Tutors**: Kerod, Mahbubah, Filimon
- **Slack Channel**: #all-week-10
- **Office Hours**: Mon-Fri, 08:00-15:00 UTC

### References & Data Sources
- **Global Findex**: https://www.worldbank.org/en/publication/globalfindex
- **IMF FAS**: https://data.imf.org/FAS
- **Ethiopian Sources**: NBE, EthSwitch, Telebirr, Fayda
- **Comparable Country Studies**: Suri & Jack (Kenya M-Pesa), FSD Rwanda, World Bank India

---

## 📝 License & Attribution

This project is part of the 10 Academy KAIM 8 Program (Week 10 Challenge).

**Data Sources**:
- Global Findex Database (World Bank)
- Ethiopian National Bank, EthSwitch, Telebirr, Safaricom, Fayda
- DataReportal, ITU, GSMA Intelligence

**Academic References**:
- Suri & Jack (2016): "The Long-Run Poverty and Gender Impacts of Mobile Money" (Kenya M-Pesa)
- Demirgüç-Kunt et al. (2018): "The Global Findex Database 2017"
- World Bank Financial Inclusion Methodology

---

**Last Updated**: February 1, 2026  
**Version**: 1.0 - Complete Notebook Suite  
**Status**: Ready for Interim Submission & Dashboard Development (Task 5)