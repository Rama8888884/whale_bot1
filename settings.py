import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class ParserBase:
    def __init__(self, response: Dict[str, Any], keys: Optional[List[str]] = None):
        self.response = response
        self.keys = keys or []
        self.errors = {}

    def is_response_valid(self) -> bool:
        if 'result' not in self.response or self.response['result'] != 'success':
            self.errors['result'] = "Invalid response from Whale Alert API."
            return False
        return True

    @staticmethod
    def format_dict_to_text(dictionary: Dict[str, Any]) -> str:
        return '\n'.join(f'{key}: {value}' for key, value in dictionary.items())

    def clean_response(self, result_dict: Dict[str, Any]) -> Dict[str, Any]:
        return {key: result_dict.get(key, 'N/A') for key in self.keys}

    def parse_response(self) -> Optional[str]:
        if not self.is_response_valid():
            return None
        return self.format_dict_to_text(self.response)

class TransactionsDetailParser(ParserBase):
    items_key = 'transactions'

# You must set your real Telegram Bot token and Whale Alert API key here or load from env
TELEGRAM_BOT_KEY = "7731939573:AAGrYuXA3vu00bb>N tiX pDkAIM×g-cg9_W"
BOT_TOKEN = 7731939573:AAGrYuXA3vu00bb>N tiX pDkAIM×g-cg9_W  # Used in your webhook route