import pandas as pd
import numpy as np
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json
from data_enricher import DataEnricher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('task_1_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DataExporter:
    """Export enriched data and generate documentation."""
    
    def __init__(self, output_dir: str = './data/processed', logger=None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def export_enriched_data(self, df: pd.DataFrame, filename: str = 'ethiopia_fi_unified_data_enriched.csv') -> str:
        """Export enriched dataset."""
        try:
            filepath = self.output_dir / filename
            df.to_csv(filepath, index=False)
            self.logger.info(f"Exported enriched data to {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error exporting data: {e}")
            raise
    
    def create_enrichment_log(self, enricher: DataEnricher, filename: str = 'data_enrichment_log.md') -> str:
        """Create enrichment documentation."""
        try:
            filepath = self.output_dir / filename
            
            with open(filepath, 'w') as f:
                f.write("# Data Enrichment Log\n\n")
                f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("## Summary\n")
                f.write(f"- Total enrichment actions: {len(enricher.enrichment_log)}\n\n")
                
                f.write("## Enrichment Details\n\n")
                for i, log_entry in enumerate(enricher.enrichment_log, 1):
                    f.write(f"### {i}. {log_entry['action'].upper()}\n")
                    f.write(f"- Record ID: {log_entry['record_id']}\n")
                    f.write(f"- Timestamp: {log_entry['timestamp']}\n")
                    f.write(f"- Notes: {log_entry.get('notes', log_entry.get('category', 'N/A'))}\n\n")
            
            self.logger.info(f"Created enrichment log at {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error creating enrichment log: {e}")
            raise
    
    def create_summary_report(self, record_types_dist: pd.DataFrame, analysis_dict: Dict, filename: str = 'task_1_summary.json') -> str:
        """Create summary report of findings."""
        try:
            filepath = self.output_dir / filename
            
            # Convert datetime objects to strings for JSON serialization
            summary_report = {
                'execution_date': datetime.now().isoformat(),
                'data_overview': {
                    'total_records': int(analysis_dict['shape'][0]),
                    'total_columns': int(analysis_dict['shape'][1])
                },
                'record_types': {
                    'observation': int(record_types_dist[record_types_dist['record_type'] == 'observation']['count'].values[0]) if len(record_types_dist[record_types_dist['record_type'] == 'observation']) > 0 else 0,
                    'event': int(record_types_dist[record_types_dist['record_type'] == 'event']['count'].values[0]) if len(record_types_dist[record_types_dist['record_type'] == 'event']) > 0 else 0,
                    'impact_link': int(record_types_dist[record_types_dist['record_type'] == 'impact_link']['count'].values[0]) if len(record_types_dist[record_types_dist['record_type'] == 'impact_link']) > 0 else 0,
                    'target': int(record_types_dist[record_types_dist['record_type'] == 'target']['count'].values[0]) if len(record_types_dist[record_types_dist['record_type'] == 'target']) > 0 else 0
                }
            }
            
            with open(filepath, 'w') as f:
                json.dump(summary_report, f, indent=2, default=str)
            
            self.logger.info(f"Created summary report at {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error creating summary report: {e}")
            raise