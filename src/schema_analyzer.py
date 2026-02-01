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

class SchemaAnalyzer:
    """Analyze and validate data schema."""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def analyze_structure(self, df: pd.DataFrame, df_name: str = "Dataset") -> Dict:
        """Analyze dataset structure."""
        self.logger.info(f"\nAnalyzing structure of {df_name}")
        
        analysis = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_rows': df.duplicated().sum()
        }
        
        self.logger.info(f"Shape: {analysis['shape']}")
        self.logger.info(f"Columns ({len(analysis['columns'])}): {analysis['columns'][:5]}...")
        self.logger.info(f"Missing values: {sum(analysis['missing_values'].values())} total")
        self.logger.info(f"Duplicate rows: {analysis['duplicate_rows']}")
        
        return analysis
    
    def analyze_record_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze distribution of record types."""
        self.logger.info("\nAnalyzing record types distribution")
        
        record_types = df['record_type'].value_counts().reset_index()
        record_types.columns = ['record_type', 'count']
        record_types['percentage'] = (record_types['count'] / record_types['count'].sum() * 100).round(2)
        
        self.logger.info(f"\nRecord Types Distribution:\n{record_types.to_string(index=False)}")
        
        return record_types
    
    def analyze_temporal_coverage(self, df: pd.DataFrame) -> Dict:
        """Analyze temporal coverage of data."""
        self.logger.info("\nAnalyzing temporal coverage")
        
        # Convert observation_date to datetime
        df['observation_date'] = pd.to_datetime(df['observation_date'], errors='coerce')
        
        temporal_info = {
            'earliest_date': df['observation_date'].min(),
            'latest_date': df['observation_date'].max(),
            'total_years': (df['observation_date'].max() - df['observation_date'].min()).days / 365.25
        }
        
        self.logger.info(f"Earliest date: {temporal_info['earliest_date']}")
        self.logger.info(f"Latest date: {temporal_info['latest_date']}")
        self.logger.info(f"Total span: {temporal_info['total_years']:.1f} years")
        
        return temporal_info
    
    def analyze_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze indicator coverage."""
        self.logger.info("\nAnalyzing indicator coverage")
        
        observations = df[df['record_type'] == 'observation'].copy()
        indicator_analysis = observations.groupby('indicator_code').agg({
            'record_id': 'count',
            'indicator': 'first',
            'observation_date': ['min', 'max'],
            'confidence': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'unknown'
        }).round(2)
        
        indicator_analysis.columns = ['count', 'indicator_name', 'earliest', 'latest', 'primary_confidence']
        indicator_analysis = indicator_analysis.reset_index()
        
        self.logger.info(f"\nIndicator Coverage ({len(indicator_analysis)} unique indicators):\n{indicator_analysis.to_string(index=False)}")
        
        return indicator_analysis