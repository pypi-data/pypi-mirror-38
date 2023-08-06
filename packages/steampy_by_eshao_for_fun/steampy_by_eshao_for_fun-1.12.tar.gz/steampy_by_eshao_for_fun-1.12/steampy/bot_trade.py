import time

from steampy.client import SteamClient, Asset
import json


class BotTrade:
    def __init__(self, col):
        self.user = col['username']
        self.psw = col['password']
        self.apikey = col['dev_key']
        self.config = col.get('configs')
        self.guard_info = {
            "steamid": str(col['steam_id']),
            "shared_secret": col['configs']['shared_secret'],
            "identity_secret": col['configs']['identity_secret'],
        }
        self.steam_client = SteamClient(self.apikey, self.user, self.guard_info, self.config)
        if not self.steam_client.was_login_executed:
            self.steam_client.login(self.user, self.psw, json.dumps(self.guard_info))

    def send_all_items(self, trade_url, max_for_offer=300):
        my_asset_list = self.get_all_tradable_assetid()
        while my_asset_list:
            send_asset_list = my_asset_list[:max_for_offer]
            del my_asset_list[:max_for_offer]
            resp_dict = self.steam_client.make_offer_with_url(send_asset_list, [], trade_url, '')
            print(resp_dict)
            yield resp_dict['tradeofferid']

    def send_all_items_to_many(self, trade_url_list):
        my_asset_list = self.get_all_tradable_assetid()
        count = len(my_asset_list) // len(trade_url_list)  # 整除
        for index, value in enumerate(trade_url_list):
            if index == len(trade_url_list) - 1:
                data = my_asset_list[count * index:]
            else:
                data = my_asset_list[count * index:count * (index + 1)]
            resp_dict = self.steam_client.make_offer_with_url(data, [], value, '')
            yield (value, resp_dict['tradeofferid'])

    def accept(self, trade_offer_id, allow_2fa=False):
        resp = self.steam_client.accept_trade_offer(trade_offer_id, allow_2fa)
        offer_status = self.steam_client.get_trade_offer(trade_offer_id)['response']['offer']['trade_offer_state']
        result = dict(trade_offer_id=trade_offer_id, response=resp, status_code=offer_status)
        print('Accept trade', result)

        if offer_status != 3:
            time.sleep(5)
            offer_status = self.steam_client.get_trade_offer(trade_offer_id)['response']['offer']['trade_offer_state']
            print(offer_status)

    def get_all_tradable_assetid(self):
        my_items = self.steam_client.get_inventory_asset()
        my_asset_list = []
        for i in my_items:
            if i['tradable'] == 1:
                my_asset_list.append(Asset(i['assetid']))
        return my_asset_list
