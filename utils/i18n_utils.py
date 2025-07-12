"""
国際化（i18n）ユーティリティ - i18nice標準実装
"""

# 新しい標準実装へのインポート
from config.i18n_config import t, set_locale, get_locale

# 後方互換性のためのラッパークラス（段階的移行用）
class I18nUtils:
    """後方互換性のためのラッパークラス（非推奨）"""
    
    def __init__(self):
        print("[WARNING] I18nUtils class is deprecated. Use 'from config.i18n_config import t' instead.")
    
    def t(self, key: str, **kwargs) -> str:
        """翻訳を取得する（非推奨）"""
        return t(key, **kwargs)
    
    def set_locale(self, locale: str):
        """言語設定を変更する（非推奨）"""
        set_locale(locale)
    
    def get_locale(self) -> str:
        """現在の言語設定を取得する（非推奨）"""
        return get_locale()

# 後方互換性のためのシングルトンインスタンス（非推奨）
i18n_utils = I18nUtils()

# 推奨：新しいAPIを直接使用
# from config.i18n_config import t, set_locale, get_locale