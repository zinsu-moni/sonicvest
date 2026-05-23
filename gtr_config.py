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


def _float_env(name: str, default: float) -> float:
    value = (os.environ.get(name) or '').strip()
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        return default


GTR_CONFIG = {
    'MERCHANT_ID': os.environ.get('NEKPAY_MERCHANT_ID', '999300111'),
    'SECRET_KEY': os.environ.get('NEKPAY_SECRET_KEY', 'e8a4cdd0ccdb4d2b9ca6212453c5e40c'),
    'PAY_TYPE': os.environ.get('NEKPAY_PAY_TYPE', '520'),
    'BANK_CODE': os.environ.get('NEKPAY_BANK_CODE', 'NGR044'),
    'ENABLED': _bool_env('NEKPAY_ENABLED', True),
    'BASE_URL': os.environ.get('NEKPAY_BASE_URL', 'https://api.nekpayment.com/pay/web'),
    'VERIFY_BASE_URL': os.environ.get('NEKPAY_VERIFY_BASE_URL', '').strip() or None,
    'REQUEST_TIMEOUT': _float_env('NEKPAY_REQUEST_TIMEOUT', 12.0),
    'MIN_AMOUNT': _float_env('NEKPAY_MIN_AMOUNT', 500.0),
    'MAX_AMOUNT': _float_env('NEKPAY_MAX_AMOUNT', 10000000.0),
    'TRANSFER_SECRET_KEY': os.environ.get('NEKPAY_TRANSFER_SECRET_KEY', os.environ.get('NEKPAY_SECRET_KEY', 'e8a4cdd0ccdb4d2b9ca6212453c5e40c')),
    'TRANSFER_BASE_URL': os.environ.get('NEKPAY_TRANSFER_BASE_URL', 'https://api.nekpayment.com/pay/transfer'),
    'TRANSFER_REQUEST_TIMEOUT': _float_env('NEKPAY_TRANSFER_REQUEST_TIMEOUT', 12.0),
    'TRANSFER_MIN_AMOUNT': _float_env('NEKPAY_TRANSFER_MIN_AMOUNT', 1.0),
    'TRANSFER_MAX_AMOUNT': _float_env('NEKPAY_TRANSFER_MAX_AMOUNT', 100.0),
}
