# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class DeleteClassRequest(Request):

    def __init__(self):
        super(DeleteClassRequest, self).__init__(
            'vod', 'qcloudcliV1', 'DeleteClass', 'vod.api.qcloud.com')

    def get_SubAppId(self):
        return self.get_params().get('SubAppId')

    def set_SubAppId(self, SubAppId):
        self.add_param('SubAppId', SubAppId)

    def get_classId(self):
        return self.get_params().get('classId')

    def set_classId(self, classId):
        self.add_param('classId', classId)
