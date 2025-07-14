"""
Internationalization (i18n) Utilities - i18nice Standard Implementation
"""

# Import to new standard implementation
from config.i18n_config import t, set_locale, get_locale

# Wrapper class for backward compatibility (for gradual migration)
class I18nUtils:
    """Wrapper class for backward compatibility (deprecated)"""
    
    def __init__(self):
        print("[WARNING] I18nUtils class is deprecated. Use 'from config.i18n_config import t' instead.")
    
    def t(self, key: str, **kwargs) -> str:
        """Get translation (deprecated)"""
        return t(key, **kwargs)
    
    def set_locale(self, locale: str):
        """Change language setting (deprecated)"""
        set_locale(locale)
    
    def get_locale(self) -> str:
        """Get current language setting (deprecated)"""
        return get_locale()

# Singleton instance for backward compatibility (deprecated)
i18n_utils = I18nUtils()

# Recommended: Use new API directly
# from config.i18n_config import t, set_locale, get_locale