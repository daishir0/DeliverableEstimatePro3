"""
Centralized i18n Configuration Management
Implementation using standard i18nice library usage
"""

import os
import i18n

def setup_i18n():
    """Initialize i18n configuration"""
    # Set translation file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    locales_path = os.path.join(current_dir, '..', 'locales')
    
    # Configure i18n
    i18n.load_path.append(locales_path)
    i18n.set('file_format', 'json')
    i18n.set('fallback', 'ja')
    i18n.set('enable_memoization', True)
    
    # Get language setting from environment variable
    locale = os.getenv('LANGUAGE', 'ja')
    if locale in ['ja', 'en']:
        i18n.set('locale', locale)
    else:
        i18n.set('locale', 'ja')  # Default is Japanese
    
    # Output logs only in debug mode
    debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    if debug_mode:
        print(f"[i18n] Initialized with locale: {i18n.get('locale')}")
    
    # Manual loading of translation data
    _load_translations(locales_path, locale, debug_mode)

def t(key: str, **kwargs) -> str:
    """Translation helper function"""
    try:
        return i18n.t(key, **kwargs)
    except Exception as e:
        print(f"[i18n] Translation error for key '{key}': {e}")
        return key  # Return the key as-is

def set_locale(locale: str):
    """Change language setting"""
    if locale in ['ja', 'en']:
        i18n.set('locale', locale)
        print(f"[i18n] Locale changed to: {locale}")
    else:
        print(f"[i18n] Unsupported locale: {locale}. Using default 'ja'")
        i18n.set('locale', 'ja')

def get_locale() -> str:
    """Get current language setting"""
    return i18n.get('locale')

def _load_translations(locales_path: str, locale: str, debug_mode: bool = False):
    """Manually load translation files"""
    import json
    import glob
    
    # Load translation files for current locale
    locale_dir = os.path.join(locales_path, locale)
    if os.path.exists(locale_dir):
        json_files = glob.glob(os.path.join(locale_dir, '*.json'))
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    filename = os.path.basename(json_file).replace('.json', '')
                    
                    # Add by expanding keys hierarchically
                    _add_nested_translations(data, filename)
                    
                if debug_mode:
                    print(f"[i18n] Loaded {len(json_files)} translation files for locale '{locale}'")
            except Exception as e:
                if debug_mode:
                    print(f"[i18n] Error loading {json_file}: {e}")
    
    # Also load fallback locale
    if locale != 'ja':
        fallback_dir = os.path.join(locales_path, 'ja')
        if os.path.exists(fallback_dir):
            json_files = glob.glob(os.path.join(fallback_dir, '*.json'))
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        filename = os.path.basename(json_file).replace('.json', '')
                        
                        # Add with 'ja' locale for fallback
                        _add_nested_translations(data, filename, fallback_locale='ja')
                        
                except Exception as e:
                    if debug_mode:
                        print(f"[i18n] Error loading fallback {json_file}: {e}")

def _add_nested_translations(data: dict, namespace: str, prefix: str = "", fallback_locale: str = None):
    """Add nested translation data to i18n"""
    target_locale = fallback_locale or i18n.get('locale')
    
    for key, value in data.items():
        full_key = f"{namespace}.{prefix}.{key}" if prefix else f"{namespace}.{key}"
        
        if isinstance(value, dict):
            # Process nested data recursively
            _add_nested_translations(value, namespace, f"{prefix}.{key}" if prefix else key, fallback_locale)
        else:
            # Add translation
            i18n.add_translation(full_key, value, locale=target_locale)

# No automatic execution as initialization is called manually
# setup_i18n() is called in main.py after load_dotenv()