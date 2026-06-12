# -*- coding: utf-8 -*-
"""
Price Analysis Module - Arbitrage calculations and analysis
"""

import pandas as pd
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PriceAnalyzer:
    """Price analysis and arbitrage opportunities"""
    
    def __init__(self, commission_calculator=None):
        self.commission_calculator = commission_calculator
    
    def find_best_price_with_filters(self, df_skins: pd.DataFrame,
                                     min_rating: Optional[float] = None,
                                     max_rating: Optional[float] = None) -> pd.DataFrame:
        """Find best price per product with optional rating filters"""
        if df_skins.empty:
            return pd.DataFrame()
        
        df = df_skins.copy()
        
        if min_rating is not None or max_rating is not None:
            min_r = min_rating if min_rating is not None else 0
            max_r = max_rating if max_rating is not None else 5.0
            df = df[(df['site_rating'] >= min_r) & (df['site_rating'] <= max_r)]
        
        if df.empty:
            logger.warning("No sites match the rating filter")
            return pd.DataFrame()
        
        best_prices = df.loc[df.groupby('name')['site_price'].idxmin()]
        return best_prices
    
    def calculate_profit_percentages(self, df: pd.DataFrame,
                                    direction: str = "steam_to_cash") -> pd.DataFrame:
        """Calculate profit percentage for each row"""
        if df.empty or self.commission_calculator is None:
            return df
        
        df = df.copy()
        profit_percentages = []
        
        for idx, row in df.iterrows():
            profit_pct = self.commission_calculator.calculate_profit_percentage(
                steam_price=row['steam_price'],
                site_price=row['site_price'],
                site=row['site'],
                direction=direction
            )
            profit_percentages.append(profit_pct)
        
        df['profit_percentage'] = profit_percentages
        return df
    
    def find_arbitrage_opportunities(self, df_skins: pd.DataFrame,
                                    min_profit_threshold: float = 0,
                                    min_rating: Optional[float] = None,
                                    max_rating: Optional[float] = None,
                                    direction: str = "steam_to_cash") -> pd.DataFrame:
        """Find arbitrage opportunities above profit threshold"""
        if df_skins.empty:
            return pd.DataFrame()
        
        best_prices = self.find_best_price_with_filters(
            df_skins, min_rating=min_rating, max_rating=max_rating
        )
        
        if best_prices.empty:
            return pd.DataFrame()
        
        df_profit = self.calculate_profit_percentages(best_prices, direction)
        arbitrage_df = df_profit[df_profit['profit_percentage'] >= min_profit_threshold]
        
        return arbitrage_df.sort_values('profit_percentage', ascending=False)
    
    def identify_manipulation_candidates(self, df_skins: pd.DataFrame,
                                        max_daily_volume: int = 10) -> List[str]:
        """Identify suspicious items with low volume"""
        if df_skins.empty:
            return []
        
        suspicious = df_skins[df_skins['daily_volume'] < max_daily_volume]['name'].unique().tolist()
        return suspicious
    
    def get_profit_summary(self, df: pd.DataFrame,
                          group_by: str = "product_type") -> pd.DataFrame:
        """Get profit summary grouped by category"""
        if df.empty or 'profit_percentage' not in df.columns:
            return pd.DataFrame()
        
        summary = df.groupby(group_by).agg({
            'profit_percentage': ['mean', 'min', 'max', 'count'],
            'steam_price': 'mean',
            'site_price': 'mean'
        }).round(2)
        
        return summary
    
    def compare_arbitrage_strategies(self, df_skins: pd.DataFrame,
                                    target_balance: float, site: str) -> pd.DataFrame:
        """Compare different arbitrage strategies"""
        if df_skins.empty or self.commission_calculator is None:
            return pd.DataFrame()
        
        df = df_skins.copy()
        results = []
        
        for idx, row in df.iterrows():
            steam_price = row['steam_price']
            site_price = row['site_price']
            
            qty_s2c, net_per_s2c, total_net_s2c = self.commission_calculator.calculate_quantity_needed(
                target_balance=target_balance,
                unit_price=steam_price,
                direction="steam_to_cash",
                site=site
            )
            
            profit_s2c = self.commission_calculator.calculate_profit_percentage(
                steam_price, site_price, site, "steam_to_cash"
            )
            
            qty_c2s, _, total_net_c2s = self.commission_calculator.calculate_quantity_needed(
                target_balance=target_balance,
                unit_price=steam_price,
                direction="cash_to_steam",
                site=site
            )
            
            profit_c2s = self.commission_calculator.calculate_profit_percentage(
                steam_price, site_price, site, "cash_to_steam"
            )
            
            results.append({
                'name': row['name'],
                'steam_price': steam_price,
                'site_price': site_price,
                's2c_quantity': qty_s2c,
                's2c_net': total_net_s2c,
                's2c_profit_%': profit_s2c,
                'c2s_quantity': qty_c2s,
                'c2s_net': total_net_c2s,
                'c2s_profit_%': profit_c2s,
            })
        
        return pd.DataFrame(results)
    
    def identify_best_opportunities_by_profit_range(self, df_skins: pd.DataFrame,
                                                   min_profit: float,
                                                   max_profit: float,
                                                   direction: str = "steam_to_cash") -> pd.DataFrame:
        """Find opportunities within specific profit range"""
        if df_skins.empty:
            return pd.DataFrame()
        
        df = self.calculate_profit_percentages(df_skins, direction)
        filtered = df[(df['profit_percentage'] >= min_profit) & 
                     (df['profit_percentage'] <= max_profit)]
        
        return filtered.sort_values('profit_percentage', ascending=False)
