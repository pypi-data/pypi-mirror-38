# coding: utf-8

"""
    Fiddle Options Platform

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint

import six

from mercury.client.model import BaseCondor, CondorValueException


class IronCondor(BaseCondor):
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
        'symbol': 'str',
        'quantity': 'int',
        'opening_date': 'date',
        'option_legs': 'list[OptionLeg]',
        'type': 'str',
        'direction': 'Direction'
    }

    attribute_map = {
        'symbol': 'symbol',
        'quantity': 'quantity',
        'opening_date': 'openingDate',
        'option_legs': 'optionLegs',
        'type': 'type',
        'direction': 'direction'
    }

    def __init__(self,
                 symbol=None,
                 opening_date=None,
                 quantity=1,
                 out_leg_call=None,
                 in_leg_call=None,
                 in_leg_put=None,
                 out_leg_put=None,
                 open_price=None,
                 option_legs=None,
                 type=None,
                 direction=None):  # noqa: E501
        """IronCondor - a model defined in Swagger"""  # noqa: E501
        self.discriminator = None

        if option_legs is not None:
            out_leg_call = option_legs[0]
            in_leg_call = option_legs[1]
            in_leg_put = option_legs[2]
            out_leg_put = option_legs[3]

        if not (in_leg_call.is_call() and out_leg_call.is_call() and
                not out_leg_put.is_call() and not in_leg_put.is_call()):
            raise CondorValueException('Invalid iron condor')

        if (out_leg_call.strike > in_leg_call.strike) or \
                (in_leg_put.strike < out_leg_put.strike):
            raise CondorValueException('Invalid iron condor - strike')

        super(IronCondor, self).__init__(symbol=symbol,
                                         opening_date=opening_date,
                                         open_price=open_price,
                                         quantity=quantity,
                                         out_lower_leg=out_leg_call,
                                         in_lower_mid_leg=in_leg_call,
                                         in_upper_mid_leg=in_leg_put,
                                         out_upper_leg=out_leg_put,
                                         type=type)

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
        if not isinstance(other, IronCondor):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
