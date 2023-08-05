# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class CreateDsaHostRequest(Request):

    def __init__(self):
        super(CreateDsaHostRequest, self).__init__(
            'dsa', 'qcloudcliV1', 'CreateDsaHost', 'dsa.api.qcloud.com')

    def get_area(self):
        return self.get_params().get('area')

    def set_area(self, area):
        self.add_param('area', area)

    def get_backupOrigin(self):
        return self.get_params().get('backupOrigin')

    def set_backupOrigin(self, backupOrigin):
        self.add_param('backupOrigin', backupOrigin)

    def get_host(self):
        return self.get_params().get('host')

    def set_host(self, host):
        self.add_param('host', host)

    def get_https(self):
        return self.get_params().get('https')

    def set_https(self, https):
        self.add_param('https', https)

    def get_ipAccess(self):
        return self.get_params().get('ipAccess')

    def set_ipAccess(self, ipAccess):
        self.add_param('ipAccess', ipAccess)

    def get_ipFreqLimit(self):
        return self.get_params().get('ipFreqLimit')

    def set_ipFreqLimit(self, ipFreqLimit):
        self.add_param('ipFreqLimit', ipFreqLimit)

    def get_origin(self):
        return self.get_params().get('origin')

    def set_origin(self, origin):
        self.add_param('origin', origin)

    def get_projectId(self):
        return self.get_params().get('projectId')

    def set_projectId(self, projectId):
        self.add_param('projectId', projectId)

    def get_rspHeader(self):
        return self.get_params().get('rspHeader')

    def set_rspHeader(self, rspHeader):
        self.add_param('rspHeader', rspHeader)

    def get_strategyWeight(self):
        return self.get_params().get('strategyWeight')

    def set_strategyWeight(self, strategyWeight):
        self.add_param('strategyWeight', strategyWeight)
