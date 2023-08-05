# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class AttachInstanceRequest(Request):

    def __init__(self):
        super(AttachInstanceRequest, self).__init__(
            'scaling', 'qcloudcliV1', 'AttachInstance', 'scaling.api.qcloud.com')

    def get_instanceIds(self):
        return self.get_params().get('instanceIds')

    def set_instanceIds(self, instanceIds):
        self.add_param('instanceIds', instanceIds)

    def get_scalingGroupId(self):
        return self.get_params().get('scalingGroupId')

    def set_scalingGroupId(self, scalingGroupId):
        self.add_param('scalingGroupId', scalingGroupId)
