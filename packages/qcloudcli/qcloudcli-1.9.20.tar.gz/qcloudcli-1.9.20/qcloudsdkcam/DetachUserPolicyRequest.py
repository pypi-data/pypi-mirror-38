# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class DetachUserPolicyRequest(Request):

    def __init__(self):
        super(DetachUserPolicyRequest, self).__init__(
            'cam', 'qcloudcliV1', 'DetachUserPolicy', 'cam.api.qcloud.com')

    def get_policyId(self):
        return self.get_params().get('policyId')

    def set_policyId(self, policyId):
        self.add_param('policyId', policyId)

    def get_uin(self):
        return self.get_params().get('uin')

    def set_uin(self, uin):
        self.add_param('uin', uin)
