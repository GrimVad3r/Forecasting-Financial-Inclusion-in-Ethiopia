"""
Data Loading and Validation Module
Handles loading, validating, and preparing data for financial inclusion analysis.
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load and validate financial inclusion datasets."""
    
    def __init__(self, data_dir: str = "data/raw"):
        """
        Initialize DataLoader.
        
        Args:
            data_dir: Path to raw data directory
        """
        self.data_dir = Path(data_dir)
        self.data = None
        self.reference_codes = None
        logger.info(f"DataLoader initialized with data_dir: {data_dir}")
    
    def load_datasets(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load main dataset and reference codes.
        
        Returns:
            Tuple of (unified_data, reference_codes) DataFrames
            
        Raises:
            FileNotFoundError: If required files not found
            ValueError: If data validation fails
        """
        try:
            # Load main dataset
            data_path = self.data_dir / "ethiopia_fi_unified_data.xlsx"
            if not data_path.exists():
                raise FileNotFoundError(f"Data file not found: {data_path}")
            
            self.data = pd.read_excel(data_path,sheet_name='ethiopia_fi_unified_data')
            logger.info(f"Loaded {len(self.data)} records from {data_path}")

            # Load Impact Data
            data_path = self.data_dir / "ethiopia_fi_unified_data.xlsx"
            if not data_path.exists():
                raise FileNotFoundError(f"Data file not found: {data_path}")
            
            self.impact_data = pd.read_excel(data_path,sheet_name='Impact_sheet')
            logger.info(f"Loaded {len(self.impact_data)} records from {data_path}")
            
            # Load reference codes
            ref_path = self.data_dir / "reference_codes.xlsx"
            if not ref_path.exists():
                raise FileNotFoundError(f"Reference file not found: {ref_path}")
            
            self.reference_codes = pd.read_excel(ref_path,sheet_name='reference_codes')
            logger.info(f"Loaded reference codes from {ref_path}")
            
            # Validate data
            self._validate_data()
            
            return self.data, self.reference_codes
            
        except Exception as e:
            logger.error(f"Failed to load datasets: {str(e)}")
            raise
    
    def _validate_data(self) -> None:
        """
        Validate data structure and required columns.
        
        Raises:
            ValueError: If validation fails
        """
        try:
            # Check for required columns
            required_cols = ['record_type', 'indicator_code', 'observation_date']
            missing_cols = [col for col in required_cols if col not in self.data.columns]
            
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Check for null values in critical fields
            critical_nulls = self.data[required_cols].isnull().sum()
            if critical_nulls.any():
                logger.warning(f"Null values found in critical columns:\n{critical_nulls[critical_nulls > 0]}")
            
            # Validate record_type values
            valid_types = ['observation', 'event', 'impact_link', 'target']
            invalid_types = self.data[~self.data['record_type'].isin(valid_types)]['record_type'].unique()
            if len(invalid_types) > 0:
                logger.warning(f"Found invalid record_type values: {invalid_types}")
            
            logger.info("Data validation completed successfully")
            
        except Exception as e:
            logger.error(f"Data validation failed: {str(e)}")
            raise
    
    def get_observations(self) -> pd.DataFrame:
        """Get only observation records."""
        try:
            obs = self.data[self.data['record_type'] == 'observation'].copy()
            logger.info(f"Retrieved {len(obs)} observation records")
            return obs
        except Exception as e:
            logger.error(f"Failed to get observations: {str(e)}")
            raise
    
    def get_events(self) -> pd.DataFrame:
        """Get only event records."""
        try:
            events = self.data[self.data['record_type'] == 'event'].copy()
            logger.info(f"Retrieved {len(events)} event records")
            return events
        except Exception as e:
            logger.error(f"Failed to get events: {str(e)}")
            raise
    
    def get_impact_links(self) -> pd.DataFrame:
        """Get only impact_link records."""
        try:
            links = self.impact_data[self.impact_data['record_type'] == 'impact_link'].copy()
            logger.info(f"Retrieved {len(links)} impact_link records")
            return links
        except Exception as e:
            logger.error(f"Failed to get impact_links: {str(e)}")
            raise
    
    def parse_dates(self, date_columns: list = None) -> pd.DataFrame:
        """
        Parse date columns to datetime.
        
        Args:
            date_columns: List of columns to parse as dates
            
        Returns:
            DataFrame with parsed dates
        """
        try:
            if date_columns is None:
                date_columns = ['observation_date', 'event_date']
            
            data = self.data.copy()
            for col in date_columns:
                if col in data.columns:
                    data[col] = pd.to_datetime(data[col], errors='coerce')
                    null_count = data[col].isnull().sum()
                    if null_count > 0:
                        logger.warning(f"Failed to parse {null_count} dates in {col}")
            
            logger.info("Date parsing completed")
            return data
            
        except Exception as e:
            logger.error(f"Failed to parse dates: {str(e)}")
            raise


class DataEnricher:
    """Handle data enrichment with new observations, events, and impact links."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize DataEnricher.
        
        Args:
            data: The base DataFrame to enrich
        """
        self.data = data.copy()
        self.enrichment_log = []
        logger.info("DataEnricher initialized")
    
    def add_observation(self, 
                       indicator_code: str,
                       value_numeric: float,
                       observation_date: str,
                       source_name: str,
                       source_url: str = None,
                       confidence: str = 'medium',
                       pillar: str = None,
                       notes: str = None) -> None:
        """
        Add a new observation record.
        
        Args:
            indicator_code: Code for the indicator
            value_numeric: Numeric value
            observation_date: Date of observation
            source_name: Name of the source
            source_url: URL of the source
            confidence: Confidence level (high/medium/low)
            pillar: access or usage pillar
            notes: Additional notes
        """
        try:
            new_record = {
                'record_type': 'observation',
                'indicator_code': indicator_code,
                'value_numeric': value_numeric,
                'observation_date': observation_date,
                'source_name': source_name,
                'source_url': source_url,
                'confidence': confidence,
                'pillar': pillar,
                'notes': notes,
                'collected_by': 'data_enrichment',
                'collection_date': datetime.now().strftime('%Y-%m-%d')
            }
            
            self.data = pd.concat([self.data, pd.DataFrame([new_record])], ignore_index=True)
            self.enrichment_log.append(f"Added observation: {indicator_code} = {value_numeric} on {observation_date}")
            logger.info(f"Added observation for {indicator_code}")
            
        except Exception as e:
            logger.error(f"Failed to add observation: {str(e)}")
            raise
    
    def add_event(self,
                  event_name: str,
                  event_date: str,
                  category: str,
                  source_name: str = None,
                  source_url: str = None,
                  description: str = None) -> str:
        """
        Add a new event record.
        
        Args:
            event_name: Name of the event
            event_date: Date of the event
            category: Type of event (policy, product_launch, etc.)
            source_name: Source name
            source_url: Source URL
            description: Event description
            
        Returns:
            The event_id for use in impact_links
        """
        try:
            event_id = f"EVT_{len(self.data)}"
            new_record = {
                'record_type': 'event',
                'event_id': event_id,
                'event_name': event_name,
                'event_date': event_date,
                'category': category,
                'source_name': source_name,
                'source_url': source_url,
                'description': description,
                'collected_by': 'data_enrichment',
                'collection_date': datetime.now().strftime('%Y-%m-%d')
            }
            
            self.data = pd.concat([self.data, pd.DataFrame([new_record])], ignore_index=True)
            self.enrichment_log.append(f"Added event: {event_name} on {event_date}")
            logger.info(f"Added event: {event_name} (ID: {event_id})")
            
            return event_id
            
        except Exception as e:
            logger.error(f"Failed to add event: {str(e)}")
            raise
    
    def save_enrichment_log(self, filepath: str = "data_enrichment_log.md") -> None:
        """
        Save enrichment log to file.
        
        Args:
            filepath: Path to save log
        """
        try:
            with open(filepath, 'w') as f:
                f.write("# Data Enrichment Log\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("## Changes Made\n\n")
                for log_entry in self.enrichment_log:
                    f.write(f"- {log_entry}\n")
            
            logger.info(f"Enrichment log saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save enrichment log: {str(e)}")
            raise
    
    def get_enriched_data(self) -> pd.DataFrame:
        """Return the enriched data."""
        return self.data.copy()