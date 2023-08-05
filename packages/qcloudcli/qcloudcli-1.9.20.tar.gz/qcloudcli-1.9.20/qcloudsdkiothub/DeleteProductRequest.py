# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class DeleteProductRequest(Request):

    def __init__(self):
        super(DeleteProductRequest, self).__init__(
            'iothub', 'qcloudcliV1', 'DeleteProduct', 'iothub.api.qcloud.com')

    def get_productName(self):
        return self.get_params().get('productName')

    def set_productName(self, productName):
        self.add_param('productName', productName)
