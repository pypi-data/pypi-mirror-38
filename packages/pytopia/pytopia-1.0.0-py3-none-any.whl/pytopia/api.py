from typing import Dict, Optional

import requests
import hmac
import base64
import hashlib
import json
import time

from enum import Enum
from requests.compat import quote_plus
from requests.exceptions import RequestException


class TransactionType(Enum):
    DEPOSIT = 'Deposit'
    WITHDRAW = 'Withdraw'


class TradeType(Enum):
    BUY = 'Buy'
    SELL = 'Sell'


class CancelType(Enum):
    ALL = 'All'
    TRADE = 'Trade'
    TRADEPAIR = 'TradePair'


class CryptopiaAPIHandler:
    _private_key: str = None
    _public_key: str = None
    _base_url: str = "https://www.cryptopia.co.nz/api/"
    _public_url: str = "https://www.cryptopia.co.nz/api/public/"

    @classmethod
    def init(cls, public_key: str, private_key: str):
        CryptopiaAPIHandler._public_key = public_key
        CryptopiaAPIHandler._private_key = private_key

    @classmethod
    def _headers(cls, url: str, data: Dict) -> Dict:
        md5 = hashlib.md5()
        nonce = str(time.time())

        md5.update(data.encode('utf-8'))
        rcb64 = base64.b64encode(md5.digest()).decode('utf-8')
        request_signature = f'{cls._public_key}POST{quote_plus(url).lower()}{nonce}{rcb64}'

        hmac_signature = base64.b64encode(hmac.new(base64.b64decode(cls._private_key),
                                                   request_signature.encode('utf-8'),
                                                   hashlib.sha256).digest()).decode('utf-8')
        return {
            'Authorization': f'amx {cls._public_key}:{hmac_signature}:{nonce}',
            'Content-Type':  'application/json; charset=utf-8'
        }

    @classmethod
    def _post(cls, url: str, payload: Dict):
        payload = json.dumps(payload)
        response_data = None

        for _ in range(RETRIES):
            try:
                response_data = requests.post(url, headers=cls._headers(url, payload), data=payload).json()
            except json.JSONDecodeError:
                continue
            break

        if response_data.get('Success') and response_data.get('Success') is True:
            return response_data.get('Data')

        raise RequestException(response_data.get('Error'))

    @classmethod
    def _get(cls, url: str, query_params: Optional[Dict] = None):
        if query_params:
            for _,v in query_params.items():
                url += f'/{v}'

        response_data = requests.get(url).json()

        if not response_data:
            return None

        return response_data['Data']

    @classmethod
    def get_balances(cls, currency: str = None):
        return cls._post(f"{cls._base_url}GetBalance", {'Currency': currency if currency else ''})

    @classmethod
    def get_deposit_address(cls, currency: str):
        return cls._post(f"{cls._base_url}GetDepositAddress", {'Currency': currency})

    @classmethod
    def get_open_orders(cls, market: str, limit: Optional[int] = 100):
        return cls._post(f"{cls._base_url}GetOpenOrders", {'TradePairId': market, 'Count': limit})

    @classmethod
    def get_trade_history(cls, market: str, limit: Optional[int] = 100):
        return cls._post(f"{cls._base_url}TradeHistory", {'Market': market, 'Count': limit})

    @classmethod
    def get_transactions(cls, transaction_type: TransactionType, limit: Optional[int] = 100):
        return cls._post(f"{cls._base_url}GetTransactions", {'Type': transaction_type.value, 'limit': limit})

    @classmethod
    def submit_trade(cls, market, trade_type: TradeType, rate: float, amount: float):
        return cls._post(f"{cls._base_url}SubmitTrade", {'Market': market, 'Type': trade_type.value, 'Rate': rate,
                                                         'Amount': amount})

    @classmethod
    def cancel_trade(cls, cancel_type: CancelType, order_id: Optional[int] = None, trade_pair_id: Optional[int] = None):
        return cls._post(f"{cls._base_url}CancelTrade", {'Type': cancel_type.value,
                                                         'OrderId': order_id if order_id else '',
                                                         'TradePairId': trade_pair_id if trade_pair_id else ''})

    @classmethod
    def submit_tip(cls, currency: str, active_users: int, amount: float):
        return cls._post(f"{cls._base_url}SubmitTip", {'Currency': currency, 'ActiveUsers': active_users,
                                                       'Amount': amount})

    @classmethod
    def submit_withdraw(cls, currency: str, address: str, amount: float):
        return cls._post(f"{cls._base_url}SubmitWithdraw", {'Currency': currency, 'Address': address,
                                                            'amount': amount})

    @classmethod
    def get_currencies(cls):
        return cls._get(f"{cls._base_url}GetCurrencies")

    @classmethod
    def get_trade_pairs(cls):
        return cls._get(f"{cls._base_url}GetTradePairs")

    @classmethod
    def get_markets(cls, base_market: Optional[str] = 'All', hours: Optional[int] = 24):
        return cls._get(f"{cls._base_url}GetMarkets", {'baseMarket': base_market, 'hours': hours})

    @classmethod
    def get_market(cls, market: str, hours: Optional[int] = 24):
        return cls._get(f"{cls._base_url}GetMarket", {'market': market, 'hours': hours})

    @classmethod
    def get_market_history(cls, market: str, hours: Optional[int] = 24):
        return cls._get(f"{cls._base_url}GetMarketHistory", {'market': market, 'hours': hours})

    @classmethod
    def get_market_orders(cls, market: str, order_count: Optional[int] = 100):
        return cls._get(f"{cls._base_url}GetMarketOrders", {'market': market, 'orderCount': order_count})

    @classmethod
    def get_market_order_groups(cls, markets: Optional[str] = 'All', order_count: Optional[int] = 100):
        return cls._get(f"{cls._base_url}GetMarketOrderGroups", {'markets': markets, 'orderCount': order_count})
