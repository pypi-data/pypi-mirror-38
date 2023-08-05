# coding: utf-8

"""
    Fiddle Options Platform

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint

import six

from mercury.client.model.option_contract_type import OptionContractType
from mercury.client.model.option_leg import OptionLeg


class OptionContract(object):
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
        'strike': 'float',
        'bid': 'float',
        'ask': 'float',
        'volume': 'int',
        'open_interest': 'int',
        'delta': 'float',
        'gamma': 'float',
        'vega': 'float',
        'theta': 'float',
        'rho': 'float',
        'iv': 'float',
        'expiration_date': 'date',
        'call': 'bool',
        'mid': 'float'
    }

    attribute_map = {
        'strike': 'strike',
        'bid': 'bid',
        'ask': 'ask',
        'volume': 'volume',
        'open_interest': 'openInterest',
        'delta': 'delta',
        'gamma': 'gamma',
        'vega': 'vega',
        'theta': 'theta',
        'rho': 'rho',
        'iv': 'iv',
        'expiration_date': 'expirationDate',
        'call': 'call',
        'mid': 'mid'
    }

    def __init__(self, strike=None, bid=None, ask=None, volume=None, open_interest=None, delta=None, gamma=None, vega=None, theta=None, rho=None, iv=None, expiration_date=None, call=None, mid=None):  # noqa: E501
        """OptionContract - a model defined in Swagger"""  # noqa: E501

        self._strike = None
        self._bid = None
        self._ask = None
        self._volume = None
        self._open_interest = None
        self._delta = None
        self._gamma = None
        self._vega = None
        self._theta = None
        self._rho = None
        self._iv = None
        self._expiration_date = None
        self._call = None
        self._mid = None
        self.discriminator = None

        if strike is not None:
            self.strike = strike
        if bid is not None:
            self.bid = bid
        if ask is not None:
            self.ask = ask
        if volume is not None:
            self.volume = volume
        if open_interest is not None:
            self.open_interest = open_interest
        if delta is not None:
            self.delta = delta
        if gamma is not None:
            self.gamma = gamma
        if vega is not None:
            self.vega = vega
        if theta is not None:
            self.theta = theta
        if rho is not None:
            self.rho = rho
        if iv is not None:
            self.iv = iv
        if expiration_date is not None:
            self.expiration_date = expiration_date
        if call is not None:
            self.call = call
        if mid is not None:
            self.mid = mid

    @property
    def strike(self):
        """Gets the strike of this OptionContract.  # noqa: E501


        :return: The strike of this OptionContract.  # noqa: E501
        :rtype: float
        """
        return self._strike

    @strike.setter
    def strike(self, strike):
        """Sets the strike of this OptionContract.


        :param strike: The strike of this OptionContract.  # noqa: E501
        :type: float
        """

        self._strike = strike

    @property
    def bid(self):
        """Gets the bid of this OptionContract.  # noqa: E501


        :return: The bid of this OptionContract.  # noqa: E501
        :rtype: float
        """
        return self._bid

    @bid.setter
    def bid(self, bid):
        """Sets the bid of this OptionContract.


        :param bid: The bid of this OptionContract.  # noqa: E501
        :type: float
        """

        self._bid = bid

    @property
    def ask(self):
        """Gets the ask of this OptionContract.  # noqa: E501


        :return: The ask of this OptionContract.  # noqa: E501
        :rtype: float
        """
        return self._ask

    @ask.setter
    def ask(self, ask):
        """Sets the ask of this OptionContract.


        :param ask: The ask of this OptionContract.  # noqa: E501
        :type: float
        """

        self._ask = ask

    @property
    def volume(self):
        """Gets the volume of this OptionContract.  # noqa: E501


        :return: The volume of this OptionContract.  # noqa: E501
        :rtype: int
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this OptionContract.


        :param volume: The volume of this OptionContract.  # noqa: E501
        :type: int
        """

        self._volume = volume

    @property
    def open_interest(self):
        """Gets the open_interest of this OptionContract.  # noqa: E501


        :return: The open_interest of this OptionContract.  # noqa: E501
        :rtype: int
        """
        return self._open_interest

    @open_interest.setter
    def open_interest(self, open_interest):
        """Sets the open_interest of this OptionContract.


        :param open_interest: The open_interest of this OptionContract.  # noqa: E501
        :type: int
        """

        self._open_interest = open_interest

    @property
    def delta(self):
        """Gets the delta of this OptionContract.  # noqa: E501


        :return: The delta of this OptionContract.  # noqa: E501
        :rtype: float
        """
        return self._delta

    @delta.setter
    def delta(self, delta):
        """Sets the delta of this OptionContract.


        :param delta: The delta of this OptionContract.  # noqa: E501
        :type: float
        """

        self._delta = delta

    @property
    def gamma(self):
        """Gets the gamma of this OptionContract.  # noqa: E501


        :return: The gamma of this OptionContract.  # noqa: E501
        :rtype: float
        """
        return self._gamma

    @gamma.setter
    def gamma(self, gamma):
        """Sets the gamma of this OptionContract.


        :param gamma: The gamma of this OptionContract.  # noqa: E501
        :type: float
        """

        self._gamma = gamma

    @property
    def vega(self):
        """Gets the vega of this OptionContract.  # noqa: E501


        :return: The vega of this OptionContract.  # noqa: E501
        :rtype: float
        """
        return self._vega

    @vega.setter
    def vega(self, vega):
        """Sets the vega of this OptionContract.


        :param vega: The vega of this OptionContract.  # noqa: E501
        :type: float
        """

        self._vega = vega

    @property
    def theta(self):
        """Gets the theta of this OptionContract.  # noqa: E501


        :return: The theta of this OptionContract.  # noqa: E501
        :rtype: float
        """
        return self._theta

    @theta.setter
    def theta(self, theta):
        """Sets the theta of this OptionContract.


        :param theta: The theta of this OptionContract.  # noqa: E501
        :type: float
        """

        self._theta = theta

    @property
    def rho(self):
        """Gets the rho of this OptionContract.  # noqa: E501


        :return: The rho of this OptionContract.  # noqa: E501
        :rtype: float
        """
        return self._rho

    @rho.setter
    def rho(self, rho):
        """Sets the rho of this OptionContract.


        :param rho: The rho of this OptionContract.  # noqa: E501
        :type: float
        """

        self._rho = rho

    @property
    def iv(self):
        """Gets the iv of this OptionContract.  # noqa: E501


        :return: The iv of this OptionContract.  # noqa: E501
        :rtype: float
        """
        return self._iv

    @iv.setter
    def iv(self, iv):
        """Sets the iv of this OptionContract.


        :param rho: The iv of this OptionContract.  # noqa: E501
        :type: float
        """

        self._iv = iv

    @property
    def expiration_date(self):
        """Gets the expiration_date of this OptionContract.  # noqa: E501


        :return: The expiration_date of this OptionContract.  # noqa: E501
        :rtype: date
        """
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, expiration_date):
        """Sets the expiration_date of this OptionContract.


        :param expiration_date: The expiration_date of this OptionContract.  # noqa: E501
        :type: date
        """

        self._expiration_date = expiration_date

    @property
    def call(self):
        """Gets the call of this OptionContract.  # noqa: E501


        :return: The call of this OptionContract.  # noqa: E501
        :rtype: bool
        """
        return self._call

    @call.setter
    def call(self, call):
        """Sets the call of this OptionContract.


        :param call: The call of this OptionContract.  # noqa: E501
        :type: bool
        """

        self._call = call

    @property
    def mid(self):
        """Gets the mid of this OptionContract.  # noqa: E501


        :return: The mid of this OptionContract.  # noqa: E501
        :rtype: float
        """
        return self._mid

    @mid.setter
    def mid(self, mid):
        """Sets the mid of this OptionContract.


        :param mid: The mid of this OptionContract.  # noqa: E501
        :type: float
        """

        self._mid = mid

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

    def to_option_leg(self, quantity):
        return OptionLeg(expiration_date=self.expiration_date,
                         type=OptionContractType.CALL if self.call else OptionContractType.PUT,
                         quantity=quantity,
                         strike=self.strike,
                         opening_price=self.mid)

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OptionContract):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
