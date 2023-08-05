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


class CreateAccountCredsParams(object):
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
        'account_admin_user_email': 'str',
        'account_admin_user_phone': 'str',
        'expires': 'int',
        'policy_rules_type': 'PolicyRulesType',
        'rules': 'PolicyRules'
    }

    attribute_map = {
        'account_admin_user_email': 'account_admin_user_email',
        'account_admin_user_phone': 'account_admin_user_phone',
        'expires': 'expires',
        'policy_rules_type': 'policy_rules_type',
        'rules': 'rules'
    }

    def __init__(self, account_admin_user_email=None, account_admin_user_phone=None, expires=None, policy_rules_type=None, rules=None):  # noqa: E501
        """CreateAccountCredsParams - a model defined in Swagger"""  # noqa: E501

        self._account_admin_user_email = None
        self._account_admin_user_phone = None
        self._expires = None
        self._policy_rules_type = None
        self._rules = None
        self.discriminator = None

        if account_admin_user_email is not None:
            self.account_admin_user_email = account_admin_user_email
        if account_admin_user_phone is not None:
            self.account_admin_user_phone = account_admin_user_phone
        if expires is not None:
            self.expires = expires
        if policy_rules_type is not None:
            self.policy_rules_type = policy_rules_type
        if rules is not None:
            self.rules = rules

    @property
    def account_admin_user_email(self):
        """Gets the account_admin_user_email of this CreateAccountCredsParams.  # noqa: E501

        Account admin user email  # noqa: E501

        :return: The account_admin_user_email of this CreateAccountCredsParams.  # noqa: E501
        :rtype: str
        """
        return self._account_admin_user_email

    @account_admin_user_email.setter
    def account_admin_user_email(self, account_admin_user_email):
        """Sets the account_admin_user_email of this CreateAccountCredsParams.

        Account admin user email  # noqa: E501

        :param account_admin_user_email: The account_admin_user_email of this CreateAccountCredsParams.  # noqa: E501
        :type: str
        """

        self._account_admin_user_email = account_admin_user_email

    @property
    def account_admin_user_phone(self):
        """Gets the account_admin_user_phone of this CreateAccountCredsParams.  # noqa: E501

        Account admin user phone  # noqa: E501

        :return: The account_admin_user_phone of this CreateAccountCredsParams.  # noqa: E501
        :rtype: str
        """
        return self._account_admin_user_phone

    @account_admin_user_phone.setter
    def account_admin_user_phone(self, account_admin_user_phone):
        """Sets the account_admin_user_phone of this CreateAccountCredsParams.

        Account admin user phone  # noqa: E501

        :param account_admin_user_phone: The account_admin_user_phone of this CreateAccountCredsParams.  # noqa: E501
        :type: str
        """

        self._account_admin_user_phone = account_admin_user_phone

    @property
    def expires(self):
        """Gets the expires of this CreateAccountCredsParams.  # noqa: E501

        Policy expiration date (Unix timestamp).  # noqa: E501

        :return: The expires of this CreateAccountCredsParams.  # noqa: E501
        :rtype: int
        """
        return self._expires

    @expires.setter
    def expires(self, expires):
        """Sets the expires of this CreateAccountCredsParams.

        Policy expiration date (Unix timestamp).  # noqa: E501

        :param expires: The expires of this CreateAccountCredsParams.  # noqa: E501
        :type: int
        """

        self._expires = expires

    @property
    def policy_rules_type(self):
        """Gets the policy_rules_type of this CreateAccountCredsParams.  # noqa: E501


        :return: The policy_rules_type of this CreateAccountCredsParams.  # noqa: E501
        :rtype: PolicyRulesType
        """
        return self._policy_rules_type

    @policy_rules_type.setter
    def policy_rules_type(self, policy_rules_type):
        """Sets the policy_rules_type of this CreateAccountCredsParams.


        :param policy_rules_type: The policy_rules_type of this CreateAccountCredsParams.  # noqa: E501
        :type: PolicyRulesType
        """

        self._policy_rules_type = policy_rules_type

    @property
    def rules(self):
        """Gets the rules of this CreateAccountCredsParams.  # noqa: E501


        :return: The rules of this CreateAccountCredsParams.  # noqa: E501
        :rtype: PolicyRules
        """
        return self._rules

    @rules.setter
    def rules(self, rules):
        """Sets the rules of this CreateAccountCredsParams.


        :param rules: The rules of this CreateAccountCredsParams.  # noqa: E501
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
        if not isinstance(other, CreateAccountCredsParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
