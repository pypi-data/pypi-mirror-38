# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class BindAlarmRuleObjectsRequest(Request):

    def __init__(self):
        super(BindAlarmRuleObjectsRequest, self).__init__(
            'monitor', 'qcloudcliV1', 'BindAlarmRuleObjects', 'monitor.api.qcloud.com')

    def get_alarmRuleId(self):
        return self.get_params().get('alarmRuleId')

    def set_alarmRuleId(self, alarmRuleId):
        self.add_param('alarmRuleId', alarmRuleId)

    def get_dimensions(self):
        return self.get_params().get('dimensions')

    def set_dimensions(self, dimensions):
        self.add_param('dimensions', dimensions)
