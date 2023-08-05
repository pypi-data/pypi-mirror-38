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


class KFMStatusReplyObj(object):
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
        'instance_id': 'str',
        'version': 'str'
    }

    attribute_map = {
        'instance_id': 'instance-id',
        'version': 'version'
    }

    def __init__(self, instance_id=None, version=None):  # noqa: E501
        """KFMStatusReplyObj - a model defined in Swagger"""  # noqa: E501

        self._instance_id = None
        self._version = None
        self.discriminator = None

        if instance_id is not None:
            self.instance_id = instance_id
        if version is not None:
            self.version = version

    @property
    def instance_id(self):
        """Gets the instance_id of this KFMStatusReplyObj.  # noqa: E501

        The Id of the KFM instance  # noqa: E501

        :return: The instance_id of this KFMStatusReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this KFMStatusReplyObj.

        The Id of the KFM instance  # noqa: E501

        :param instance_id: The instance_id of this KFMStatusReplyObj.  # noqa: E501
        :type: str
        """

        self._instance_id = instance_id

    @property
    def version(self):
        """Gets the version of this KFMStatusReplyObj.  # noqa: E501

        Current KFM version  # noqa: E501

        :return: The version of this KFMStatusReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this KFMStatusReplyObj.

        Current KFM version  # noqa: E501

        :param version: The version of this KFMStatusReplyObj.  # noqa: E501
        :type: str
        """

        self._version = version

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
        if not isinstance(other, KFMStatusReplyObj):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
