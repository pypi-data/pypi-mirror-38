# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class DescribeApisStatusRequest(Request):

    def __init__(self):
        super(DescribeApisStatusRequest, self).__init__(
            'apigateway', 'qcloudcliV1', 'DescribeApisStatus', 'apigateway.api.qcloud.com')

    def get_apiBuniessType(self):
        return self.get_params().get('apiBuniessType')

    def set_apiBuniessType(self, apiBuniessType):
        self.add_param('apiBuniessType', apiBuniessType)

    def get_apiIds(self):
        return self.get_params().get('apiIds')

    def set_apiIds(self, apiIds):
        self.add_param('apiIds', apiIds)

    def get_apiName(self):
        return self.get_params().get('apiName')

    def set_apiName(self, apiName):
        self.add_param('apiName', apiName)

    def get_apiType(self):
        return self.get_params().get('apiType')

    def set_apiType(self, apiType):
        self.add_param('apiType', apiType)

    def get_authRelationApiId(self):
        return self.get_params().get('authRelationApiId')

    def set_authRelationApiId(self, authRelationApiId):
        self.add_param('authRelationApiId', authRelationApiId)

    def get_authType(self):
        return self.get_params().get('authType')

    def set_authType(self, authType):
        self.add_param('authType', authType)

    def get_filter(self):
        return self.get_params().get('filter')

    def set_filter(self, filter):
        self.add_param('filter', filter)

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

    def get_orderby(self):
        return self.get_params().get('orderby')

    def set_orderby(self, orderby):
        self.add_param('orderby', orderby)

    def get_searchId(self):
        return self.get_params().get('searchId')

    def set_searchId(self, searchId):
        self.add_param('searchId', searchId)

    def get_searchName(self):
        return self.get_params().get('searchName')

    def set_searchName(self, searchName):
        self.add_param('searchName', searchName)

    def get_serviceId(self):
        return self.get_params().get('serviceId')

    def set_serviceId(self, serviceId):
        self.add_param('serviceId', serviceId)
