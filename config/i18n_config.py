"""
i18n設定の一元管理
i18niceライブラリの標準使用法による実装
"""

import os
import i18n

def setup_i18n():
    """i18n設定の初期化"""
    # 翻訳ファイルのパス設定
    current_dir = os.path.dirname(os.path.abspath(__file__))
    locales_path = os.path.join(current_dir, '..', 'locales')
    
    # i18nの設定
    i18n.load_path.append(locales_path)
    i18n.set('file_format', 'json')
    i18n.set('fallback', 'ja')
    i18n.set('enable_memoization', True)
    
    # 環境変数から言語設定を取得
    locale = os.getenv('LANGUAGE', 'ja')
    if locale in ['ja', 'en']:
        i18n.set('locale', locale)
    else:
        i18n.set('locale', 'ja')  # デフォルトは日本語
    
    # デバッグモードの場合のみログ出力
    debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    if debug_mode:
        print(f"[i18n] Initialized with locale: {i18n.get('locale')}")
    
    # 翻訳データの手動ロード
    _load_translations(locales_path, locale, debug_mode)

def t(key: str, **kwargs) -> str:
    """翻訳のヘルパー関数"""
    try:
        return i18n.t(key, **kwargs)
    except Exception as e:
        print(f"[i18n] Translation error for key '{key}': {e}")
        return key  # キーをそのまま返す

def set_locale(locale: str):
    """言語設定を変更する"""
    if locale in ['ja', 'en']:
        i18n.set('locale', locale)
        print(f"[i18n] Locale changed to: {locale}")
    else:
        print(f"[i18n] Unsupported locale: {locale}. Using default 'ja'")
        i18n.set('locale', 'ja')

def get_locale() -> str:
    """現在の言語設定を取得する"""
    return i18n.get('locale')

def _load_translations(locales_path: str, locale: str, debug_mode: bool = False):
    """翻訳ファイルを手動でロード"""
    import json
    import glob
    
    # 現在のロケールの翻訳ファイルをロード
    locale_dir = os.path.join(locales_path, locale)
    if os.path.exists(locale_dir):
        json_files = glob.glob(os.path.join(locale_dir, '*.json'))
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    filename = os.path.basename(json_file).replace('.json', '')
                    
                    # 階層的にキーを展開して追加
                    _add_nested_translations(data, filename)
                    
                if debug_mode:
                    print(f"[i18n] Loaded {len(json_files)} translation files for locale '{locale}'")
            except Exception as e:
                if debug_mode:
                    print(f"[i18n] Error loading {json_file}: {e}")
    
    # フォールバックロケールもロード
    if locale != 'ja':
        fallback_dir = os.path.join(locales_path, 'ja')
        if os.path.exists(fallback_dir):
            json_files = glob.glob(os.path.join(fallback_dir, '*.json'))
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        filename = os.path.basename(json_file).replace('.json', '')
                        
                        # フォールバック用に'ja'ロケールで追加
                        _add_nested_translations(data, filename, fallback_locale='ja')
                        
                except Exception as e:
                    if debug_mode:
                        print(f"[i18n] Error loading fallback {json_file}: {e}")

def _add_nested_translations(data: dict, namespace: str, prefix: str = "", fallback_locale: str = None):
    """ネストされた翻訳データをi18nに追加"""
    target_locale = fallback_locale or i18n.get('locale')
    
    for key, value in data.items():
        full_key = f"{namespace}.{prefix}.{key}" if prefix else f"{namespace}.{key}"
        
        if isinstance(value, dict):
            # 再帰的にネストされたデータを処理
            _add_nested_translations(value, namespace, f"{prefix}.{key}" if prefix else key, fallback_locale)
        else:
            # 翻訳を追加
            i18n.add_translation(full_key, value, locale=target_locale)

# 初期化を手動で呼び出すため、自動実行はしない
# setup_i18n() は main.py で load_dotenv() 後に呼び出される