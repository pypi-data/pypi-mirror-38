import hashlib
import hmac
import base64
from dotenv import load_dotenv, find_dotenv
import requests
from datetime import datetime
import os

load_dotenv(find_dotenv())

general_api = 'https://jsapi.settle.finance/api'
price_api = 'https://dbapi.settle.finance/api'
chat_api = 'https://chat.settle.finance/v1/api'


class _SettleBase:
    def __init__(self, api, api_key=None, api_secret=None):
        self.__api_key = os.getenv("SETTLE_API_KEY") if api_key is None else api_key
        self.__api_secret = os.getenv("SETTLE_API_SECRET") if api_secret is None else api_secret
        self.__access_key = None
        self.__signature = None
        self.__api = api if os.getenv("ENVIRONMENT") != 'development' else 'https://localhost:3005'

    def __generate_url(self, endpoint):
        if endpoint[0] != '/':
            endpoint = "{}/{}".format(self.__api, endpoint)
        else:
            endpoint = "{}{}".format(self.__api, endpoint)

        return endpoint

    def __get_access_key(self):
        r = requests.get(
            self.__generate_url('app/AccessToken'),
             headers={'X-Api-Key': self.__api_key}
        )

        self.__access_key_time = datetime.now()
        self.__access_key = r.json()['accessToken']

        return self.__access_key

    def __get_signature(self):
        return base64.b64encode(
            hmac.new(
                bytes(self.__api_secret.encode('utf-8')),
                bytes(self.__access_key.encode('utf-8')),
                digestmod=hashlib.sha256).digest()).decode()

    def __get_request_header(self):
            return {
                'X-Api-Key': self.__api_key,
                'X-Access-Token': self.__get_access_key(),
                'X-Api-Signature': self.__get_signature()
            }

    def __generate_request(self, endpoint, params={}):
        return requests.get(
            self.__generate_url(endpoint),
            params=params,
            headers=self.__get_request_header()
        )



class PriceList(_SettleBase):
    def __init__(self):
        _SettleBase.__init__(self, price_api)

    def price_history(self, params={}, include_response=False):
        r = super(PriceList, self)._SettleBase__generate_request('/public/price-history', params)
        data = r.json()
        return data if not include_response else (data, r)


    def info(self, params={}, include_response=False):
        r = super(PriceList, self)._SettleBase__generate_request('/public/info', params)
        data = r.json()
        return data if not include_response else (data, r)

    def ticker(self, params={}, include_response=False):
        r = super(PriceList, self)._SettleBase__generate_request('/public/ticker', params)
        data = r.json()
        return data if not include_response else (data, r)


class Portfolio(_SettleBase):
    def __init__(self):
        _SettleBase.__init__(self, general_api)

    def summary(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/Summary', params)
        data = r.json()
        return data if not include_response else (data, r)

    def holdings(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/Holdings', params)
        data = r.json()
        return data if not include_response else (data, r)

    def holdings_with_trades(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/HoldingsWithTrades', params)
        data = r.json()
        return data if not include_response else (data, r)

    def trades(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/Trades', params)
        data = r.json()
        return data if not include_response else (data, r)

    def exchanges(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/Exchanges', params)
        data = r.json()
        return data if not include_response else (data, r)

    def balance_history(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/BalanceHistory', params)
        data = r.json()
        return data if not include_response else (data, r)


class Users(_SettleBase):
    def __init__(self):
        _SettleBase.__init__(self, general_api)
        pass

    def guid_to_username(self, params={}, include_response=False):
        r = super(Users, self)._SettleBase__generate_request('/app/GuidToUsername', params)
        data = r.json()
        return data if not include_response else (data, r)

    def exchange_token_for_guid(self, params={}, include_response=False):
        r = super(Users, self)._SettleBase__generate_request('/app/', params)
        data = r.json()
        return data if not include_response else (data, r)


class Chat(_SettleBase):
    def __init__(self):
        _SettleBase.__init__(self, chat_api)
        pass

    def send_event(self, params={}, include_response=False):
        r = super(Chat, self)._SettleBase__generate_request('/app/event', params)
        data = r.content.decode('utf-8')
        return data if not include_response else (data, r)


class App(_SettleBase):
    def __init__(self):
        _SettleBase.__init__(self, general_api)

    def users(self, params={}, include_response=False):
        r = super(App, self)._SettleBase__generate_request('/app/Users', params)
        data = r.json()
        return data if not include_response else (data, r)

    def send_notification(self, params={}, include_response=False):
        r = super(App, self)._SettleBase__generate_request('/app/SendNotification', params)
        data = r.content.decode('utf-8')
        return data if not include_response else (data, r)



