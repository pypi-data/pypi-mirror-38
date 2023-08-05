# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class BindBmL4ListenerRsRequest(Request):

    def __init__(self):
        super(BindBmL4ListenerRsRequest, self).__init__(
            'bmlb', 'qcloudcliV1', 'BindBmL4ListenerRs', 'bmlb.api.qcloud.com')

    def get_backends(self):
        return self.get_params().get('backends')

    def set_backends(self, backends):
        self.add_param('backends', backends)

    def get_bindType(self):
        return self.get_params().get('bindType')

    def set_bindType(self, bindType):
        self.add_param('bindType', bindType)

    def get_listenerId(self):
        return self.get_params().get('listenerId')

    def set_listenerId(self, listenerId):
        self.add_param('listenerId', listenerId)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)
