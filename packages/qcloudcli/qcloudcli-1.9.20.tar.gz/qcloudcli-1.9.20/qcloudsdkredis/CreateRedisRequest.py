# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class CreateRedisRequest(Request):

    def __init__(self):
        super(CreateRedisRequest, self).__init__(
            'redis', 'qcloudcliV1', 'CreateRedis', 'redis.api.qcloud.com')

    def get_autoRenewFlag(self):
        return self.get_params().get('autoRenewFlag')

    def set_autoRenewFlag(self, autoRenewFlag):
        self.add_param('autoRenewFlag', autoRenewFlag)

    def get_goodsNum(self):
        return self.get_params().get('goodsNum')

    def set_goodsNum(self, goodsNum):
        self.add_param('goodsNum', goodsNum)

    def get_memSize(self):
        return self.get_params().get('memSize')

    def set_memSize(self, memSize):
        self.add_param('memSize', memSize)

    def get_password(self):
        return self.get_params().get('password')

    def set_password(self, password):
        self.add_param('password', password)

    def get_period(self):
        return self.get_params().get('period')

    def set_period(self, period):
        self.add_param('period', period)

    def get_projectId(self):
        return self.get_params().get('projectId')

    def set_projectId(self, projectId):
        self.add_param('projectId', projectId)

    def get_securityGroupList(self):
        return self.get_params().get('securityGroupList')

    def set_securityGroupList(self, securityGroupList):
        self.add_param('securityGroupList', securityGroupList)

    def get_subnetId(self):
        return self.get_params().get('subnetId')

    def set_subnetId(self, subnetId):
        self.add_param('subnetId', subnetId)

    def get_typeId(self):
        return self.get_params().get('typeId')

    def set_typeId(self, typeId):
        self.add_param('typeId', typeId)

    def get_unSubnetId(self):
        return self.get_params().get('unSubnetId')

    def set_unSubnetId(self, unSubnetId):
        self.add_param('unSubnetId', unSubnetId)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vPort(self):
        return self.get_params().get('vPort')

    def set_vPort(self, vPort):
        self.add_param('vPort', vPort)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)

    def get_zoneId(self):
        return self.get_params().get('zoneId')

    def set_zoneId(self, zoneId):
        self.add_param('zoneId', zoneId)

    def get_zoneName(self):
        return self.get_params().get('zoneName')

    def set_zoneName(self, zoneName):
        self.add_param('zoneName', zoneName)
