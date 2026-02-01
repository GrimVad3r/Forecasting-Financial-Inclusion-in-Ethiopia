import pandas as pd
import numpy as np
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

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

class DataExplorer:
    """Explore and understand data patterns."""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def explore_events(self, df: pd.DataFrame) -> pd.DataFrame:
        """Explore cataloged events."""
        self.logger.info("\nExploring cataloged events")
        
        events = df[df['record_type'] == 'event'].copy()
        events['observation_date'] = pd.to_datetime(events['observation_date'], errors='coerce')
        events = events.sort_values('observation_date')
        
        event_summary = events[['record_id', 'category', 'indicator', 'observation_date', 'confidence', 'source_name']].copy()
        
        self.logger.info(f"\nTotal events: {len(events)}")
        self.logger.info(f"\nEvent Categories:\n{events['category'].value_counts().to_string()}")
        self.logger.info(f"\nEvent Timeline:\n{event_summary.to_string(index=False)}")
        
        return event_summary
    
    def explore_impact_links(self, impact_df: pd.DataFrame) -> pd.DataFrame:
        """Explore impact relationships."""
        self.logger.info("\nExploring impact links")
        
        impact_summary = impact_df[['record_id', 'parent_id', 'indicator_code', 'impact_direction', 
                                      'impact_magnitude', 'lag_months', 'evidence_basis']].copy()
        
        self.logger.info(f"\nTotal impact links: {len(impact_summary)}")
        self.logger.info(f"\nImpact Directions:\n{impact_df['impact_direction'].value_counts().to_string()}")
        self.logger.info(f"\nEvidence Basis:\n{impact_df['evidence_basis'].value_counts().to_string()}")
        
        return impact_summary
    
    def analyze_data_quality(self, df: pd.DataFrame) -> Dict:
        """Analyze data quality metrics."""
        self.logger.info("\nAnalyzing data quality")
        
        observations = df[df['record_type'] == 'observation'].copy()
        
        quality_metrics = {
            'total_observations': len(observations),
            'confidence_distribution': observations['confidence'].value_counts().to_dict(),
            'source_type_distribution': observations['source_type'].value_counts().to_dict(),
            'missing_urls': observations['source_url'].isnull().sum(),
            'missing_values_numeric': observations['value_numeric'].isnull().sum(),
            'completeness_pct': round((1 - (observations.isnull().sum().sum() / (len(observations) * len(observations.columns)))) * 100, 2)
        }
        
        self.logger.info(f"\nData Quality Metrics:")
        self.logger.info(f"  Total observations: {quality_metrics['total_observations']}")
        self.logger.info(f"  Confidence distribution: {quality_metrics['confidence_distribution']}")
        self.logger.info(f"  Completeness: {quality_metrics['completeness_pct']}%")
        
        return quality_metrics