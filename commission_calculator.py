# -*- coding: utf-8 -*-
"""
Commission Calculator Module - Tax and Commission calculations
"""

from typing import Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommissionCalculator:
    """Tax and commission calculations"""
    
    def __init__(self, site_commissions: Dict[str, float], steam_commission: float = 15.0):
        """Initialize commission calculator"""
        self.site_commissions = site_commissions
        self.steam_commission = steam_commission
    
    def get_site_commission(self, site: str) -> float:
        """Get commission rate for a site"""
        return self.site_commissions.get(site.lower(), 0)
    
    def calculate_net_amount_steam_to_cash(self, steam_price: float, site: str) -> float:
        """
        Calculate net amount: Steam -> Cash conversion
        net = steam_price * (1 - steam_commission%) * (1 - site_commission%)
        """
        if steam_price <= 0:
            return 0
        
        after_steam = steam_price * (1 - self.steam_commission / 100)
        site_comm = self.get_site_commission(site)
        net_amount = after_steam * (1 - site_comm / 100)
        return max(0, net_amount)
    
    def calculate_net_amount_cash_to_steam(self, target_steam_price: float, source_site: str) -> float:
        """
        Calculate required amount: Cash -> Steam conversion
        How much cash is needed to get target_steam_price worth of items?
        """
        if target_steam_price <= 0:
            return 0
        
        site_commission_rate = self.get_site_commission(source_site) / 100
        required_amount = target_steam_price / (1 - site_commission_rate)
        return max(0, required_amount)
    
    def calculate_quantity_needed(self, target_balance: float, unit_price: float,
                                 direction: str, site: str) -> Tuple[int, float, float]:
        """
        Calculate quantity needed to reach target balance
        Returns: (quantity, net_per_unit, total_net)
        """
        if unit_price <= 0:
            return 0, 0, 0
        
        if direction == "steam_to_cash":
            net_per_unit = self.calculate_net_amount_steam_to_cash(unit_price, site)
            if net_per_unit <= 0:
                return 0, 0, 0
            quantity = int(target_balance / net_per_unit)
            if quantity == 0:
                quantity = 1
            total_net = quantity * net_per_unit
            
        elif direction == "cash_to_steam":
            required_per_unit = self.calculate_net_amount_cash_to_steam(unit_price, site)
            if required_per_unit <= 0:
                return 0, 0, 0
            quantity = int(target_balance / required_per_unit)
            if quantity == 0:
                quantity = 1
            total_net = quantity * required_per_unit
            net_per_unit = unit_price
        else:
            return 0, 0, 0
        
        return quantity, net_per_unit, total_net
    
    def calculate_profit_percentage(self, steam_price: float, site_price: float,
                                    site: str, direction: str = "steam_to_cash") -> float:
        """Calculate profit/loss percentage"""
        if steam_price <= 0 or site_price <= 0:
            return 0
        
        if direction == "steam_to_cash":
            net_from_site = self.calculate_net_amount_steam_to_cash(site_price, site)
            if net_from_site <= 0:
                return -100
            profit_percentage = ((net_from_site - steam_price) / steam_price) * 100
            
        elif direction == "cash_to_steam":
            required_from_site = self.calculate_net_amount_cash_to_steam(steam_price, site)
            if required_from_site <= 0:
                return -100
            profit_percentage = ((steam_price - required_from_site) / required_from_site) * 100
        else:
            return 0
        
        return profit_percentage
    
    def update_site_commission(self, site: str, commission: float):
        """Update commission for a site"""
        self.site_commissions[site.lower()] = commission
        logger.info(f"{site} commission updated to {commission}%")
    
    def get_all_commissions(self) -> Dict[str, float]:
        """Get all commission rates"""
        return self.site_commissions.copy()
