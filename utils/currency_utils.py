"""
Currency Utility Module
Handles currency formatting and configuration
"""
import os
from typing import Dict, Any


class CurrencyFormatter:
    """Currency formatting utility"""
    
    # Currency symbols and formatting
    CURRENCY_SYMBOLS = {
        "USD": "$",
        "JPY": "¥",
        "EUR": "€",
        "GBP": "£"
    }
    
    # Default daily rates (can be overridden by environment)
    DEFAULT_DAILY_RATES = {
        "USD": 500,
        "JPY": 50000,
        "EUR": 450,
        "GBP": 400
    }
    
    def __init__(self):
        self.currency = os.getenv("CURRENCY", "USD").upper()
        self.daily_rate = float(os.getenv("DAILY_RATE", str(self.DEFAULT_DAILY_RATES.get(self.currency, 500))))
        self.tax_rate = float(os.getenv("TAX_RATE", "0.10"))
    
    def get_currency_symbol(self) -> str:
        """Get currency symbol for current currency"""
        return self.CURRENCY_SYMBOLS.get(self.currency, self.currency)
    
    def format_amount(self, amount: float) -> str:
        """Format amount with currency symbol"""
        symbol = self.get_currency_symbol()
        if self.currency == "JPY":
            # JPY doesn't use decimal places
            return f"{symbol}{int(amount):,}"
        else:
            # Other currencies use 2 decimal places
            return f"{symbol}{amount:,.2f}"
    
    def get_daily_rate(self) -> float:
        """Get daily rate for current currency"""
        return self.daily_rate
    
    def get_currency_code(self) -> str:
        """Get currency code"""
        return self.currency
    
    def calculate_cost(self, effort_days: float) -> float:
        """Calculate cost based on effort and daily rate"""
        return effort_days * self.daily_rate
    
    def calculate_tax(self, subtotal: float) -> float:
        """Calculate tax amount"""
        return subtotal * self.tax_rate
    
    def calculate_total(self, subtotal: float) -> float:
        """Calculate total including tax"""
        return subtotal + self.calculate_tax(subtotal)
    
    def get_currency_info(self) -> Dict[str, Any]:
        """Get complete currency configuration info"""
        return {
            "currency": self.currency,
            "symbol": self.get_currency_symbol(),
            "daily_rate": self.daily_rate,
            "tax_rate": self.tax_rate
        }


# Global instance
currency_formatter = CurrencyFormatter()