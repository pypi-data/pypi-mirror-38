# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class ModifySubnetDhcpRelayFlagRequest(Request):

    def __init__(self):
        super(ModifySubnetDhcpRelayFlagRequest, self).__init__(
            'bmvpc', 'qcloudcliV1', 'ModifySubnetDhcpRelayFlag', 'bmvpc.api.qcloud.com')

    def get_dhcpEnable(self):
        return self.get_params().get('dhcpEnable')

    def set_dhcpEnable(self, dhcpEnable):
        self.add_param('dhcpEnable', dhcpEnable)

    def get_dhcpServerIp(self):
        return self.get_params().get('dhcpServerIp')

    def set_dhcpServerIp(self, dhcpServerIp):
        self.add_param('dhcpServerIp', dhcpServerIp)

    def get_ipReserve(self):
        return self.get_params().get('ipReserve')

    def set_ipReserve(self, ipReserve):
        self.add_param('ipReserve', ipReserve)

    def get_subnetId(self):
        return self.get_params().get('subnetId')

    def set_subnetId(self, subnetId):
        self.add_param('subnetId', subnetId)

    def get_unSubnetId(self):
        return self.get_params().get('unSubnetId')

    def set_unSubnetId(self, unSubnetId):
        self.add_param('unSubnetId', unSubnetId)

    def get_unVpcId(self):
        return self.get_params().get('unVpcId')

    def set_unVpcId(self, unVpcId):
        self.add_param('unVpcId', unVpcId)

    def get_vpcId(self):
        return self.get_params().get('vpcId')

    def set_vpcId(self, vpcId):
        self.add_param('vpcId', vpcId)
