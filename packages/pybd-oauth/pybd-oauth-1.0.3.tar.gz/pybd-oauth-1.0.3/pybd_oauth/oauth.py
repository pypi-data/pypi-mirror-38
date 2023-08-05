# -*- coding: utf-8 -*-

import urllib

import shortuuid
from pybd_base import BaseBaidu


class Oauth(BaseBaidu):
    def __init__(self):
        super(Oauth, self).__init__()
        # 引导用户完成授权获取code, Refer: https://xiongzhang.baidu.com/open/wiki/chapter2/section2.1.html?t=1540208308867
        self.BAIDU_OAUTH2_AUTHORIZE = self.OPENAPI + '/oauth/2.0/authorize?response_type=code&client_id={appid}&redirect_uri={redirect_uri}&scope={scope}&pass_no_login={pass_no_login}&state={state}'
        # 获取网页授权access_token, Refer: https://xiongzhang.baidu.com/open/wiki/chapter2/section2.2.html?t=1540208308867
        self.BAIDU_OAUTH2_ACCESS_TOKEN = self.OPENAPI + '/oauth/2.0/token?grant_type=authorization_code&code={code}&client_id={appid}&client_secret={secret}&redirect_uri={redirect_uri}'
        # 获取授权用户信息, Refer: https://xiongzhang.baidu.com/open/wiki/chapter2/section2.4.html?t=1540208308867
        self.BAIDU_OAUTH2_USERINFO = self.OPENAPI + '/rest/2.0/cambrian/sns/userinfo?access_token={access_token}&openid={openid}'

        # 引导用户完成授权获取code, Refer: https://xiongzhang.baidu.com/open/wiki/chapter5/section5.4.1.html?t=1540208308867
        self.BAIDU_COMPONENT_OAUTH2_AUTHORIZE = self.OPENAPI + '/oauth/2.0/authorize?response_type=code&client_id={appid}&redirect_uri={redirect_uri}&scope={scope}&tp_client_id={component_appid}&pass_no_login={pass_no_login}&state={state}'
        # 获取网页授权access_token, Refer: https://xiongzhang.baidu.com/open/wiki/chapter5/section5.4.2.html?t=1540208308867
        self.BAIDU_COMPONENT_OAUTH2_ACCESS_TOKEN = self.OPENAPI + '/oauth/2.0/token?grant_type=authorization_code&code={code}&client_id={appid}&tp_client_id={component_appid}&tp_access_token={component_access_token}&redirect_uri={redirect_uri}'
        # 拉取用户信息（需要scope为snsapi_userinfo）, Refer: https://xiongzhang.baidu.com/open/wiki/chapter5/section5.4.4.html?t=1540208308867
        self.BAIDU_COMPONENT_OAUTH2_USERINFO = self.OPENAPI + '/rest/2.0/cambrian/sns/userinfo?access_token={access_token}&openid={openid}'

    def get_oauth_code_url(self, appid=None, redirect_uri=None, scope='snsapi_base', redirect_url=None, pass_no_login=0, component=False, component_appid=None):
        if component:
            return self.get_component_oauth_code_url(appid=appid, redirect_uri=redirect_uri, scope=scope, redirect_url=redirect_url, component_appid=component_appid)
        return self.BAIDU_OAUTH2_AUTHORIZE.format(
            appid=appid,
            redirect_uri=urllib.quote_plus(redirect_uri),
            scope=scope,
            pass_no_login=pass_no_login,
            state=urllib.quote_plus(redirect_url),
        )

    def get_access_info(self, appid=None, secret=None, redirect_uri=None, code=None, component=False, component_appid=None, component_access_token=None):
        if component:
            return self.get_component_access_info(appid=appid, redirect_uri=redirect_uri, code=code, component_appid=component_appid, component_access_token=component_access_token)
        return self.get(self.BAIDU_OAUTH2_ACCESS_TOKEN, appid=appid, secret=secret, redirect_uri=urllib.quote_plus(redirect_uri), code=code)

    def get_userinfo(self, access_token=None, openid=None, component=False):
        if component:
            return self.get_component_userinfo(access_token=access_token, openid=openid)
        return self.get(self.BAIDU_OAUTH2_USERINFO, access_token=access_token, openid=openid)

    def get_component_oauth_code_url(self, appid=None, redirect_uri=None, scope='snsapi_base', redirect_url=None, pass_no_login=0, component_appid=None):
        return self.BAIDU_COMPONENT_OAUTH2_AUTHORIZE.format(
            appid=appid,
            redirect_uri=urllib.quote_plus(redirect_uri),
            scope=scope,
            pass_no_login=pass_no_login,
            state=urllib.quote_plus(redirect_url),
            component_appid=component_appid,
        )

    def get_component_access_info(self, appid=None, redirect_uri=None, code=None, component_appid=None, component_access_token=None):
        return self.get(self.BAIDU_COMPONENT_OAUTH2_ACCESS_TOKEN, appid=appid, code=code, component_appid=component_appid, component_access_token=component_access_token)

    def get_component_userinfo(self, access_token=None, openid=None):
        return self.get(self.BAIDU_COMPONENT_OAUTH2_USERINFO, access_token=access_token, openid=openid)

    def get_oauth_redirect_url(self, oauth_uri, scope='snsapi_base', redirect_url=None, default_url=None, direct_redirect=None, random_str=True):
        """
        # https://a.com/wx/oauth2?redirect_url=redirect_url
        # https://a.com/wx/oauth2?redirect_url=redirect_url&default_url=default_url
        # https://a.com/wx/oauth2?scope=snsapi_base&redirect_url=redirect_url
        # https://a.com/wx/oauth2?scope=snsapi_base&redirect_url=redirect_url&default_url=default_url
        # https://a.com/wx/oauth2?scope=snsapi_base&redirect_url=redirect_url&default_url=default_url&direct_redirect=true

        # https://a.com/wx/o?r=redirect_url
        # https://a.com/wx/o?r=redirect_url&d=default_url
        # https://a.com/wx/o?s=snsapi_base&r=redirect_url
        # https://a.com/wx/o?s=snsapi_base&r=redirect_url&d=default_url
        # https://a.com/wx/o?s=snsapi_base&r=redirect_url&d=default_url&dr=true
        """
        oauth_url = oauth_uri.format(scope, urllib.quote_plus(redirect_url), urllib.quote_plus(default_url)) if default_url else oauth_uri.format(scope, urllib.quote_plus(redirect_url))
        oauth_url = '{0}&dr=true'.format(oauth_url) if direct_redirect else oauth_url
        oauth_url = '{0}&rs={1}'.format(oauth_url, shortuuid.uuid()) if random_str else oauth_url
        return oauth_url


oauth = Oauth()
get_oauth_code_url = oauth.get_oauth_code_url
get_access_info = oauth.get_access_info
get_userinfo = oauth.get_userinfo
get_component_oauth_code_url = oauth.get_component_oauth_code_url
get_component_access_info = oauth.get_component_access_info
get_component_userinfo = oauth.get_component_userinfo
get_oauth_redirect_url = oauth.get_oauth_redirect_url
