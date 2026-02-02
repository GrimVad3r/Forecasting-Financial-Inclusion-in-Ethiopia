import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging
from pathlib import Path
from typing import Dict, List

# Setup Logging
logger = logging.getLogger(__name__)

class DataVisualizer:
    """Generate standardized visualizations for financial inclusion trends."""
    
    def __init__(self, output_dir: str = './reports/figures'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Global Seaborn Settings
        sns.set_theme(style="whitegrid", palette="muted")
        plt.rcParams['figure.figsize'] = (12, 7)
        plt.rcParams['axes.titlesize'] = 16
        plt.rcParams['axes.labelsize'] = 12

    def plot_ownership_trajectory(self, ownership_df: pd.DataFrame):
        """Plot Account Ownership trends over time."""
        plt.figure()
        plot = sns.lineplot(
            data=ownership_df, 
            x='observation_date', 
            y='value_numeric', 
            hue='gender',
            marker='o',
            linewidth=2.5
        )
        plot.set_title("Financial Account Ownership Trajectory (Ethiopia)")
        plot.set_ylabel("Ownership Rate (%)")
        plot.set_xlabel("Year")
        
        plt.tight_layout()
        plt.show()
        save_path = self.output_dir / "account_ownership_trend.png"
        plt.savefig(save_path)
        plt.close()
        logger.info(f"Saved ownership plot to {save_path}")

    def plot_usage_gap(self, gap_data: Dict):
        """Visualize the gap between registered and active users with error handling."""
        plt.figure()
        
        # Define the mapping
        labels_map = {
            'mm_accounts_pct': 'Mobile Money Accounts', 
            'digital_payment_pct': 'Active Digital Payments'
        }
        
        # Filter out None values to prevent TypeErrors
        plot_data = {
            labels_map[k]: v for k, v in gap_data.items() 
            if k in labels_map and v is not None
        }
        
        if not plot_data:
            logger.warning("No valid data found for usage gap plot.")
            plt.text(0.5, 0.5, "Data Not Available", ha='center')
            plt.close()
            return

        labels = list(plot_data.keys())
        values = list(plot_data.values())
        
        plot = sns.barplot(x=labels, y=values, palette="viridis")
        plot.set_title("Registered vs. Active Usage Gap")
        plot.set_ylabel("Percentage (%)")
        
        # Annotate values safely
        for i, v in enumerate(values):
            # Only attempt to add 0.5 if v is a number
            plot.text(i, v , f"{v}%", ha='center', fontweight='bold')
            
        plt.tight_layout()
        plt.show()
        save_path = self.output_dir / "usage_gap_analysis.png"
        plt.savefig(save_path)
        plt.close()

    def plot_infrastructure_benchmarks(self, infra_data: Dict):
        """Plot the scaling of enabling infrastructure (4G, Smartphone, etc.)."""
        plt.figure()
        names = list(infra_data.keys())
        values = [v['latest_value'] for v in infra_data.values()]
        
        df = pd.DataFrame({'Indicator': names, 'Value': values})
        df = df.sort_values('Value', ascending=False)
        
        plot = sns.barplot(data=df, x='Value', y='Indicator', palette="magma")
        plot.set_title("Enabling Infrastructure Penetration (2024-2025)")
        plot.set_xlabel("Penetration Rate (%)")
        
        plt.tight_layout()
        plt.show()
        save_path = self.output_dir / "infrastructure_benchmarks.png"
        plt.savefig(save_path)
        plt.close()

    def plot_impact_magnitudes(self, impact_df: pd.DataFrame):
        """Visualize the strength of relationship drivers."""
        plt.figure()
        # Top 10 drivers
        top_drivers = impact_df.nlargest(10, 'impact_magnitude_numeric')
        
        plot = sns.barplot(
            data=impact_df.nlargest(10, 'impact_magnitude_numeric'), 
                x='impact_magnitude_numeric', 
                y='parent_id',
                hue='impact_direction'
        )
        plot.set_title("Top Drivers of Financial Inclusion")
        plot.set_xlabel("Estimated Impact Magnitude (%)")
        plot.set_ylabel("Driving Factor")
        
        plt.tight_layout()
        plt.show()
        save_path = self.output_dir / "impact_drivers.png"
        plt.savefig(save_path)
        plt.close()

    def plot_usage_gap_bar(self, df: pd.DataFrame):
        """1. Usage Gap Bar Chart - Registered vs. Active Digital Users"""
        plt.figure(figsize=(10, 6))
        # Logic: Filter for Telebirr users (Registered) vs Active Rate
        # Based on CSV: USG_TELEBIRR_USERS vs USG_ACTIVE_RATE
        metrics = df[df['indicator_code'].isin(['USG_TELEBIRR_USERS', 'USG_ACTIVE_RATE'])]
        
        plot = sns.barplot(data=metrics, x='indicator', y='value_numeric', palette='flare')
        plot.set_title("Digital Finance Usage Gap: Registration vs. 90-Day Activity")
        plot.set_ylabel("Value (Users Count / Percentage)")
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "usage_gap_bar.png")
        plt.show()

    def plot_gender_ownership_heatmap(self, df: pd.DataFrame):
        """2. Gender-Disaggregated Ownership Gap Heatmap"""
        # Pivot the data: Rows=Years, Cols=Gender, Values=Ownership Rate
        gender_df = df[df['indicator_code'] == 'ACC_OWNERSHIP'].pivot_table(
            index='fiscal_year', columns='gender', values='value_numeric'
        )
        
        if not gender_df.empty:
            plt.figure(figsize=(10, 5))
            # Calculate gap for annotation
            plot = sns.heatmap(gender_df, annot=True, cmap="YlGnBu", fmt=".1f")
            plot.set_title("Gender Ownership Gap over Time")
            
            plt.tight_layout()
            plt.savefig(self.output_dir / "gender_ownership_heatmap.png")
            plt.show()

    def plot_infra_vs_ownership_scatter(self, df: pd.DataFrame):
        """3. Infrastructure vs. Ownership Correlation Scatter Plot"""
        # Prepare data: Need rows where we have both infra and ownership for same period
        pivot_df = df.pivot_table(
            index=['fiscal_year', 'location'], 
            columns='indicator_code', 
            values='value_numeric'
        ).reset_index()

        # Assuming ACC_MOBILE_PEN (Infra) and ACC_OWNERSHIP (Ownership)
        if 'ACC_MOBILE_PEN' in pivot_df.columns and 'ACC_OWNERSHIP' in pivot_df.columns:
            plt.figure(figsize=(10, 6))
            plot = sns.scatterplot(
                data=pivot_df, x='ACC_MOBILE_PEN', y='ACC_OWNERSHIP', 
                hue='fiscal_year', size='ACC_MOBILE_PEN', sizes=(100, 400)
            )
            sns.regplot(data=pivot_df, x='ACC_MOBILE_PEN', y='ACC_OWNERSHIP', scatter=False, color='gray')
            
            plot.set_title("Correlation: Mobile Penetration vs. Account Ownership")
            plot.set_xlabel("Mobile Penetration Rate (%)")
            plot.set_ylabel("Account Ownership (%)")
            
            plt.tight_layout()
            plt.savefig(self.output_dir / "infra_ownership_correlation.png")
            plt.show()

    def plot_transaction_type_pie(self, df: pd.DataFrame):
        """4. Transaction Type Distribution Pie Chart"""
        # Filter for transaction indicators (e.g., P2P, Merchant, Utility)
        tx_indicators = ['USG_P2P_COUNT', 'USG_MERCHANT_PAY', 'USG_UTILITY_PAY']
        tx_data = df[df['indicator_code'].isin(tx_indicators)].copy()
        
        if not tx_data.empty:
            plt.figure(figsize=(8, 8))
            plt.pie(
                tx_data['value_numeric'], 
                labels=tx_data['indicator'], 
                autopct='%1.1f%%', 
                colors=sns.color_palette('pastel')
            )
            plt.title("Volume Distribution by Transaction Type")
            
            plt.savefig(self.output_dir / "transaction_distribution_pie.png")
            plt.show()