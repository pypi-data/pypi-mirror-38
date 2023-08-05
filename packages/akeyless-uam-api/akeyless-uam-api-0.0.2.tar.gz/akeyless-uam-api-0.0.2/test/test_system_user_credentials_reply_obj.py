# coding: utf-8

"""
    UAM - Application API

    UAM manages client accounts and allows each client to define users, roles and master keys. The core operations of UAM are as follows: Creating new accounts. For each account: Creating new master keys. Adding new users Adding new roles Attaching roles to users. Attaching roles to keys. Returning the key's metadata together with temporary access credentials in order to access the key fragments.  # noqa: E501

    OpenAPI spec version: 1.0.2
    Contact: refael@akeyless-security.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import akeyless_uam_api
from akeyless_uam_api.models.system_user_credentials_reply_obj import SystemUserCredentialsReplyObj  # noqa: E501
from akeyless_uam_api.rest import ApiException


class TestSystemUserCredentialsReplyObj(unittest.TestCase):
    """SystemUserCredentialsReplyObj unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSystemUserCredentialsReplyObj(self):
        """Test SystemUserCredentialsReplyObj"""
        # FIXME: construct object with mandatory attributes with example values
        # model = akeyless_uam_api.models.system_user_credentials_reply_obj.SystemUserCredentialsReplyObj()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
