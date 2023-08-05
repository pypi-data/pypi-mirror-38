# coding: utf-8

"""
    Fiddle Options Platform

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from mercury.api_client import ApiClient


class TradeserviceApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def calculate_decomposed_pn_l(self, **kwargs):  # noqa: E501
        """Returns the P&amp;L timeline decomposed by greeks for the given trade and the specified time range  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.calculate_decomposed_pn_l(async=True)
        >>> result = thread.get()

        :param async bool
        :param Position position:
        :param date from_date:
        :param date to:
        :return: list[DataPoint]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.calculate_decomposed_pn_l_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.calculate_decomposed_pn_l_with_http_info(**kwargs)  # noqa: E501
            return data

    def calculate_decomposed_pn_l_with_http_info(self, **kwargs):  # noqa: E501
        """Returns the P&amp;L timeline decomposed by greeks for the given trade and the specified time range  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.calculate_decomposed_pn_l_with_http_info(async=True)
        >>> result = thread.get()

        :param async bool
        :param Position position:
        :param date from_date:
        :param date to:
        :return: list[DataPoint]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['position', 'from_date', 'to_date']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method calculate_decomposed_pn_l" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'from_date' in params:
            query_params.append(('from', params['from_date']))  # noqa: E501
        if 'to_date' in params:
            query_params.append(('to', params['to_date']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'position' in params:
            body_params = params['position']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tradeservice/dpnlCalculator', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[DataPoint]',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def calculate_historical_pn_l(self, **kwargs):  # noqa: E501
        """Returns the P&amp;L timeline for the given trade and the specified time range  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.calculate_historical_pn_l(async=True)
        >>> result = thread.get()

        :param async bool
        :param Position position:
        :param date from_date:
        :param date to:
        :return: list[DataPoint]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.calculate_historical_pn_l_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.calculate_historical_pn_l_with_http_info(**kwargs)  # noqa: E501
            return data

    def calculate_historical_pn_l_with_http_info(self, **kwargs):  # noqa: E501
        """Returns the P&amp;L timeline for the given trade and the specified time range  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.calculate_historical_pn_l_with_http_info(async=True)
        >>> result = thread.get()

        :param async bool
        :param Position position:
        :param date from_date:
        :param date to:
        :return: list[DataPoint]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['position', 'from_date', 'to_date']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method calculate_historical_pn_l" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'from_date' in params:
            query_params.append(('from', params['from_date']))  # noqa: E501
        if 'to_date' in params:
            query_params.append(('to', params['to_date']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'position' in params:
            body_params = params['position']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tradeservice/histpnlCalculator', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[DataPoint]',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def calculate_historical_value(self, **kwargs):  # noqa: E501
        """Returns the historical dollar denominated value for the given trade and the time window  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.calculate_historical_value(async=True)
        >>> result = thread.get()

        :param async bool
        :param Position position:
        :param date from_date:
        :param date to:
        :return: list[DateValueDataPointDouble]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.calculate_historical_value_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.calculate_historical_value_with_http_info(**kwargs)  # noqa: E501
            return data

    def calculate_historical_value_with_http_info(self, **kwargs):  # noqa: E501
        """Returns the historical dollar denominated value for the given trade and the time window  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.calculate_historical_value_with_http_info(async=True)
        >>> result = thread.get()

        :param async bool
        :param Position position:
        :param date from_date:
        :param date to:
        :return: list[DateValueDataPointDouble]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['position', 'from_date', 'to_date']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method calculate_historical_value" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'from_date' in params:
            query_params.append(('from', params['from_date']))  # noqa: E501
        if 'to_date' in params:
            query_params.append(('to', params['to_date']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'position' in params:
            body_params = params['position']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tradeservice/histvalueCalculator', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[DateValueDataPointDouble]',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def calculate_instant_decomposed_pn_l(self, **kwargs):  # noqa: E501
        """Returns the greek decomposed P&amp;L for the given trade and the time window  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.calculate_instant_decomposed_pn_l(async=True)
        >>> result = thread.get()

        :param async bool
        :param Position position:
        :param date from_date:
        :param date to:
        :return: DataPoint
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.calculate_instant_decomposed_pn_l_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.calculate_instant_decomposed_pn_l_with_http_info(**kwargs)  # noqa: E501
            return data

    def calculate_instant_decomposed_pn_l_with_http_info(self, **kwargs):  # noqa: E501
        """Returns the greek decomposed P&amp;L for the given trade and the time window  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.calculate_instant_decomposed_pn_l_with_http_info(async=True)
        >>> result = thread.get()

        :param async bool
        :param Position position:
        :param date from_date:
        :param date to:
        :return: DataPoint
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['position', 'from_date', 'to_date']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method calculate_instant_decomposed_pn_l" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'from_date' in params:
            query_params.append(('from', params['from_date']))  # noqa: E501
        if 'to_date' in params:
            query_params.append(('to', params['to_date']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'position' in params:
            body_params = params['position']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tradeservice/instantdpnlCalculator', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DataPoint',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def calculate_pn_l(self, **kwargs):  # noqa: E501
        """Returns the the t+0 curve and expiration PnL curve for the given trade  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.calculate_pn_l(async=True)
        >>> result = thread.get()

        :param async bool
        :param Position position:
        :param date date:
        :return: PnL
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.calculate_pn_l_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.calculate_pn_l_with_http_info(**kwargs)  # noqa: E501
            return data

    def calculate_pn_l_with_http_info(self, **kwargs):  # noqa: E501
        """Returns the the t+0 curve and expiration PnL curve for the given trade  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.calculate_pn_l_with_http_info(async=True)
        >>> result = thread.get()

        :param async bool
        :param Position position:
        :param date date:
        :return: PnL
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['position', 'date']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method calculate_pn_l" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'date' in params:
            query_params.append(('date', params['date']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'position' in params:
            body_params = params['position']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tradeservice/pnlCalculator', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PnL',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
