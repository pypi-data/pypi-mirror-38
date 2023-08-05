# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class AddCdnHostRequest(Request):

    def __init__(self):
        super(AddCdnHostRequest, self).__init__(
            'cdn', 'qcloudcliV1', 'AddCdnHost', 'cdn.api.qcloud.com')

    def get_accessIp(self):
        return self.get_params().get('accessIp')

    def set_accessIp(self, accessIp):
        self.add_param('accessIp', accessIp)

    def get_advancedCache(self):
        return self.get_params().get('advancedCache')

    def set_advancedCache(self, advancedCache):
        self.add_param('advancedCache', advancedCache)

    def get_backupOrigin(self):
        return self.get_params().get('backupOrigin')

    def set_backupOrigin(self, backupOrigin):
        self.add_param('backupOrigin', backupOrigin)

    def get_cache(self):
        return self.get_params().get('cache')

    def set_cache(self, cache):
        self.add_param('cache', cache)

    def get_cacheMode(self):
        return self.get_params().get('cacheMode')

    def set_cacheMode(self, cacheMode):
        self.add_param('cacheMode', cacheMode)

    def get_cnameHost(self):
        return self.get_params().get('cnameHost')

    def set_cnameHost(self, cnameHost):
        self.add_param('cnameHost', cnameHost)

    def get_cosOriginAuthorization(self):
        return self.get_params().get('cosOriginAuthorization')

    def set_cosOriginAuthorization(self, cosOriginAuthorization):
        self.add_param('cosOriginAuthorization', cosOriginAuthorization)

    def get_cosSpecialSign(self):
        return self.get_params().get('cosSpecialSign')

    def set_cosSpecialSign(self, cosSpecialSign):
        self.add_param('cosSpecialSign', cosSpecialSign)

    def get_follow302(self):
        return self.get_params().get('follow302')

    def set_follow302(self, follow302):
        self.add_param('follow302', follow302)

    def get_fullUrl(self):
        return self.get_params().get('fullUrl')

    def set_fullUrl(self, fullUrl):
        self.add_param('fullUrl', fullUrl)

    def get_fwdHost(self):
        return self.get_params().get('fwdHost')

    def set_fwdHost(self, fwdHost):
        self.add_param('fwdHost', fwdHost)

    def get_host(self):
        return self.get_params().get('host')

    def set_host(self, host):
        self.add_param('host', host)

    def get_hostType(self):
        return self.get_params().get('hostType')

    def set_hostType(self, hostType):
        self.add_param('hostType', hostType)

    def get_ipFrequenceLimit(self):
        return self.get_params().get('ipFrequenceLimit')

    def set_ipFrequenceLimit(self, ipFrequenceLimit):
        self.add_param('ipFrequenceLimit', ipFrequenceLimit)

    def get_origin(self):
        return self.get_params().get('origin')

    def set_origin(self, origin):
        self.add_param('origin', origin)

    def get_pathOrigin(self):
        return self.get_params().get('pathOrigin')

    def set_pathOrigin(self, pathOrigin):
        self.add_param('pathOrigin', pathOrigin)

    def get_projectId(self):
        return self.get_params().get('projectId')

    def set_projectId(self, projectId):
        self.add_param('projectId', projectId)

    def get_refer(self):
        return self.get_params().get('refer')

    def set_refer(self, refer):
        self.add_param('refer', refer)

    def get_rspHeader(self):
        return self.get_params().get('rspHeader')

    def set_rspHeader(self, rspHeader):
        self.add_param('rspHeader', rspHeader)

    def get_serviceType(self):
        return self.get_params().get('serviceType')

    def set_serviceType(self, serviceType):
        self.add_param('serviceType', serviceType)
