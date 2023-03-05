import requests
import json
from config import currency


class APIException(Exception):
    pass


class ModAmount:
    @staticmethod
    def mod_amount(amount):
        if ',' in amount:
            amount = amount.replace(',', '.')
            return amount
        else:
            return amount


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base and quote == base in currency.keys():
            raise APIException('Невозможно перевести одинаковые валюты.')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}". Проверьте список доступных валют.')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}". Проверьте список доступных валют.')

        try:
            amount = float(ModAmount.mod_amount(amount))
        except ValueError:
            raise APIException(f'Невозможно обработать количество "{amount}"!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        result = json.loads(r.content)[currency[base]]*amount

        return result
