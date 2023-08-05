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


class DerivationCredsReplyObj(object):
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
        'kf_ms_hosts_dns_map': 'dict(str, str)',
        'credential': 'str',
        'expiry': 'int',
        'item_id': 'int',
        'item_name': 'str',
        'item_size': 'int',
        'item_type': 'str',
        'item_version': 'int',
        'restricted_dd': 'str'
    }

    attribute_map = {
        'kf_ms_hosts_dns_map': 'KFMsHostsDNSMap',
        'credential': 'credential',
        'expiry': 'expiry',
        'item_id': 'item_id',
        'item_name': 'item_name',
        'item_size': 'item_size',
        'item_type': 'item_type',
        'item_version': 'item_version',
        'restricted_dd': 'restricted_dd'
    }

    def __init__(self, kf_ms_hosts_dns_map=None, credential=None, expiry=None, item_id=None, item_name=None, item_size=None, item_type=None, item_version=None, restricted_dd=None):  # noqa: E501
        """DerivationCredsReplyObj - a model defined in Swagger"""  # noqa: E501

        self._kf_ms_hosts_dns_map = None
        self._credential = None
        self._expiry = None
        self._item_id = None
        self._item_name = None
        self._item_size = None
        self._item_type = None
        self._item_version = None
        self._restricted_dd = None
        self.discriminator = None

        if kf_ms_hosts_dns_map is not None:
            self.kf_ms_hosts_dns_map = kf_ms_hosts_dns_map
        if credential is not None:
            self.credential = credential
        if expiry is not None:
            self.expiry = expiry
        if item_id is not None:
            self.item_id = item_id
        if item_name is not None:
            self.item_name = item_name
        if item_size is not None:
            self.item_size = item_size
        if item_type is not None:
            self.item_type = item_type
        if item_version is not None:
            self.item_version = item_version
        if restricted_dd is not None:
            self.restricted_dd = restricted_dd

    @property
    def kf_ms_hosts_dns_map(self):
        """Gets the kf_ms_hosts_dns_map of this DerivationCredsReplyObj.  # noqa: E501

        Mapping between the serial number of the item fragments and the KFMs hosts DNS in which they are stored.  # noqa: E501

        :return: The kf_ms_hosts_dns_map of this DerivationCredsReplyObj.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._kf_ms_hosts_dns_map

    @kf_ms_hosts_dns_map.setter
    def kf_ms_hosts_dns_map(self, kf_ms_hosts_dns_map):
        """Sets the kf_ms_hosts_dns_map of this DerivationCredsReplyObj.

        Mapping between the serial number of the item fragments and the KFMs hosts DNS in which they are stored.  # noqa: E501

        :param kf_ms_hosts_dns_map: The kf_ms_hosts_dns_map of this DerivationCredsReplyObj.  # noqa: E501
        :type: dict(str, str)
        """

        self._kf_ms_hosts_dns_map = kf_ms_hosts_dns_map

    @property
    def credential(self):
        """Gets the credential of this DerivationCredsReplyObj.  # noqa: E501

        Temporary credentials string (JWT format)  # noqa: E501

        :return: The credential of this DerivationCredsReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._credential

    @credential.setter
    def credential(self, credential):
        """Sets the credential of this DerivationCredsReplyObj.

        Temporary credentials string (JWT format)  # noqa: E501

        :param credential: The credential of this DerivationCredsReplyObj.  # noqa: E501
        :type: str
        """

        self._credential = credential

    @property
    def expiry(self):
        """Gets the expiry of this DerivationCredsReplyObj.  # noqa: E501

        Credentials expiration date  # noqa: E501

        :return: The expiry of this DerivationCredsReplyObj.  # noqa: E501
        :rtype: int
        """
        return self._expiry

    @expiry.setter
    def expiry(self, expiry):
        """Sets the expiry of this DerivationCredsReplyObj.

        Credentials expiration date  # noqa: E501

        :param expiry: The expiry of this DerivationCredsReplyObj.  # noqa: E501
        :type: int
        """

        self._expiry = expiry

    @property
    def item_id(self):
        """Gets the item_id of this DerivationCredsReplyObj.  # noqa: E501


        :return: The item_id of this DerivationCredsReplyObj.  # noqa: E501
        :rtype: int
        """
        return self._item_id

    @item_id.setter
    def item_id(self, item_id):
        """Sets the item_id of this DerivationCredsReplyObj.


        :param item_id: The item_id of this DerivationCredsReplyObj.  # noqa: E501
        :type: int
        """

        self._item_id = item_id

    @property
    def item_name(self):
        """Gets the item_name of this DerivationCredsReplyObj.  # noqa: E501

        The name, id, version, type and size of the item that the fragments belong to  # noqa: E501

        :return: The item_name of this DerivationCredsReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._item_name

    @item_name.setter
    def item_name(self, item_name):
        """Sets the item_name of this DerivationCredsReplyObj.

        The name, id, version, type and size of the item that the fragments belong to  # noqa: E501

        :param item_name: The item_name of this DerivationCredsReplyObj.  # noqa: E501
        :type: str
        """

        self._item_name = item_name

    @property
    def item_size(self):
        """Gets the item_size of this DerivationCredsReplyObj.  # noqa: E501


        :return: The item_size of this DerivationCredsReplyObj.  # noqa: E501
        :rtype: int
        """
        return self._item_size

    @item_size.setter
    def item_size(self, item_size):
        """Sets the item_size of this DerivationCredsReplyObj.


        :param item_size: The item_size of this DerivationCredsReplyObj.  # noqa: E501
        :type: int
        """

        self._item_size = item_size

    @property
    def item_type(self):
        """Gets the item_type of this DerivationCredsReplyObj.  # noqa: E501


        :return: The item_type of this DerivationCredsReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._item_type

    @item_type.setter
    def item_type(self, item_type):
        """Sets the item_type of this DerivationCredsReplyObj.


        :param item_type: The item_type of this DerivationCredsReplyObj.  # noqa: E501
        :type: str
        """

        self._item_type = item_type

    @property
    def item_version(self):
        """Gets the item_version of this DerivationCredsReplyObj.  # noqa: E501


        :return: The item_version of this DerivationCredsReplyObj.  # noqa: E501
        :rtype: int
        """
        return self._item_version

    @item_version.setter
    def item_version(self, item_version):
        """Sets the item_version of this DerivationCredsReplyObj.


        :param item_version: The item_version of this DerivationCredsReplyObj.  # noqa: E501
        :type: int
        """

        self._item_version = item_version

    @property
    def restricted_dd(self):
        """Gets the restricted_dd of this DerivationCredsReplyObj.  # noqa: E501

        In case not empty, the derivation operation will be restricted to this derivation data  # noqa: E501

        :return: The restricted_dd of this DerivationCredsReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._restricted_dd

    @restricted_dd.setter
    def restricted_dd(self, restricted_dd):
        """Sets the restricted_dd of this DerivationCredsReplyObj.

        In case not empty, the derivation operation will be restricted to this derivation data  # noqa: E501

        :param restricted_dd: The restricted_dd of this DerivationCredsReplyObj.  # noqa: E501
        :type: str
        """

        self._restricted_dd = restricted_dd

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
        if not isinstance(other, DerivationCredsReplyObj):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
