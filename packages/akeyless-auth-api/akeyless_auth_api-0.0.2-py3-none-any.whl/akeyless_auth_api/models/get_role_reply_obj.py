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


class GetRoleReplyObj(object):
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
        'comment': 'str',
        'role_action': 'str',
        'role_items': 'list[str]',
        'role_name': 'str',
        'role_users': 'list[str]'
    }

    attribute_map = {
        'comment': 'comment',
        'role_action': 'role_action',
        'role_items': 'role_items',
        'role_name': 'role_name',
        'role_users': 'role_users'
    }

    def __init__(self, comment=None, role_action=None, role_items=None, role_name=None, role_users=None):  # noqa: E501
        """GetRoleReplyObj - a model defined in Swagger"""  # noqa: E501

        self._comment = None
        self._role_action = None
        self._role_items = None
        self._role_name = None
        self._role_users = None
        self.discriminator = None

        if comment is not None:
            self.comment = comment
        if role_action is not None:
            self.role_action = role_action
        if role_items is not None:
            self.role_items = role_items
        if role_name is not None:
            self.role_name = role_name
        if role_users is not None:
            self.role_users = role_users

    @property
    def comment(self):
        """Gets the comment of this GetRoleReplyObj.  # noqa: E501


        :return: The comment of this GetRoleReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this GetRoleReplyObj.


        :param comment: The comment of this GetRoleReplyObj.  # noqa: E501
        :type: str
        """

        self._comment = comment

    @property
    def role_action(self):
        """Gets the role_action of this GetRoleReplyObj.  # noqa: E501


        :return: The role_action of this GetRoleReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._role_action

    @role_action.setter
    def role_action(self, role_action):
        """Sets the role_action of this GetRoleReplyObj.


        :param role_action: The role_action of this GetRoleReplyObj.  # noqa: E501
        :type: str
        """

        self._role_action = role_action

    @property
    def role_items(self):
        """Gets the role_items of this GetRoleReplyObj.  # noqa: E501


        :return: The role_items of this GetRoleReplyObj.  # noqa: E501
        :rtype: list[str]
        """
        return self._role_items

    @role_items.setter
    def role_items(self, role_items):
        """Sets the role_items of this GetRoleReplyObj.


        :param role_items: The role_items of this GetRoleReplyObj.  # noqa: E501
        :type: list[str]
        """

        self._role_items = role_items

    @property
    def role_name(self):
        """Gets the role_name of this GetRoleReplyObj.  # noqa: E501


        :return: The role_name of this GetRoleReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._role_name

    @role_name.setter
    def role_name(self, role_name):
        """Sets the role_name of this GetRoleReplyObj.


        :param role_name: The role_name of this GetRoleReplyObj.  # noqa: E501
        :type: str
        """

        self._role_name = role_name

    @property
    def role_users(self):
        """Gets the role_users of this GetRoleReplyObj.  # noqa: E501


        :return: The role_users of this GetRoleReplyObj.  # noqa: E501
        :rtype: list[str]
        """
        return self._role_users

    @role_users.setter
    def role_users(self, role_users):
        """Sets the role_users of this GetRoleReplyObj.


        :param role_users: The role_users of this GetRoleReplyObj.  # noqa: E501
        :type: list[str]
        """

        self._role_users = role_users

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
        if not isinstance(other, GetRoleReplyObj):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
