# coding: utf-8

"""
    KFM - Application API

    KFM manages and stores key fragments. The core operations of each KFM instance are as follows: Creating secure random encryption keys which will be used as a master key fragment. Managing data storage for key fragments. Performing a key fragment derivation function, which generates a derived fragment from the original key fragment.  # noqa: E501

    OpenAPI spec version: 1.0.2
    Contact: refael@akeyless-security.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import akeyless_kfm_api
from akeyless_kfm_api.models.policy_params import PolicyParams  # noqa: E501
from akeyless_kfm_api.rest import ApiException


class TestPolicyParams(unittest.TestCase):
    """PolicyParams unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPolicyParams(self):
        """Test PolicyParams"""
        # FIXME: construct object with mandatory attributes with example values
        # model = akeyless_kfm_api.models.policy_params.PolicyParams()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
