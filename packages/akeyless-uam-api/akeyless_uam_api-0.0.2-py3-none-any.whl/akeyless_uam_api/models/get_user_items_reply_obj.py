# coding: utf-8

"""
    UAM - Application API

    UAM manages client accounts and allows each client to define users, roles and master keys. The core operations of UAM are as follows: Creating new accounts. For each account: Creating new master keys. Adding new users Adding new roles Attaching roles to users. Attaching roles to keys. Returning the key's metadata together with temporary access credentials in order to access the key fragments.  # noqa: E501

    OpenAPI spec version: 1.0.2
    Contact: refael@akeyless-security.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from akeyless_uam_api.models.get_item_reply_obj import GetItemReplyObj  # noqa: F401,E501


class GetUserItemsReplyObj(object):
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
        'items': 'list[GetItemReplyObj]'
    }

    attribute_map = {
        'items': 'items'
    }

    def __init__(self, items=None):  # noqa: E501
        """GetUserItemsReplyObj - a model defined in Swagger"""  # noqa: E501

        self._items = None
        self.discriminator = None

        if items is not None:
            self.items = items

    @property
    def items(self):
        """Gets the items of this GetUserItemsReplyObj.  # noqa: E501

        List of items  # noqa: E501

        :return: The items of this GetUserItemsReplyObj.  # noqa: E501
        :rtype: list[GetItemReplyObj]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this GetUserItemsReplyObj.

        List of items  # noqa: E501

        :param items: The items of this GetUserItemsReplyObj.  # noqa: E501
        :type: list[GetItemReplyObj]
        """

        self._items = items

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
        if not isinstance(other, GetUserItemsReplyObj):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
