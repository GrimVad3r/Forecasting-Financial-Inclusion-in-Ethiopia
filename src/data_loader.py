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

class DataLoader:
    """Load and validate datasets from Excel files."""
    
    def __init__(self, data_dir: str = '../data/raw'):
        self.data_dir = Path(data_dir)
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def load_unified_data(self, filename: str = 'ethiopia_fi_unified_data.xlsx') -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load unified data and impact links sheets.
        
        Returns:
            Tuple of (unified_data_df, impact_links_df)
        """
        try:
            filepath = self.data_dir / filename
            self.logger.info(f"Loading unified data from {filepath}")
            
            # Load main data sheet
            unified_data = pd.read_excel(filepath, sheet_name='ethiopia_fi_unified_data')
            self.logger.info(f"Loaded unified data: {unified_data.shape[0]} rows, {unified_data.shape[1]} columns")
            
            # Load impact links
            impact_links = pd.read_excel(filepath, sheet_name='Impact_sheet')
            self.logger.info(f"Loaded impact links: {impact_links.shape[0]} rows, {impact_links.shape[1]} columns")
            
            return unified_data, impact_links
        except FileNotFoundError as e:
            self.logger.error(f"File not found: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise
    
    def load_reference_codes(self, filename: str = 'reference_codes.xlsx') -> pd.DataFrame:
        """Load reference codes for validation."""
        try:
            filepath = self.data_dir / filename
            self.logger.info(f"Loading reference codes from {filepath}")
            
            ref_codes = pd.read_excel(filepath, sheet_name='reference_codes')
            self.logger.info(f"Loaded reference codes: {ref_codes.shape[0]} rows")
            
            return ref_codes
        except FileNotFoundError as e:
            self.logger.error(f"File not found: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading reference codes: {e}")
            raise