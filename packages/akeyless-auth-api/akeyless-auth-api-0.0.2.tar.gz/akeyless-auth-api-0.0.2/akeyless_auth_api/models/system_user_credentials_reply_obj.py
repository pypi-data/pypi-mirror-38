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


class SystemUserCredentialsReplyObj(object):
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
        'auth_creds': 'str',
        'expiry': 'int',
        'kfm_creds': 'str',
        'uam_creds': 'str'
    }

    attribute_map = {
        'auth_creds': 'auth_creds',
        'expiry': 'expiry',
        'kfm_creds': 'kfm_creds',
        'uam_creds': 'uam_creds'
    }

    def __init__(self, auth_creds=None, expiry=None, kfm_creds=None, uam_creds=None):  # noqa: E501
        """SystemUserCredentialsReplyObj - a model defined in Swagger"""  # noqa: E501

        self._auth_creds = None
        self._expiry = None
        self._kfm_creds = None
        self._uam_creds = None
        self.discriminator = None

        if auth_creds is not None:
            self.auth_creds = auth_creds
        if expiry is not None:
            self.expiry = expiry
        if kfm_creds is not None:
            self.kfm_creds = kfm_creds
        if uam_creds is not None:
            self.uam_creds = uam_creds

    @property
    def auth_creds(self):
        """Gets the auth_creds of this SystemUserCredentialsReplyObj.  # noqa: E501

        Temporary credentials for accessing Auth  # noqa: E501

        :return: The auth_creds of this SystemUserCredentialsReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._auth_creds

    @auth_creds.setter
    def auth_creds(self, auth_creds):
        """Sets the auth_creds of this SystemUserCredentialsReplyObj.

        Temporary credentials for accessing Auth  # noqa: E501

        :param auth_creds: The auth_creds of this SystemUserCredentialsReplyObj.  # noqa: E501
        :type: str
        """

        self._auth_creds = auth_creds

    @property
    def expiry(self):
        """Gets the expiry of this SystemUserCredentialsReplyObj.  # noqa: E501

        Credentials expiration date  # noqa: E501

        :return: The expiry of this SystemUserCredentialsReplyObj.  # noqa: E501
        :rtype: int
        """
        return self._expiry

    @expiry.setter
    def expiry(self, expiry):
        """Sets the expiry of this SystemUserCredentialsReplyObj.

        Credentials expiration date  # noqa: E501

        :param expiry: The expiry of this SystemUserCredentialsReplyObj.  # noqa: E501
        :type: int
        """

        self._expiry = expiry

    @property
    def kfm_creds(self):
        """Gets the kfm_creds of this SystemUserCredentialsReplyObj.  # noqa: E501

        Temporary credentials for accessing the KFMs instances  # noqa: E501

        :return: The kfm_creds of this SystemUserCredentialsReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._kfm_creds

    @kfm_creds.setter
    def kfm_creds(self, kfm_creds):
        """Sets the kfm_creds of this SystemUserCredentialsReplyObj.

        Temporary credentials for accessing the KFMs instances  # noqa: E501

        :param kfm_creds: The kfm_creds of this SystemUserCredentialsReplyObj.  # noqa: E501
        :type: str
        """

        self._kfm_creds = kfm_creds

    @property
    def uam_creds(self):
        """Gets the uam_creds of this SystemUserCredentialsReplyObj.  # noqa: E501

        Temporary credentials for accessing the UAM service  # noqa: E501

        :return: The uam_creds of this SystemUserCredentialsReplyObj.  # noqa: E501
        :rtype: str
        """
        return self._uam_creds

    @uam_creds.setter
    def uam_creds(self, uam_creds):
        """Sets the uam_creds of this SystemUserCredentialsReplyObj.

        Temporary credentials for accessing the UAM service  # noqa: E501

        :param uam_creds: The uam_creds of this SystemUserCredentialsReplyObj.  # noqa: E501
        :type: str
        """

        self._uam_creds = uam_creds

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
        if not isinstance(other, SystemUserCredentialsReplyObj):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
