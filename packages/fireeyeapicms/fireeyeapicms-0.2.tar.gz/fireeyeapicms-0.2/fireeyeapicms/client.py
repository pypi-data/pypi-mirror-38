from __future__ import unicode_literals
from __future__ import print_function

import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)


class FireClient:

    def __init__(self,username,password,server,verify=True):
        self.username=username
        self.password=password
        self.server=server[:-1] if server[-1]=="/" else server
        self.login_url = self.server+"/login/login"
        self.session = requests.session()
        self.verify=verify
        self.initiate()


    def initiate(self):
        r = self.session.request("GET",self.login_url,verify=self.verify)
        if r.status_code != requests.codes.ok:
            raise RuntimeError('Error %d (%s)' % (r.status_code,r.reason))
        data={"auth_method":"password",
              "data":{
                  "username":self.username,
                  "password":self.password}}
        ok_codes=[200,203]
        import json
        r = self.session.request("POST",self.login_url,verify=self.verify,json=data)
        if r.status_code not in ok_codes:
            raise RuntimeError('Error %d (%s)' % (r.status_code,r.reason))

    def req(self,method,url,data,ok_codes,params=None):
        """

        :param method:
        :param url:
        :param data:
        :param ok_codes:
        :return:
        """

        try:
            if self.session:
                r = self.session.request(method,url,verify=self.verify,json=data,params=params)
                if r.status_code not in ok_codes:
                    raise RuntimeError('Error %d (%s)' % (r.status_code,r.reason))
            else:
                raise RuntimeError("Session not initialized")
        except InsecureRequestWarning:
            pass
        return r

