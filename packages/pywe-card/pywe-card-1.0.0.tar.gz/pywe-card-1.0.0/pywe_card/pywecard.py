# -*- coding: utf-8 -*-

from pywe_token import BaseToken, final_access_token


class Card(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(Card, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        # 创建会员卡, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1451025283
        self.WECHAT_CARD_CREATE = self.API_DOMAIN + '/card/create?access_token={access_token}'
        # 管理会员卡, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1466494654_K9rNz
        self.WECHAT_CARD_UPDATE = self.API_DOMAIN + '/card/update?access_token={access_token}'

    def create(self, data, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_CARD_CREATE.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data=data,
        )

    def update(self, data, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_CARD_UPDATE.format(access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)),
            data=data,
        )


card = Card()
card_create = card.create
card_update = card.update
