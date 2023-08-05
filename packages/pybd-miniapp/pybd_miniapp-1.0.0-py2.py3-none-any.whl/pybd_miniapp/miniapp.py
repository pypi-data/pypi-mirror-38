# -*- coding: utf-8 -*-

from pybd_base import BaseBaidu
from pybd_decrypt import decrypt
from pywe_storage import MemoryStorage


class MiniApp(BaseBaidu):
    def __init__(self, appid=None, secret=None, storage=None):
        super(MiniApp, self).__init__()
        self.appid = appid
        self.secret = secret
        self.storage = storage or MemoryStorage()
        # https://smartprogram.baidu.com/docs/develop/api/open_log/
        self.getSessionKeyByCode = self.OPENAPI + '/nalogin/getSessionKeyByCode'

    def sessionKey(self, unid=None):
        # https://developers.weixin.qq.com/community/develop/doc/00088a409fc308b765475fa4351000?highLine=session_key
        # sessionKey 非共用
        return '{0}:{1}:sessionKey'.format(self.appid, unid or '')

    def update_params(self, appid=None, secret=None, storage=None):
        self.appid = appid or self.appid
        self.secret = secret or self.secret
        self.storage = storage or self.storage

    def store_session_key(self, appid=None, secret=None, session_key=None, unid=None, storage=None):
        # Update params
        self.update_params(appid=appid, secret=secret, storage=storage)
        # Store sessionKey
        if session_key and unid:
            return self.storage.set(self.sessionKey(unid=unid), session_key)
        return False

    def get_session_info(self, appid=None, secret=None, code=None, unid=None, storage=None):
        """
        # curl -d "code=xxx&client_id=xxx&sk=xxx" https://openapi.baidu.com/nalogin/getSessionKeyByCode
        {
            "openid": "ABCDEFG123",
            "session_key": "xxxxxx"
        }
        """
        # Update params
        self.update_params(appid=appid, secret=secret, storage=storage)
        # Fetch sessionInfo
        session_info = self.post(
            self.getSessionKeyByCode,
            data_to_json_str=False,
            data={
                'client_id': self.appid,
                'sk': self.secret,
                'code': code,
            }
        ) if code else {}
        # Store sessionKey
        if session_info and unid:
            self.storage.set(self.sessionKey(unid=unid), session_info.get('session_key', ''))
        return session_info

    def get_session_key(self, appid=None, secret=None, code=None, unid=None, storage=None):
        # Update params
        self.update_params(appid=appid, secret=secret, storage=storage)
        # Fetch sessionKey
        # From storage
        session_key = '' if code or not unid else self.storage.get(self.sessionKey(unid=unid))
        # From request api
        if not session_key:
            session_key = self.get_session_info(appid=self.appid, secret=self.secret, code=code, storage=self.storage).get('session_key', '')
        return session_key

    def get_userinfo(self, appid=None, secret=None, code=None, unid=None, session_key=None, encryptedData=None, iv=None, storage=None):
        """
        {
            u'headimgurl': u'https://himg.bdimg.com/sys/portrait/item/ea8348514d4953970a',
            u'nickname': u'HQMIS',
            u'openid': u'mgJNc4Ut1tzE1L1ltQCCBWCZ9L',
            u'sex': 1
        }
        """
        # Update params
        self.update_params(appid=appid, secret=secret, storage=storage)
        # If not encryptedData return session_info
        if not encryptedData:
            return self.get_session_info(appid=self.appid, secret=self.secret, code=code, unid=unid, storage=self.storage)
        # Update sessionKey
        if not session_key:
            session_key = self.get_session_key(appid=self.appid, secret=self.secret, code=code, unid=unid, storage=self.storage)
        return decrypt(sessionKey=session_key, encryptedData=encryptedData, iv=iv)


miniapp = MiniApp()
store_session_key = miniapp.store_session_key
get_session_info = miniapp.get_session_info
get_session_key = miniapp.get_session_key
get_userinfo = miniapp.get_userinfo
