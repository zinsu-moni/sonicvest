"""
GTR Pay Configuration File
Reads credentials from environment variables first, then falls back to test defaults.
"""

import os

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)


def _bool_env(name: str, default: bool) -> bool:
    value = (os.environ.get(name) or '').strip().lower()
    if not value:
        return default
    return value in ('1', 'true', 'yes', 'on')


GTR_CONFIG = {
    'MERCHANT_ID': os.environ.get('NEKPAY_MERCHANT_ID', '999300111'),
    'SECRET_KEY': os.environ.get('NEKPAY_SECRET_KEY', 'e8a4cdd0ccdb4d2b9ca6212453c5e40c'),
    'PAY_TYPE': os.environ.get('NEKPAY_PAY_TYPE', '520'),
    'BANK_CODE': os.environ.get('NEKPAY_BANK_CODE', 'NGR044'),
    'ENABLED': _bool_env('NEKPAY_ENABLED', True),
    'BASE_URL': os.environ.get('NEKPAY_BASE_URL', 'https://api.nekpayment.com/pay/web'),
}
