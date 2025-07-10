"""
国際化（i18n）ユーティリティ
"""

import os
import i18n
from typing import Dict, Any

class I18nUtils:
    """国際化（i18n）ユーティリティクラス"""
    
    def __init__(self):
        # i18nの設定
        i18n.load_path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locales'))
        i18n.set('filename_format', '{locale}.{format}')
        i18n.set('file_format', 'json')
        i18n.set('skip_locale_root_data', True)
        i18n.set('fallback', 'ja')  # デフォルトは日本語
        
        # 環境変数から言語設定を取得
        self.set_locale(os.getenv("LANGUAGE", "ja"))
    
    def set_locale(self, locale: str):
        """言語設定を変更する"""
        if locale in ["ja", "en"]:
            i18n.set('locale', locale)
        else:
            i18n.set('locale', "ja")  # 不明な言語の場合はデフォルト（日本語）
    
    def get_locale(self) -> str:
        """現在の言語設定を取得する"""
        return i18n.get('locale')
    
    def t(self, key: str, **kwargs) -> str:
        """翻訳を取得する"""
        return i18n.t(key, **kwargs)
    
    def translate_dict(self, data: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """辞書内の文字列を翻訳する（キーにprefixを付けて翻訳キーとする）"""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                trans_key = f"{prefix}.{key}" if prefix else key
                result[key] = i18n.t(trans_key, default=value)
            elif isinstance(value, dict):
                new_prefix = f"{prefix}.{key}" if prefix else key
                result[key] = self.translate_dict(value, new_prefix)
            elif isinstance(value, list):
                result[key] = [
                    self.translate_dict(item, f"{prefix}.{key}.item") if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result

# シングルトンインスタンス
i18n_utils = I18nUtils()