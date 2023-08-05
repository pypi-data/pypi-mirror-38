# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class DescribeJobSubmitInfoRequest(Request):

    def __init__(self):
        super(DescribeJobSubmitInfoRequest, self).__init__(
            'batch', 'qcloudcliV1', 'DescribeJobSubmitInfo', 'batch.api.qcloud.com')

    def get_JobId(self):
        return self.get_params().get('JobId')

    def set_JobId(self, JobId):
        self.add_param('JobId', JobId)

    def get_Version(self):
        return self.get_params().get('Version')

    def set_Version(self, Version):
        self.add_param('Version', Version)
