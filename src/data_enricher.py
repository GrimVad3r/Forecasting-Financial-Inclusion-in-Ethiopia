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

class DataEnricher:
    """Enrich dataset with new observations and events."""
    
    def __init__(self, reference_df: pd.DataFrame, logger=None):
        self.reference_df = reference_df
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.enrichment_log = []
    
    def validate_record(self, record: Dict, record_type: str) -> bool:
        """Validate record against schema and reference codes."""
        try:
            # Check required fields
            required_fields = {
                'observation': ['record_id', 'record_type', 'indicator_code', 'value_numeric', 'observation_date', 'source_name', 'confidence'],
                'event': ['record_id', 'record_type', 'category', 'observation_date', 'source_name'],
                'impact_link': ['record_id', 'parent_id', 'indicator_code', 'impact_direction']
            }
            
            for field in required_fields.get(record_type, []):
                if field not in record or pd.isna(record.get(field)):
                    self.logger.warning(f"Missing field {field} in record {record.get('record_id')}")
                    return False
            
            return True
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return False
    
    def add_observation(self, df: pd.DataFrame, record: Dict) -> pd.DataFrame:
        """Add new observation to dataset."""
        try:
            if not self.validate_record(record, 'observation'):
                return df
            
            new_df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            self.enrichment_log.append({
                'action': 'add_observation',
                'record_id': record['record_id'],
                'timestamp': datetime.now(),
                'notes': record.get('notes', 'Added via enrichment')
            })
            
            self.logger.info(f"Added observation {record['record_id']}")
            return new_df
        except Exception as e:
            self.logger.error(f"Error adding observation: {e}")
            return df
    
    def add_event(self, df: pd.DataFrame, record: Dict) -> pd.DataFrame:
        """Add new event to dataset."""
        try:
            if not self.validate_record(record, 'event'):
                return df
            
            # Ensure record_type is 'event'
            record['record_type'] = 'event'
            
            new_df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            self.enrichment_log.append({
                'action': 'add_event',
                'record_id': record['record_id'],
                'category': record.get('category'),
                'timestamp': datetime.now()
            })
            
            self.logger.info(f"Added event {record['record_id']}")
            return new_df
        except Exception as e:
            self.logger.error(f"Error adding event: {e}")
            return df
    
    def get_enrichment_log(self) -> pd.DataFrame:
        """Return enrichment log as DataFrame."""
        return pd.DataFrame(self.enrichment_log)