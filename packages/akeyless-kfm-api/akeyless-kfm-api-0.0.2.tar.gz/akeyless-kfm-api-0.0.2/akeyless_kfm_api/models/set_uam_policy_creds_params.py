# coding: utf-8

"""
    KFM - Application API

    KFM manages and stores key fragments. The core operations of each KFM instance are as follows: Creating secure random encryption keys which will be used as a master key fragment. Managing data storage for key fragments. Performing a key fragment derivation function, which generates a derived fragment from the original key fragment.  # noqa: E501

    OpenAPI spec version: 1.0.2
    Contact: refael@akeyless-security.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from akeyless_kfm_api.models.policy_rules import PolicyRules  # noqa: F401,E501
from akeyless_kfm_api.models.policy_rules_type import PolicyRulesType  # noqa: F401,E501
from akeyless_kfm_api.models.update_policy_mode import UpdatePolicyMode  # noqa: F401,E501


class SetUAMPolicyCredsParams(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'expires': 'int',
        'policy_rules_type': 'PolicyRulesType',
        'rules': 'PolicyRules',
        'update_modes': 'list[UpdatePolicyMode]'
    }

    attribute_map = {
        'expires': 'expires',
        'policy_rules_type': 'policy_rules_type',
        'rules': 'rules',
        'update_modes': 'update_modes'
    }

    def __init__(self, expires=None, policy_rules_type=None, rules=None, update_modes=None):  # noqa: E501
        """SetUAMPolicyCredsParams - a model defined in Swagger"""  # noqa: E501

        self._expires = None
        self._policy_rules_type = None
        self._rules = None
        self._update_modes = None
        self.discriminator = None

        if expires is not None:
            self.expires = expires
        if policy_rules_type is not None:
            self.policy_rules_type = policy_rules_type
        if rules is not None:
            self.rules = rules
        if update_modes is not None:
            self.update_modes = update_modes

    @property
    def expires(self):
        """Gets the expires of this SetUAMPolicyCredsParams.  # noqa: E501

        Policy expiration date (Unix timestamp).  # noqa: E501

        :return: The expires of this SetUAMPolicyCredsParams.  # noqa: E501
        :rtype: int
        """
        return self._expires

    @expires.setter
    def expires(self, expires):
        """Sets the expires of this SetUAMPolicyCredsParams.

        Policy expiration date (Unix timestamp).  # noqa: E501

        :param expires: The expires of this SetUAMPolicyCredsParams.  # noqa: E501
        :type: int
        """

        self._expires = expires

    @property
    def policy_rules_type(self):
        """Gets the policy_rules_type of this SetUAMPolicyCredsParams.  # noqa: E501


        :return: The policy_rules_type of this SetUAMPolicyCredsParams.  # noqa: E501
        :rtype: PolicyRulesType
        """
        return self._policy_rules_type

    @policy_rules_type.setter
    def policy_rules_type(self, policy_rules_type):
        """Sets the policy_rules_type of this SetUAMPolicyCredsParams.


        :param policy_rules_type: The policy_rules_type of this SetUAMPolicyCredsParams.  # noqa: E501
        :type: PolicyRulesType
        """

        self._policy_rules_type = policy_rules_type

    @property
    def rules(self):
        """Gets the rules of this SetUAMPolicyCredsParams.  # noqa: E501


        :return: The rules of this SetUAMPolicyCredsParams.  # noqa: E501
        :rtype: PolicyRules
        """
        return self._rules

    @rules.setter
    def rules(self, rules):
        """Sets the rules of this SetUAMPolicyCredsParams.


        :param rules: The rules of this SetUAMPolicyCredsParams.  # noqa: E501
        :type: PolicyRules
        """

        self._rules = rules

    @property
    def update_modes(self):
        """Gets the update_modes of this SetUAMPolicyCredsParams.  # noqa: E501

        Array of policy parameters names to be updated (update_key, update_exp, update_cidr). All the parameters will be updated in case of empty array  # noqa: E501

        :return: The update_modes of this SetUAMPolicyCredsParams.  # noqa: E501
        :rtype: list[UpdatePolicyMode]
        """
        return self._update_modes

    @update_modes.setter
    def update_modes(self, update_modes):
        """Sets the update_modes of this SetUAMPolicyCredsParams.

        Array of policy parameters names to be updated (update_key, update_exp, update_cidr). All the parameters will be updated in case of empty array  # noqa: E501

        :param update_modes: The update_modes of this SetUAMPolicyCredsParams.  # noqa: E501
        :type: list[UpdatePolicyMode]
        """

        self._update_modes = update_modes

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SetUAMPolicyCredsParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
