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

from akeyless_auth_api.models.get_user_reply_obj import GetUserReplyObj  # noqa: F401,E501


class GetAccountUsersReplyObj(object):
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
        'users': 'list[GetUserReplyObj]'
    }

    attribute_map = {
        'users': 'users'
    }

    def __init__(self, users=None):  # noqa: E501
        """GetAccountUsersReplyObj - a model defined in Swagger"""  # noqa: E501

        self._users = None
        self.discriminator = None

        if users is not None:
            self.users = users

    @property
    def users(self):
        """Gets the users of this GetAccountUsersReplyObj.  # noqa: E501

        List of users  # noqa: E501

        :return: The users of this GetAccountUsersReplyObj.  # noqa: E501
        :rtype: list[GetUserReplyObj]
        """
        return self._users

    @users.setter
    def users(self, users):
        """Sets the users of this GetAccountUsersReplyObj.

        List of users  # noqa: E501

        :param users: The users of this GetAccountUsersReplyObj.  # noqa: E501
        :type: list[GetUserReplyObj]
        """

        self._users = users

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
        if not isinstance(other, GetAccountUsersReplyObj):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
