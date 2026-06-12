# -*- coding: utf-8 -*-
"""
Data Management Module - Pandas DataFrame operations
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SkinData:
    """Data class for skin information"""
    name: str
    product_type: str
    steam_price: float
    daily_volume: int
    marketplace_data: Dict


class DataManager:
    """Data management and DataFrame operations"""
    
    def __init__(self):
        self.df_skins = pd.DataFrame()
        self.df_marketplace = pd.DataFrame()
        self.cache = {}
        
    def create_skin_dataframe(self, skins_data: List[Dict]) -> pd.DataFrame:
        """Create DataFrame from skin data"""
        try:
            self.df_skins = pd.DataFrame(skins_data)
            self.df_skins['steam_price'] = pd.to_numeric(self.df_skins['steam_price'], errors='coerce')
            self.df_skins['daily_volume'] = pd.to_numeric(self.df_skins['daily_volume'], errors='coerce')
            self.df_skins = self.df_skins.dropna(subset=['steam_price', 'name'])
            logger.info(f"Skin DataFrame created: {len(self.df_skins)} rows")
            return self.df_skins
        except Exception as e:
            logger.error(f"DataFrame creation error: {e}")
            return pd.DataFrame()
    
    def flatten_marketplace_data(self) -> pd.DataFrame:
        """Flatten marketplace data - expand to show all sites per product"""
        try:
            expanded_rows = []
            for idx, row in self.df_skins.iterrows():
                marketplace_data = row['marketplace_data']
                if not marketplace_data:
                    continue
                for site, site_data in marketplace_data.items():
                    expanded_row = {
                        'name': row['name'],
                        'product_type': row['product_type'],
                        'steam_price': row['steam_price'],
                        'daily_volume': row['daily_volume'],
                        'site': site,
                        'site_price': site_data.get('price', 0),
                        'site_rating': site_data.get('rating', 0),
                        'available_quantity': site_data.get('available_quantity', 0),
                    }
                    expanded_rows.append(expanded_row)
            self.df_marketplace = pd.DataFrame(expanded_rows)
            logger.info(f"Marketplace DataFrame created: {len(self.df_marketplace)} records")
            return self.df_marketplace
        except Exception as e:
            logger.error(f"Marketplace data flattening error: {e}")
            return pd.DataFrame()
    
    def apply_filters(self, df=None, min_rating: Optional[float] = None,
                     max_rating: Optional[float] = None,
                     min_price: Optional[float] = None,
                     max_price: Optional[float] = None,
                     product_types: Optional[List[str]] = None,
                     min_volume: Optional[int] = None) -> pd.DataFrame:
        """Apply all filters combined"""
        if df is None:
            df = self.df_marketplace.copy()
        else:
            df = df.copy()
        
        if min_rating is not None and max_rating is not None:
            df = df[(df['site_rating'] >= min_rating) & (df['site_rating'] <= max_rating)]
        
        if min_price is not None and max_price is not None:
            df = df[(df['steam_price'] >= min_price) & (df['steam_price'] <= max_price)]
        
        if product_types:
            df = df[df['product_type'].isin(product_types)]
        
        if min_volume is not None:
            df = df[df['daily_volume'] >= min_volume]
        
        return df
    
    def sort_by_profit_percentage(self, df: Optional[pd.DataFrame] = None, 
                                  ascending: bool = False) -> pd.DataFrame:
        """Sort by profit percentage"""
        if df is None:
            df = self.df_marketplace
        if 'profit_percentage' not in df.columns:
            return df
        return df.sort_values('profit_percentage', ascending=ascending)
    
    def sort_by_price(self, df: Optional[pd.DataFrame] = None, 
                     ascending: bool = True) -> pd.DataFrame:
        """Sort by price"""
        if df is None:
            df = self.df_marketplace
        return df.sort_values('steam_price', ascending=ascending)
    
    def sort_by_rating(self, df: Optional[pd.DataFrame] = None, 
                      ascending: bool = False) -> pd.DataFrame:
        """Sort by rating"""
        if df is None:
            df = self.df_marketplace
        return df.sort_values('site_rating', ascending=ascending)
    
    def get_best_price_per_skin(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get best price per skin from filtered sites"""
        if df.empty:
            return pd.DataFrame()
        return df.loc[df.groupby('name')['site_price'].idxmin()]
    
    def get_summary_stats(self, df: Optional[pd.DataFrame] = None) -> Dict:
        """Get summary statistics"""
        if df is None or df.empty:
            return {}
        return {
            'total_skins': df['name'].nunique(),
            'total_sites': df['site'].nunique(),
            'avg_price': df['steam_price'].mean(),
            'avg_rating': df['site_rating'].mean(),
            'avg_profit': df['profit_percentage'].mean() if 'profit_percentage' in df.columns else 0,
        }
    
    def export_to_csv(self, df: pd.DataFrame, filename: str = 'arbitrage_results.csv'):
        """Export to CSV"""
        try:
            df.to_csv(filename, index=False)
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"CSV export error: {e}")
    
