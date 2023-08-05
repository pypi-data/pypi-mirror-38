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


class DerivedFragmentReplyObj(object):
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
        'derivation_data': 'str',
        'derived_fragment': 'str'
    }

    attribute_map = {
        'derivation_data': 'derivation_data',
        'derived_fragment': 'derived_fragment'
    }

    def __init__(self, derivation_data=None, derived_fragment=None):  # noqa: E501
        """DerivedFragmentReplyObj - a model defined in Swagger"""  # noqa: E501

        self._derivation_data = None
        self._derived_fragment = None
        self.discriminator = None

        if derivation_data is not None:
            self.derivation_data = derivation_data
        if derived_fragment is not None:
            self.derived_fragment = derived_fragment

    @property
    def derivation_data(self):
        """Gets the derivation_data of this DerivedFragmentReplyObj.  # noqa: E501

        The derivation data that was used for the fragment derivation operation. Relevant for double derivation where the returned derivation data are different from the derivation seed that was received by the client  # noqa: E501

        :return: The derivation_data of this DerivedFragmentReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._derivation_data

    @derivation_data.setter
    def derivation_data(self, derivation_data):
        """Sets the derivation_data of this DerivedFragmentReplyObj.

        The derivation data that was used for the fragment derivation operation. Relevant for double derivation where the returned derivation data are different from the derivation seed that was received by the client  # noqa: E501

        :param derivation_data: The derivation_data of this DerivedFragmentReplyObj.  # noqa: E501
        :type: str
        """

        self._derivation_data = derivation_data

    @property
    def derived_fragment(self):
        """Gets the derived_fragment of this DerivedFragmentReplyObj.  # noqa: E501

        The derived fragment value  # noqa: E501

        :return: The derived_fragment of this DerivedFragmentReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._derived_fragment

    @derived_fragment.setter
    def derived_fragment(self, derived_fragment):
        """Sets the derived_fragment of this DerivedFragmentReplyObj.

        The derived fragment value  # noqa: E501

        :param derived_fragment: The derived_fragment of this DerivedFragmentReplyObj.  # noqa: E501
        :type: str
        """

        self._derived_fragment = derived_fragment

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
        if not isinstance(other, DerivedFragmentReplyObj):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
