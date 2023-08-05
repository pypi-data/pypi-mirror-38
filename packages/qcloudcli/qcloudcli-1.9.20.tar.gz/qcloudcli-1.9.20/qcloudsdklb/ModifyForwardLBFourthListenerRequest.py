# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class ModifyForwardLBFourthListenerRequest(Request):

    def __init__(self):
        super(ModifyForwardLBFourthListenerRequest, self).__init__(
            'lb', 'qcloudcliV1', 'ModifyForwardLBFourthListener', 'lb.api.qcloud.com')

    def get_SSLMode(self):
        return self.get_params().get('SSLMode')

    def set_SSLMode(self, SSLMode):
        self.add_param('SSLMode', SSLMode)

    def get_certCaContent(self):
        return self.get_params().get('certCaContent')

    def set_certCaContent(self, certCaContent):
        self.add_param('certCaContent', certCaContent)

    def get_certCaId(self):
        return self.get_params().get('certCaId')

    def set_certCaId(self, certCaId):
        self.add_param('certCaId', certCaId)

    def get_certCaName(self):
        return self.get_params().get('certCaName')

    def set_certCaName(self, certCaName):
        self.add_param('certCaName', certCaName)

    def get_certContent(self):
        return self.get_params().get('certContent')

    def set_certContent(self, certContent):
        self.add_param('certContent', certContent)

    def get_certId(self):
        return self.get_params().get('certId')

    def set_certId(self, certId):
        self.add_param('certId', certId)

    def get_certKey(self):
        return self.get_params().get('certKey')

    def set_certKey(self, certKey):
        self.add_param('certKey', certKey)

    def get_certName(self):
        return self.get_params().get('certName')

    def set_certName(self, certName):
        self.add_param('certName', certName)

    def get_healthNum(self):
        return self.get_params().get('healthNum')

    def set_healthNum(self, healthNum):
        self.add_param('healthNum', healthNum)

    def get_healthSwitch(self):
        return self.get_params().get('healthSwitch')

    def set_healthSwitch(self, healthSwitch):
        self.add_param('healthSwitch', healthSwitch)

    def get_intervalTime(self):
        return self.get_params().get('intervalTime')

    def set_intervalTime(self, intervalTime):
        self.add_param('intervalTime', intervalTime)

    def get_listenerId(self):
        return self.get_params().get('listenerId')

    def set_listenerId(self, listenerId):
        self.add_param('listenerId', listenerId)

    def get_listenerName(self):
        return self.get_params().get('listenerName')

    def set_listenerName(self, listenerName):
        self.add_param('listenerName', listenerName)

    def get_loadBalancerId(self):
        return self.get_params().get('loadBalancerId')

    def set_loadBalancerId(self, loadBalancerId):
        self.add_param('loadBalancerId', loadBalancerId)

    def get_scheduler(self):
        return self.get_params().get('scheduler')

    def set_scheduler(self, scheduler):
        self.add_param('scheduler', scheduler)

    def get_sessionExpire(self):
        return self.get_params().get('sessionExpire')

    def set_sessionExpire(self, sessionExpire):
        self.add_param('sessionExpire', sessionExpire)

    def get_timeOut(self):
        return self.get_params().get('timeOut')

    def set_timeOut(self, timeOut):
        self.add_param('timeOut', timeOut)

    def get_unhealthNum(self):
        return self.get_params().get('unhealthNum')

    def set_unhealthNum(self, unhealthNum):
        self.add_param('unhealthNum', unhealthNum)
