# -*- coding: utf-8 -*-
from requests import get, post

from ebayfeed.constants import ENVIRONMENT_PRODUCTION
from ebayfeed.utils import get_api_uri


class Api:
    """
    eBay API wrapper.
    """

    def __init__(self, env=ENVIRONMENT_PRODUCTION):
        """
        Create an Api object for the given environment.

        Args:
            env (str, optional): eBay environment. Must be one of [ebayfeed.EBAY_PRODUCTION, ebayfeed.EBAY_SANDBOX].
                                 Default: ebayfeed.EBAY_PRODUCTION.
        """
        self.uri = get_api_uri(env)  #: eBay API uri

    def post(self, route, headers={}, params={}):
        """
        POST request to eBay API.

        Args:
            route (str): API POST route.
            headers (dict, optional): Dictionary of request headers. Default: empty.
            params (dict, optional): Dictionary of request parameters, Default: empty.
        """
        rsp = post("{}/{}".format(self.uri, route), headers=headers, params=params)
        rsp.raise_for_status()
        return rsp

    def get(self, route, headers={}, params={}):
        """
        GET request to eBay API.

        Args:
            route (str): API GET route.
            headers (dict, optional): Dictionary of request headers. Default: empty.
            params (dict, optional): Dictionary of request parameters. Default: empty.
        """
        rsp = get("{}/{}".format(self.uri, route), headers=headers, params=params)
        rsp.raise_for_status()
        return rsp
