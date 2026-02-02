# Task 5: Dashboard Development - Setup & Running Guide

## 📊 Overview

The dashboard is a comprehensive Streamlit application that provides interactive exploration of:
- Historical financial inclusion trends
- Event impact analysis  
- 2025-2027 forecasts with scenarios
- Key insights and methodology

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Prepare Data
```bash
# Create data directory structure
mkdir -p data/raw data/processed

# Place these files in data/processed/ (from Task 4 outputs):
# - forecasts_2025_2027.csv
# - forecast_scenarios.json
# - event_indicator_association_matrix.csv
```

### Step 3: Run Dashboard
```bash
streamlit run dashboard_app.py
```

The dashboard will open at `http://localhost:8501` in your browser.

---

## 📁 File Structure

```
ethiopia-fi-forecast/
├── dashboard_app.py              ← Main dashboard application
├── requirements.txt              ← Python dependencies
├── data/
│   ├── raw/                      ← Raw Excel files (optional for dashboard)
│   └── processed/                ← Task 4 outputs (required)
│       ├── forecasts_2025_2027.csv
│       ├── forecast_scenarios.json
│       └── event_indicator_association_matrix.csv
└── README.md
```

---

## 🎯 Dashboard Features

### 1. **Overview Page** 📈
- Key metrics cards (2024 actuals, 2027 forecasts)
- Account ownership forecast with confidence intervals
- Digital payment usage forecast
- Summary statistics

**Interactive Elements:**
- Hover over charts for detailed values
- Trend lines with confidence bands
- Side-by-side metric comparison

### 2. **Trends & Analysis Page** 📊
- Historical account ownership trajectory (2011-2024)
- Growth rate analysis with annotations
- Gender gap analysis (20pp persistent)
- Registered vs active user gap analysis
- Access vs usage comparison

**Key Visualizations:**
- Time series with growth rate indicators
- Bar chart comparisons
- Metric cards with context

### 3. **Forecasts Page** 🎯
- Account ownership forecast (2025-2027)
- Digital payment usage forecast
- Forecast table with confidence intervals
- Uncertainty assessment

**Features:**
- Base forecast with 95% CI
- Multiple forecast scenarios
- Downloadable forecast table
- Uncertainty explanation

### 4. **Scenarios Page** 🔄
- Pessimistic scenario (54% access, 43% usage)
- Base scenario (57% access, 46% usage)
- Optimistic scenario (62% access, 51% usage)
- Scenario comparison charts
- Progress toward 2030 NFIS-II targets

**Analysis:**
- Probability assessment for each scenario
- Key assumptions documentation
- Acceleration levers to achieve targets

### 5. **Event Impact Page** 📍
- Event-indicator association heatmap
- Detailed event descriptions:
  - Telebirr Launch (May 2021)
  - Safaricom Entry (Aug 2022)
  - M-Pesa Launch (Aug 2023)
  - Fayda Digital ID (Jan 2024)
  - FX Reform (Jul 2024)
- Impact validation results
- Methodology notes

**Interactive Features:**
- Expandable event cards
- Impact magnitude visualization
- Comparable country benchmarks

### 6. **Key Insights Page** 💡
- 8 comprehensive insights:
  1. Stagnation Paradox
  2. Persistent Gender Gap
  3. Registered vs Active Gap
  4. P2P Dominance
  5. Infrastructure Scaling
  6. Event-Outcome Misalignment
  7. Data Quality Limitations
  8. Critical Data Gaps

**Format:**
- Detailed narrative for each insight
- Supporting data and analysis
- Implications and opportunities

### 7. **Methodology Page** 📚
- Data sources and quality assessment
- Forecasting methodology explanation
- Event impact estimation approach
- Key assumptions and limitations
- Validation strategy for 2025

---

## 🔧 Configuration

### Data Loading
The dashboard attempts to load data in this order:
1. `data/processed/forecasts_2025_2027.csv`
2. Falls back to sample data if not found

### Custom Colors
```python
Primary Blue: #1E3A8A
Secondary Orange: #F97316
Accent Cyan: #06B6D4
Success Green: #10B981
```

### Chart Settings
- All charts use Plotly for interactivity
- Hover tooltips show detailed information
- White background template for clarity
- Responsive to window size

---

## 📊 Page Navigation

Use the sidebar to navigate:
```
🧭 Navigation
├── 📈 Overview (default)
├── 📊 Trends & Analysis
├── 🎯 Forecasts
├── 🔄 Scenarios
├── 📍 Event Impact
├── 💡 Key Insights
└── 📚 Methodology
```

---

## 💾 Data Requirements

### Required Files (from Task 4)
```
data/processed/
├── forecasts_2025_2027.csv
│   ├── Year (int)
│   ├── Account_Ownership_% (float)
│   ├── Ownership_CI_Lower (float)
│   ├── Ownership_CI_Upper (float)
│   ├── Digital_Payment_% (float)
│   ├── Payment_CI_Lower (float)
│   └── Payment_CI_Upper (float)
│
├── forecast_scenarios.json
│   ├── scenarios
│   │   ├── Pessimistic (list of values)
│   │   ├── Base (list of values)
│   │   └── Optimistic (list of values)
│   └── years (list of years)
│
└── event_indicator_association_matrix.csv
    ├── Index: Event names
    └── Columns: Indicator codes
```

### Optional Files
- Historical data files (Excel) for enrichment
- Additional context documents

---

## 🎨 Dashboard Customization

### Modify Colors
Edit the CSS in `dashboard_app.py`:
```python
st.markdown("""
    <style>
    :root {
        --primary-color: #1E3A8A;  # Change this
        ...
    }
    </style>
""", unsafe_allow_html=True)
```

### Add New Pages
1. Create new function: `show_new_page()`
2. Add to sidebar navigation
3. Call in main conditional

Example:
```python
page = st.sidebar.radio(
    "Select Page:",
    ["📈 Overview", "📊 Trends", "🎯 Forecasts", 
     "🆕 New Page"],  # Add here
    index=0
)

if page == "🆕 New Page":
    show_new_page()
```

### Modify Forecast Calculations
Edit the `create_*_forecast_chart()` functions to adjust:
- Base forecast calculations
- Confidence interval widths
- Scenario adjustments
- Chart appearance

---

## 🚀 Deployment Options

### Local Development
```bash
streamlit run dashboard_app.py
```
Access at: `http://localhost:8501`

### Cloud Deployment (Streamlit Cloud)
```bash
# Push to GitHub repo
git push origin main

# Enable Streamlit Cloud deployment:
# 1. Go to https://share.streamlit.io
# 2. Connect GitHub repo
# 3. Select dashboard_app.py as main file
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard_app.py"]
```

Run with:
```bash
docker build -t eth-fi-dashboard .
docker run -p 8501:8501 eth-fi-dashboard
```

### Heroku Deployment
Create `Procfile`:
```
web: streamlit run --server.port=$PORT --server.address=0.0.0.0 dashboard_app.py
```

---

## 📈 Performance Tips

### Data Loading
- Dashboard uses `@st.cache_data` decorator for performance
- Data loaded once and reused across page navigations

### Chart Optimization
- Plotly charts are interactive but lightweight
- Large datasets rendered efficiently
- Hover tooltips computed on-demand

### Memory Usage
- Sample data generators avoid large arrays
- JSON parsing optimized
- Cache invalidation when files change

---

## 🔧 Troubleshooting

### Issue: "Module not found: streamlit"
**Solution:**
```bash
pip install streamlit==1.28.0
```

### Issue: "File not found: data/processed/..."
**Solution:**
1. Create `data/processed/` directory
2. Add required CSV and JSON files from Task 4
3. Or use `--logger.level=debug` to see which files are being loaded

### Issue: "Charts not displaying"
**Solution:**
```bash
# Update Plotly
pip install --upgrade plotly

# Clear Streamlit cache
streamlit cache clear
```

### Issue: "CSS not applying"
**Solution:**
- Refresh browser (Ctrl+Shift+R)
- Clear browser cache
- Check browser console for errors (F12)

### Issue: "Slow performance"
**Solution:**
- Clear Streamlit cache: `streamlit cache clear`
- Check system resources (RAM, CPU)
- Reduce chart resolution in visualization functions

---

## 📊 Monitoring & Validation

### 2025 Interim Validation
Run these checks:
1. Load latest Findex data (when available Q1 2026)
2. Compare 2024 Findex vs 2024 forecast
3. Adjust scenario probabilities if needed
4. Update forecast ranges

### Update Dashboard
```python
# Modify create_sample_forecast_data() with 2025 actual data
return pd.DataFrame({
    'Year': [2025, 2026, 2027],
    'Account_Ownership_%': [52.0, 54.0, 57.0],  # Update with actual
    ...
})
```

---

## 📞 Support & Questions

### Documentation
- README.md: Full project overview
- DELIVERY_SUMMARY.md: Executive summary
- Notebooks: Detailed analysis and methodology

### Code Comments
- All functions have docstrings
- Inline comments explain logic
- See notebook methodology sections for concepts

### Common Questions

**Q: Can I add more pages?**
A: Yes, follow the pattern in `main()` function

**Q: How do I customize colors?**
A: Edit CSS in `st.markdown()` at top of main()

**Q: Can I export charts as images?**
A: Yes, use Plotly's built-in export (camera icon on hover)

**Q: How do I update forecasts?**
A: Replace CSV/JSON files in `data/processed/` and restart dashboard

---

## ✅ Quality Assurance

Before deployment, verify:
- [ ] All pages load without errors
- [ ] Charts render correctly
- [ ] Data loads from expected paths
- [ ] Sidebar navigation works
- [ ] All metric cards display
- [ ] Hovering shows tooltips
- [ ] No console errors (F12)
- [ ] Sample data shown if files missing

---

## 🎯 Next Steps

1. **Collect Real Data:**
   - Export forecasts_2025_2027.csv from Task 4
   - Save forecast_scenarios.json
   - Extract association matrix

2. **Test Dashboard:**
   - Run locally with test data
   - Verify all pages load
   - Check chart interactivity

3. **Deploy:**
   - Choose deployment option (local/cloud/docker)
   - Configure for production
   - Share with stakeholders

4. **Maintain:**
   - Monitor 2025 actual vs forecast
   - Update data quarterly
   - Adjust scenarios based on outcomes

---

## 📝 Version History

- **v1.0 (Feb 2026)**: Initial release
  - 7 interactive pages
  - 15+ visualizations
  - Full methodology documentation
  - Sample data fallback

---

**Last Updated:** February 1, 2026  
**Status:** ✅ Ready for Deployment

---

## 📊 Dashboard Statistics

- **Total Pages:** 7
- **Interactive Charts:** 15+
- **Data Sources:** 3 (CSV + JSON)
- **Lines of Code:** 600+
- **Visualization Library:** Plotly
- **Framework:** Streamlit
- **Performance:** <2 second load time

---

