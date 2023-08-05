# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class DescribeEipAclBmRequest(Request):

    def __init__(self):
        super(DescribeEipAclBmRequest, self).__init__(
            'bmeip', 'qcloudcliV1', 'DescribeEipAclBm', 'bmeip.api.qcloud.com')

    def get_aclIds(self):
        return self.get_params().get('aclIds')

    def set_aclIds(self, aclIds):
        self.add_param('aclIds', aclIds)

    def get_aclName(self):
        return self.get_params().get('aclName')

    def set_aclName(self, aclName):
        self.add_param('aclName', aclName)

    def get_aclNames(self):
        return self.get_params().get('aclNames')

    def set_aclNames(self, aclNames):
        self.add_param('aclNames', aclNames)

    def get_eipIds(self):
        return self.get_params().get('eipIds')

    def set_eipIds(self, eipIds):
        self.add_param('eipIds', eipIds)

    def get_eipNames(self):
        return self.get_params().get('eipNames')

    def set_eipNames(self, eipNames):
        self.add_param('eipNames', eipNames)

    def get_eips(self):
        return self.get_params().get('eips')

    def set_eips(self, eips):
        self.add_param('eips', eips)

    def get_limit(self):
        return self.get_params().get('limit')

    def set_limit(self, limit):
        self.add_param('limit', limit)

    def get_offset(self):
        return self.get_params().get('offset')

    def set_offset(self, offset):
        self.add_param('offset', offset)

    def get_order(self):
        return self.get_params().get('order')

    def set_order(self, order):
        self.add_param('order', order)

    def get_orderField(self):
        return self.get_params().get('orderField')

    def set_orderField(self, orderField):
        self.add_param('orderField', orderField)

    def get_query(self):
        return self.get_params().get('query')

    def set_query(self, query):
        self.add_param('query', query)
