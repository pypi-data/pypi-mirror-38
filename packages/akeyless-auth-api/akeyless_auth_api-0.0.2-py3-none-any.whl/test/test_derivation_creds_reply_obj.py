# coding: utf-8

"""
    Auth - Application API

    Auth manages access policies for services that need access policies management for their clients. Auth also issues temporary credentials for the services' clients and validates them for the services  # noqa: E501

    OpenAPI spec version: 1.0.2
    Contact: refael@akeyless-security.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import akeyless_auth_api
from akeyless_auth_api.models.derivation_creds_reply_obj import DerivationCredsReplyObj  # noqa: E501
from akeyless_auth_api.rest import ApiException


class TestDerivationCredsReplyObj(unittest.TestCase):
    """DerivationCredsReplyObj unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDerivationCredsReplyObj(self):
        """Test DerivationCredsReplyObj"""
        # FIXME: construct object with mandatory attributes with example values
        # model = akeyless_auth_api.models.derivation_creds_reply_obj.DerivationCredsReplyObj()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
