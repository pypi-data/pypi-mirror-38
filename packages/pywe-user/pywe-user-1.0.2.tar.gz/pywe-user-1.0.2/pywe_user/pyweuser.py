# -*- coding: utf-8 -*-

from pywe_token import BaseToken, final_access_token


class User(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(User, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        # 获取用户列表, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140840
        self.WECHAT_USER_GET = self.API_DOMAIN + '/cgi-bin/user/get?access_token={access_token}&next_openid={next_openid}'

    def get_users(self, appid=None, secret=None, token=None, storage=None, next_openid=''):
        """
        {
            "total": 2,
            "count": 2,
            "data": {
                "openid": ["OPENID1", "OPENID2"]
            },
            "next_openid": "NEXT_OPENID"
        }
        """
        return self.get(self.WECHAT_USER_GET, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage), next_openid=next_openid)

    def get_all_users(self, appid=None, secret=None, token=None, storage=None, users_func=None, authorizer_appid=None):
        goon = True
        next_openid = ''
        while goon:
            get_user_infos = self.get(self.WECHAT_USER_GET, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage), next_openid=next_openid)
            if users_func:
                users_func(authorizer_appid, get_user_infos)
            if get_user_infos.get('count') < 10000:
                goon = False
            next_openid = get_user_infos.get('next_openid', '')


user = User()
get_users = user.get_users
get_all_users = user.get_all_users
