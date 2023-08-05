# -*- coding: utf-8 -*-

from qcloudsdkcore.request import Request

class LexicalCheckRequest(Request):

    def __init__(self):
        super(LexicalCheckRequest, self).__init__(
            'wenzhi', 'qcloudcliV1', 'LexicalCheck', 'wenzhi.api.qcloud.com')

    def get_text(self):
        return self.get_params().get('text')

    def set_text(self, text):
        self.add_param('text', text)
