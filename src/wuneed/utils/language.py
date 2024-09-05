from typing import Dict, Any
import json
import os
from wuneed.utils.logger import setup_logger

logger = setup_logger('language_manager', 'logs/language_manager.log')

class LanguageManager:
    def __init__(self):
        self.current_language = "en"
        self.translations: Dict[str, Dict[str, str]] = {}
        self.language_specific_features: Dict[str, Any] = {}
        self.load_translations()
        self.load_language_specific_features()

    def load_translations(self):
        lang_dir = os.path.join(os.path.dirname(__file__), "..", "languages")
        for filename in os.listdir(lang_dir):
            if filename.endswith(".json"):
                lang_code = filename[:-5]
                with open(os.path.join(lang_dir, filename), "r") as f:
                    self.translations[lang_code] = json.load(f)

    def load_language_specific_features(self):
        features_dir = os.path.join(os.path.dirname(__file__), "..", "language_features")
        for filename in os.listdir(features_dir):
            if filename.endswith(".py"):
                lang_code = filename[:-3]
                module = __import__(f"wuneed.language_features.{lang_code}", fromlist=['features'])
                self.language_specific_features[lang_code] = module.features

    def set_language(self, lang_code: str):
        if lang_code in self.translations:
            self.current_language = lang_code
            logger.info(f"Language set to: {lang_code}")
        else:
            raise ValueError(f"Unsupported language: {lang_code}")

    def get_text(self, key: str) -> str:
        return self.translations.get(self.current_language, {}).get(key, key)

    def get_language_feature(self, feature_name: str) -> Any:
        return self.language_specific_features.get(self.current_language, {}).get(feature_name)

language_manager = LanguageManager()