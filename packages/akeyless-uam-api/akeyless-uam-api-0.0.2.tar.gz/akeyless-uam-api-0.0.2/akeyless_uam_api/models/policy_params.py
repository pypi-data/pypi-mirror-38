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

from akeyless_uam_api.models.policy_rules import PolicyRules  # noqa: F401,E501
from akeyless_uam_api.models.policy_rules_type import PolicyRulesType  # noqa: F401,E501


class PolicyParams(object):
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
        'account_id': 'str',
        'attaches': 'str',
        'comment': 'str',
        'expires': 'int',
        'policy_rules_type': 'PolicyRulesType',
        'rules': 'PolicyRules'
    }

    attribute_map = {
        'account_id': 'account_id',
        'attaches': 'attaches',
        'comment': 'comment',
        'expires': 'expires',
        'policy_rules_type': 'policy_rules_type',
        'rules': 'rules'
    }

    def __init__(self, account_id=None, attaches=None, comment=None, expires=None, policy_rules_type=None, rules=None):  # noqa: E501
        """PolicyParams - a model defined in Swagger"""  # noqa: E501

        self._account_id = None
        self._attaches = None
        self._comment = None
        self._expires = None
        self._policy_rules_type = None
        self._rules = None
        self.discriminator = None

        if account_id is not None:
            self.account_id = account_id
        if attaches is not None:
            self.attaches = attaches
        if comment is not None:
            self.comment = comment
        self.expires = expires
        if policy_rules_type is not None:
            self.policy_rules_type = policy_rules_type
        if rules is not None:
            self.rules = rules

    @property
    def account_id(self):
        """Gets the account_id of this PolicyParams.  # noqa: E501

        Account id.  # noqa: E501

        :return: The account_id of this PolicyParams.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this PolicyParams.

        Account id.  # noqa: E501

        :param account_id: The account_id of this PolicyParams.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def attaches(self):
        """Gets the attaches of this PolicyParams.  # noqa: E501

        Generic field in a JSON format that contains additional information about the policy. This JSON will be attached to the temporary credentials that will be issued for this policy.  # noqa: E501

        :return: The attaches of this PolicyParams.  # noqa: E501
        :rtype: str
        """
        return self._attaches

    @attaches.setter
    def attaches(self, attaches):
        """Sets the attaches of this PolicyParams.

        Generic field in a JSON format that contains additional information about the policy. This JSON will be attached to the temporary credentials that will be issued for this policy.  # noqa: E501

        :param attaches: The attaches of this PolicyParams.  # noqa: E501
        :type: str
        """

        self._attaches = attaches

    @property
    def comment(self):
        """Gets the comment of this PolicyParams.  # noqa: E501

        Comments  # noqa: E501

        :return: The comment of this PolicyParams.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this PolicyParams.

        Comments  # noqa: E501

        :param comment: The comment of this PolicyParams.  # noqa: E501
        :type: str
        """

        self._comment = comment

    @property
    def expires(self):
        """Gets the expires of this PolicyParams.  # noqa: E501

        Policy expiration date (Unix timestamp).  # noqa: E501

        :return: The expires of this PolicyParams.  # noqa: E501
        :rtype: int
        """
        return self._expires

    @expires.setter
    def expires(self, expires):
        """Sets the expires of this PolicyParams.

        Policy expiration date (Unix timestamp).  # noqa: E501

        :param expires: The expires of this PolicyParams.  # noqa: E501
        :type: int
        """
        if expires is None:
            raise ValueError("Invalid value for `expires`, must not be `None`")  # noqa: E501

        self._expires = expires

    @property
    def policy_rules_type(self):
        """Gets the policy_rules_type of this PolicyParams.  # noqa: E501


        :return: The policy_rules_type of this PolicyParams.  # noqa: E501
        :rtype: PolicyRulesType
        """
        return self._policy_rules_type

    @policy_rules_type.setter
    def policy_rules_type(self, policy_rules_type):
        """Sets the policy_rules_type of this PolicyParams.


        :param policy_rules_type: The policy_rules_type of this PolicyParams.  # noqa: E501
        :type: PolicyRulesType
        """

        self._policy_rules_type = policy_rules_type

    @property
    def rules(self):
        """Gets the rules of this PolicyParams.  # noqa: E501


        :return: The rules of this PolicyParams.  # noqa: E501
        :rtype: PolicyRules
        """
        return self._rules

    @rules.setter
    def rules(self, rules):
        """Sets the rules of this PolicyParams.


        :param rules: The rules of this PolicyParams.  # noqa: E501
        :type: PolicyRules
        """

        self._rules = rules

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
        if not isinstance(other, PolicyParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
