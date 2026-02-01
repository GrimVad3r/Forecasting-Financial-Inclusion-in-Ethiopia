import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Setup visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('task_2_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DataQualityAnalyzer:
    """Analyze and report on data quality."""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def assess_completeness(self, df: pd.DataFrame) -> Dict:
        """Assess data completeness."""
        self.logger.info("\nAssessing data completeness")
        
        completeness = {
            'total_records': len(df),
            'total_cells': df.shape[0] * df.shape[1],
            'missing_cells': df.isnull().sum().sum(),
            'completeness_pct': round((1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2)
        }
        
        self.logger.info(f"Total cells: {completeness['total_cells']}")
        self.logger.info(f"Missing cells: {completeness['missing_cells']}")
        self.logger.info(f"Completeness: {completeness['completeness_pct']}%")
        
        return completeness
    
    def assess_confidence(self, df: pd.DataFrame) -> pd.Series:
        """Assess confidence distribution."""
        self.logger.info("\nAssessing confidence levels")
        
        confidence_dist = df['confidence'].value_counts()
        self.logger.info(f"\nConfidence Distribution:\n{confidence_dist}")
        
        return confidence_dist
    
    def identify_gaps(self, df: pd.DataFrame) -> Dict:
        """Identify data gaps."""
        self.logger.info("\nIdentifying data gaps")
        
        observations = df[df['record_type'] == 'observation'].copy()
        
        gaps = {
            'indicators_missing_recent_data': [],
            'years_with_sparse_data': []
        }
        
        # Find indicators without recent data (2024+)
        latest_year = observations['observation_date'].dt.year.max()
        for indicator in observations['indicator_code'].unique():
            indicator_data = observations[observations['indicator_code'] == indicator]
            latest = indicator_data['observation_date'].max().year
            if latest < 2024:
                gaps['indicators_missing_recent_data'].append({
                    'indicator': indicator,
                    'latest_year': latest,
                    'years_behind': latest_year - latest
                })
        
        self.logger.info(f"\nIndicators with missing recent data: {len(gaps['indicators_missing_recent_data'])}")
        for gap in gaps['indicators_missing_recent_data']:
            self.logger.info(f"  - {gap['indicator']}: Latest={gap['latest_year']}, Behind by {gap['years_behind']} years")
        
        return gaps
    
class AccessAnalyzer:
    """Analyze Access (Account Ownership) indicators."""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def analyze_account_ownership(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze account ownership trajectory."""
        self.logger.info("\n" + "="*60)
        self.logger.info("ACCOUNT OWNERSHIP ANALYSIS")
        self.logger.info("="*60)
        
        observations = df[df['record_type'] == 'observation'].copy()
        ownership = observations[observations['indicator_code'] == 'ACC_OWNERSHIP'].copy()
        ownership = ownership.sort_values('observation_date')
        
        self.logger.info(f"\nAccount Ownership Trajectory (2011-2024):")
        self.logger.info(ownership[['observation_date', 'value_numeric', 'gender']].to_string())
        
        # Calculate growth rates
        ownership_all = ownership[ownership['gender'] == 'all'].copy()
        if len(ownership_all) > 1:
            ownership_all['growth_pp'] = ownership_all['value_numeric'].diff()
            ownership_all['growth_pct'] = ownership_all['value_numeric'].pct_change() * 100
            
            self.logger.info(f"\nGrowth Rates:")
            self.logger.info(ownership_all[['observation_date', 'value_numeric', 'growth_pp', 'growth_pct']].to_string())
        
        return ownership
    
    def analyze_gender_gap(self, df: pd.DataFrame) -> Dict:
        """Analyze gender disparities in account ownership."""
        self.logger.info("\n" + "-"*60)
        self.logger.info("GENDER GAP ANALYSIS")
        self.logger.info("-"*60)
        
        observations = df[df['record_type'] == 'observation'].copy()
        ownership = observations[observations['indicator_code'] == 'ACC_OWNERSHIP'].copy()
        
        gender_analysis = {
            'by_year': {}
        }
        
        for year in sorted(ownership['observation_date'].dt.year.unique()):
            year_data = ownership[ownership['observation_date'].dt.year == year]
            male_val = year_data[year_data['gender'] == 'male']['value_numeric'].values
            female_val = year_data[year_data['gender'] == 'female']['value_numeric'].values
            all_val = year_data[year_data['gender'] == 'all']['value_numeric'].values
            
            if len(male_val) > 0 and len(female_val) > 0:
                gap = float(male_val[0]) - float(female_val[0])
                gender_analysis['by_year'][year] = {
                    'male': float(male_val[0]),
                    'female': float(female_val[0]),
                    'gap': gap
                }
                self.logger.info(f"{year}: Male={male_val[0]:.1f}%, Female={female_val[0]:.1f}%, Gap={gap:.1f}pp")
        
        return gender_analysis
    
    def analyze_mobile_money(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze mobile money account penetration."""
        self.logger.info("\n" + "-"*60)
        self.logger.info("MOBILE MONEY ACCOUNT ANALYSIS")
        self.logger.info("-"*60)
        
        observations = df[df['record_type'] == 'observation'].copy()
        mm_accounts = observations[observations['indicator_code'] == 'ACC_MM_ACCOUNT'].copy()
        mm_accounts = mm_accounts.sort_values('observation_date')
        
        self.logger.info(f"\nMobile Money Account Rate (2021-2024):")
        self.logger.info(mm_accounts[['observation_date', 'value_numeric']].to_string())
        
        # Calculate growth
        if len(mm_accounts) > 1:
            growth = mm_accounts['value_numeric'].iloc[-1] - mm_accounts['value_numeric'].iloc[0]
            growth_pct = (growth / mm_accounts['value_numeric'].iloc[0]) * 100
            self.logger.info(f"\nGrowth (2021-2024): {growth:.2f}pp ({growth_pct:.1f}%)")
        
        return mm_accounts

class UsageAnalyzer:
    """Analyze Usage (Digital Payments) indicators."""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def analyze_payment_adoption(self, df: pd.DataFrame) -> Dict:
        """Analyze digital payment adoption patterns."""
        self.logger.info("\n" + "="*60)
        self.logger.info("DIGITAL PAYMENT ADOPTION ANALYSIS")
        self.logger.info("="*60)
        
        observations = df[df['record_type'] == 'observation'].copy()
        
        payment_indicators = {
            'Digital Payment Rate': 'USG_DIGITAL_PAYMENT',
            'P2P Transaction Count': 'USG_P2P_COUNT',
            'Telebirr Users': 'USG_TELEBIRR_USERS',
            'M-Pesa Users': 'USG_MPESA_USERS'
        }
        
        analysis = {}
        for name, code in payment_indicators.items():
            data = observations[observations['indicator_code'] == code].copy()
            if len(data) > 0:
                data = data.sort_values('observation_date')
                analysis[name] = {
                    'latest_value': data['value_numeric'].iloc[-1],
                    'latest_date': data['observation_date'].iloc[-1],
                    'count': len(data)
                }
                self.logger.info(f"{name}: {data['value_numeric'].iloc[-1]:.2f} (as of {data['observation_date'].iloc[-1].date()})")
        
        return analysis
    
    def analyze_transaction_growth(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze P2P transaction growth."""
        self.logger.info("\n" + "-"*60)
        self.logger.info("P2P TRANSACTION ANALYSIS")
        self.logger.info("-"*60)
        
        observations = df[df['record_type'] == 'observation'].copy()
        p2p = observations[observations['indicator_code'] == 'USG_P2P_COUNT'].copy()
        p2p = p2p.sort_values('observation_date')
        
        if len(p2p) > 0:
            self.logger.info(f"\nP2P Transaction Volume:")
            self.logger.info(p2p[['observation_date', 'value_numeric']].to_string())
        
        return p2p
    
    def calculate_usage_gap(self, df: pd.DataFrame) -> Dict:
        """Calculate gap between registered and active users."""
        self.logger.info("\n" + "-"*60)
        self.logger.info("REGISTERED vs ACTIVE USAGE GAP")
        self.logger.info("-"*60)
        
        observations = df[df['record_type'] == 'observation'].copy()
        
        # Get latest mobile money accounts
        mm_accounts = observations[observations['indicator_code'] == 'ACC_MM_ACCOUNT']['value_numeric'].iloc[-1] if len(observations[observations['indicator_code'] == 'ACC_MM_ACCOUNT']) > 0 else None
        
        # Get latest digital payment rate
        digital_payment = observations[observations['indicator_code'] == 'USG_DIGITAL_PAYMENT']['value_numeric'].iloc[-1] if len(observations[observations['indicator_code'] == 'USG_DIGITAL_PAYMENT']) > 0 else None
        
        gap_analysis = {
            'mm_accounts_pct': mm_accounts,
            'digital_payment_pct': digital_payment,
            'gap_pp': None
        }
        
        if mm_accounts and digital_payment:
            gap_analysis['gap_pp'] = mm_accounts - digital_payment
            self.logger.info(f"Mobile Money Accounts: {mm_accounts}%")
            self.logger.info(f"Digital Payment Users: {digital_payment}%")
            self.logger.info(f"Gap (Registered but not actively using): {gap_analysis['gap_pp']:.2f}pp")
        
        return gap_analysis
class InfrastructureAnalyzer:
    """Analyze infrastructure and enabling factors."""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def analyze_infrastructure(self, df: pd.DataFrame) -> Dict:
        """Analyze infrastructure indicators."""
        self.logger.info("\n" + "="*60)
        self.logger.info("INFRASTRUCTURE AND ENABLERS ANALYSIS")
        self.logger.info("="*60)
        
        observations = df[df['record_type'] == 'observation'].copy()
        
        infrastructure_indicators = {
            '4G Coverage': 'ACC_4G_COV',
            'Mobile Penetration': 'ACC_MOBILE_PEN',
            'Smartphone Penetration': 'ACC_SMARTPHONE',
            'Fayda Digital ID': 'ACC_FAYDA'
        }
        
        infrastructure_data = {}
        for name, code in infrastructure_indicators.items():
            data = observations[observations['indicator_code'] == code].copy()
            if len(data) > 0:
                data = data.sort_values('observation_date')
                latest = data.iloc[-1]
                infrastructure_data[name] = {
                    'latest_value': latest['value_numeric'],
                    'latest_date': latest['observation_date'],
                    'unit': latest['unit']
                }
                self.logger.info(f"{name}: {latest['value_numeric']:.2f} {latest['unit']} (as of {latest['observation_date'].date()})")
        
        return infrastructure_data
    
    def identify_leading_indicators(self, df: pd.DataFrame) -> List[str]:
        """Identify potential leading indicators."""
        self.logger.info("\n" + "-"*60)
        self.logger.info("POTENTIAL LEADING INDICATORS")
        self.logger.info("-"*60)
        
        leading_indicators = [
            'Smartphone Penetration (ACC_SMARTPHONE)',
            '4G Population Coverage (ACC_4G_COV)',
            'Fayda Digital ID Enrollment (ACC_FAYDA)',
            'Mobile Internet Penetration (implied by mobile + data)',
            'Agent Network Density (from bank sources)',
            'Data Affordability (ITU data)',
            'Urbanization Rate'
        ]
        
        for indicator in leading_indicators:
            self.logger.info(f"  • {indicator}")
        
        return leading_indicators

class EventAnalyzer:
    """Analyze events and their potential impacts."""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def analyze_events_timeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze event timeline and characteristics."""
        self.logger.info("\n" + "="*60)
        self.logger.info("EVENT TIMELINE ANALYSIS")
        self.logger.info("="*60)
        
        events = df[df['record_type'] == 'event'].copy()
        events['observation_date'] = pd.to_datetime(events['observation_date'], errors='coerce')
        events = events.sort_values('observation_date')
        
        event_summary = events[['record_id', 'category', 'indicator', 'observation_date']].copy()
        event_summary['year'] = event_summary['observation_date'].dt.year
        
        self.logger.info(f"\nTotal Events Cataloged: {len(events)}")
        self.logger.info(f"\nEvent Distribution by Category:")
        self.logger.info(events['category'].value_counts())
        
        self.logger.info(f"\nEvent Timeline (2021-2025):")
        for _, event in events.iterrows():
            self.logger.info(f"  {event['observation_date'].date()}: {event['category']} - {event['indicator']}")
        
        return event_summary
    
    def identify_key_events(self, df: pd.DataFrame) -> Dict:
        """Identify key events and their timing relative to indicator changes."""
        self.logger.info("\n" + "-"*60)
        self.logger.info("KEY EVENTS AND THEIR IMPACTS")
        self.logger.info("-"*60)
        
        events = df[df['record_type'] == 'event'].copy()
        observations = df[df['record_type'] == 'observation'].copy()
        
        key_events = {
            'Telebirr Launch': '2021-05',
            'Safaricom Market Entry': '2022-08',
            'M-Pesa Launch': '2023-08',
            'Fayda Digital ID Expansion': '2024-01',
            'FX Reform': '2024-07'
        }
        
        self.logger.info("\nKey Events Identified:")
        for event_name, date in key_events.items():
            self.logger.info(f"  • {event_name}: {date}")
        
        return key_events

class CorrelationAnalyzer:
    """Analyze correlations between indicators."""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def analyze_impact_links(self, impact_df: pd.DataFrame) -> pd.DataFrame:
        """Analyze relationships captured in impact links."""
        self.logger.info("\n" + "="*60)
        self.logger.info("IMPACT LINK RELATIONSHIPS")
        self.logger.info("="*60)
        
        # 1. Create a copy to avoid SettingWithCopyWarning
        df = impact_df.copy()

        # 2. Define the mapping based on your requirements
        # We assign numbers so nlargest can identify "High" as the top value
        impact_map = {
            'high': 20.0,   # Representative value > 15%
            'medium': 10.0, # Representative value between 5-15%
            'low': 3.0      # Representative value < 5%
        }
        
        # 3. Convert the string column to numeric
        # if the column is already numeric, this won't break it
        if df['impact_magnitude'].dtype == 'string' or df['impact_magnitude'].dtype == 'object':
            df['impact_magnitude_numeric'] = df['impact_magnitude'].map(impact_map)
        else:
            df['impact_magnitude_numeric'] = df['impact_magnitude']

        # 4. Clean and Sort
        impact_summary = df.dropna(subset=['impact_magnitude_numeric'])
        
        self.logger.info(f"\nTotal Impact Relationships: {len(impact_summary)}")
        self.logger.info(f"\nImpact Direction Distribution:\n{df['impact_direction'].value_counts()}")
        
        self.logger.info(f"\nTop Impact Magnitudes (Mapped):")
        # Use the new numeric column for nlargest
        top_impacts = impact_summary.nlargest(5, 'impact_magnitude_numeric')[
            ['parent_id', 'indicator_code', 'impact_magnitude', 'lag_months']
        ]
        self.logger.info(top_impacts.to_string())
        
        return impact_summary
    
    def identify_access_drivers(self, df: pd.DataFrame, impact_df: pd.DataFrame) -> List[str]:
        """Identify factors most strongly associated with Access."""
        self.logger.info("\n" + "-"*60)
        self.logger.info("ACCESS DRIVERS")
        self.logger.info("-"*60)
        
        access_related = impact_df[impact_df['indicator_code'] == 'ACC_OWNERSHIP'].copy()
        
        drivers = []
        self.logger.info("\nFactors affecting Account Ownership:")
        for _, link in access_related.iterrows():
            if pd.notna(link['parent_id']):
                drivers.append(link['parent_id'])
                self.logger.info(f"  • {link['parent_id']}: {link['impact_direction']} ({link['impact_magnitude']}% estimated)")
        
        return drivers
    
    def identify_usage_drivers(self, df: pd.DataFrame, impact_df: pd.DataFrame) -> List[str]:
        """Identify factors most strongly associated with Usage."""
        self.logger.info("\n" + "-"*60)
        self.logger.info("USAGE DRIVERS")
        self.logger.info("-"*60)
        
        # Filter for usage-related indicators
        usage_codes = ['USG_DIGITAL_PAYMENT', 'USG_P2P_COUNT', 'USG_TELEBIRR_USERS', 'USG_MPESA_USERS']
        usage_related = impact_df[impact_df['indicator_code'].isin(usage_codes)].copy()
        
        drivers = []
        self.logger.info("\nFactors affecting Digital Payment Usage:")
        for _, link in usage_related.head(10).iterrows():
            if pd.notna(link['parent_id']):
                drivers.append(link['parent_id'])
                self.logger.info(f"  • {link['parent_id']}: {link['impact_direction']} on {link['indicator_code']}")
        
        return drivers
    
class InsightSummarizer:
    """Synthesize key insights from EDA."""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.insights = []
    
    def generate_insights(self) -> List[str]:
        """Generate key insights."""
        self.logger.info("\n" + "="*80)
        self.logger.info("KEY INSIGHTS FROM EDA")
        self.logger.info("="*80)
        
        insights = [
            "1. STAGNATION PARADOX: Account ownership grew only +3pp (46% to 49%) from 2021-2024, despite mobile money accounts more than doubling from 4.7% to 9.45%. This suggests existing bank accounts dominate the ownership metric and mobile money is not significantly increasing 'any account' ownership.",
            
            "2. PERSISTENT GENDER GAP: A 20pp gender gap exists (56% male vs 36% female ownership in 2021), unchanged or widened despite policy attention. Gender-specific barriers (ID access, phone ownership, cultural factors) persist despite infrastructure improvements.",
            
            "3. REGISTERED vs ACTIVE GAP: Mobile money accounts (9.45%) exceed digital payment adoption (~35% for broader payments), suggesting many registered accounts are inactive. High registration but low engagement indicates onboarding without sustained use.",
            
            "4. P2P DOMINANCE IN ETHIOPIA: Unlike global norms, digital payments in Ethiopia are heavily P2P-driven (for goods/services, not just transfers). This market nuance requires adapted baselines and program design assumptions.",
            
            "5. INFRASTRUCTURE INVESTMENT SCALING: 4G coverage doubled (37.5% to 70.8% in 2025), smartphone penetration rising (~28.5% in 2025), and Fayda digital ID enrollment (15M+) creating enabling conditions. However, asset availability hasn't yet translated to usage.",
            
            "6. EVENT TIMING vs OUTCOMES: Despite Telebirr (May 2021), Safaricom (Aug 2022), and M-Pesa (Aug 2023) entries, account ownership stagnated. Suggests events may have substitution effects (shifting users between providers) rather than driving net new inclusion.",
            
            "7. DATA QUALITY LIMITATIONS: Account ownership data relies on 5 survey points over 13 years. Sparse observations limit granular trend analysis. P2P and transaction data are more recent (2023+) but have limited history for forecasting.",
            
            "8. CRITICAL DATA GAPS: Missing data on agent density, merchant acceptance, remittance flows, credit penetration, and regional disparities. These gaps limit ability to model local inclusion drivers and identify underserved areas."
        ]
        
        for insight in insights:
            self.logger.info(f"\n{insight}")
            self.insights.append(insight)
        
        return insights
    
    def generate_hypotheses(self) -> List[str]:
        """Generate testable hypotheses for impact modeling phase."""
        self.logger.info("\n" + "="*80)
        self.logger.info("HYPOTHESES FOR IMPACT MODELING")
        self.logger.info("="*80)
        
        hypotheses = [
            "H1: Infrastructure expansion (4G, smartphone) is a necessary but not sufficient condition. Usage adoption requires complementary factors (agent density, merchant acceptance, education).",
            
            "H2: Digital ID (Fayda) enrollment will have delayed but significant impact on account ownership (2024 launch, expected 12-24 month lag for behavioral adoption).",
            
            "H3: Mobile money competition (Telebirr + M-Pesa) drove user substitution rather than net new inclusion, explaining stagnation in 'any account' ownership despite account volume growth.",
            
            "H4: Gender gap is driven by structural barriers (ID access, phone ownership, financial literacy) that will not resolve through infrastructure investment alone. Requires targeted interventions.",
            
            "H5: Regional variation (urban/rural) is larger than national aggregates suggest. Urban centers likely at 60%+ adoption while rural areas lag significantly, masking divergent dynamics.",
            
            "H6: Usage adoption (digital payments) will accelerate post-2025 as smartphone/4G/ID base reaches critical mass. Current 35% digital payment rate has ceiling for growth."
        ]
        
        for i, hyp in enumerate(hypotheses, 1):
            self.logger.info(f"\n{hyp}")
        
        return hypotheses
