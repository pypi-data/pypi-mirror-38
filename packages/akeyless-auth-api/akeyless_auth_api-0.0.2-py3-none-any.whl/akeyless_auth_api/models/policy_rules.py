# coding: utf-8

"""
    Auth - Application API

    Auth manages access policies for services that need access policies management for their clients. Auth also issues temporary credentials for the services' clients and validates them for the services  # noqa: E501

    OpenAPI spec version: 1.0.2
    Contact: refael@akeyless-security.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from akeyless_auth_api.models.algorithm import Algorithm  # noqa: F401,E501


class PolicyRules(object):
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
        'alg': 'Algorithm',
        'cidr_whitelist': 'str',
        'key': 'str'
    }

    attribute_map = {
        'alg': 'alg',
        'cidr_whitelist': 'cidr_whitelist',
        'key': 'key'
    }

    def __init__(self, alg=None, cidr_whitelist=None, key=None):  # noqa: E501
        """PolicyRules - a model defined in Swagger"""  # noqa: E501

        self._alg = None
        self._cidr_whitelist = None
        self._key = None
        self.discriminator = None

        if alg is not None:
            self.alg = alg
        if cidr_whitelist is not None:
            self.cidr_whitelist = cidr_whitelist
        if key is not None:
            self.key = key

    @property
    def alg(self):
        """Gets the alg of this PolicyRules.  # noqa: E501


        :return: The alg of this PolicyRules.  # noqa: E501
        :rtype: Algorithm
        """
        return self._alg

    @alg.setter
    def alg(self, alg):
        """Sets the alg of this PolicyRules.


        :param alg: The alg of this PolicyRules.  # noqa: E501
        :type: Algorithm
        """

        self._alg = alg

    @property
    def cidr_whitelist(self):
        """Gets the cidr_whitelist of this PolicyRules.  # noqa: E501

        An CIDR Whitelisting. Only requests from the ip addresses that match the CIDR list will be able to obtain temporary access credentials. The format of the CIDR list is a comma-separated list of valid CIDRs.The list length is limited to 10 CIDRs. In the case of an empty string there will be no restriction of IP addresses.  # noqa: E501

        :return: The cidr_whitelist of this PolicyRules.  # noqa: E501
        :rtype: str
        """
        return self._cidr_whitelist

    @cidr_whitelist.setter
    def cidr_whitelist(self, cidr_whitelist):
        """Sets the cidr_whitelist of this PolicyRules.

        An CIDR Whitelisting. Only requests from the ip addresses that match the CIDR list will be able to obtain temporary access credentials. The format of the CIDR list is a comma-separated list of valid CIDRs.The list length is limited to 10 CIDRs. In the case of an empty string there will be no restriction of IP addresses.  # noqa: E501

        :param cidr_whitelist: The cidr_whitelist of this PolicyRules.  # noqa: E501
        :type: str
        """

        self._cidr_whitelist = cidr_whitelist

    @property
    def key(self):
        """Gets the key of this PolicyRules.  # noqa: E501

        The public key value of the API-key. This is a mandatory parameter for API key policy.  # noqa: E501

        :return: The key of this PolicyRules.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this PolicyRules.

        The public key value of the API-key. This is a mandatory parameter for API key policy.  # noqa: E501

        :param key: The key of this PolicyRules.  # noqa: E501
        :type: str
        """

        self._key = key

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
        if not isinstance(other, PolicyRules):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
