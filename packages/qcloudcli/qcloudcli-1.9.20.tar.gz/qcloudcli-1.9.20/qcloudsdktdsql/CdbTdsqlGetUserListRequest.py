# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class CdbTdsqlGetUserListRequest(Request):

    def __init__(self):
        super(CdbTdsqlGetUserListRequest, self).__init__(
            'tdsql', 'qcloudcliV1', 'CdbTdsqlGetUserList', 'tdsql.api.qcloud.com')

    def get_cdbInstanceId(self):
        return self.get_params().get('cdbInstanceId')

    def set_cdbInstanceId(self, cdbInstanceId):
        self.add_param('cdbInstanceId', cdbInstanceId)

    def get_dbMode(self):
        return self.get_params().get('dbMode')

    def set_dbMode(self, dbMode):
        self.add_param('dbMode', dbMode)
