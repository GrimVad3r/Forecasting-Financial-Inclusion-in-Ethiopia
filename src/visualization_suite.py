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