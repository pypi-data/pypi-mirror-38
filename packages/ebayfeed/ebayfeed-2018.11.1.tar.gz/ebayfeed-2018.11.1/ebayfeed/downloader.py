# -*- coding: utf-8 -*-
from datetime import datetime

from ebayfeed.constants import SCOPE_NEWLY_LISTED, _1MB
from ebayfeed.utils import gunzip


_ROUTE = "buy/feed/v1_beta/item"


def get_feed(credentials, category, scope, marketplace, date=None, brange=_1MB):
    """
    Download eBay feed for the given category, scope and marketplace using the provided credentials.
    See: https://developer.ebay.com/_api-docs/buy/feed/resources/item/methods/getItemFeed.

    Args:
        credentials (obj): An ebayfeed.Credentials object used to obtain an API access_token.
        category (int): An eBay top-level category ID of the items to be returned in the feed file.
        scope (str): Feed type to return. Must be one of [ebayfeed.SCOPE_ALL_ACTIVE, ebayfeed.SCOPE_NEWLY_LISTED].
        marketplace (str): ID of the eBay marketplace where the items are hosted.
        date (str, optional): Date of the feed file to retrieve. Must be within 3-14 days in the past.
                              Format: yyyyMMdd. Ignored when scope is ebayfeed.SCOPE_ALL_ACTIVE.
        brange (int, optional): Number of bytes downloaded at each call to FeedAPI. Must be between 1 and 10485760.
                                Default: 1e+6 (_1MB).

    Returns:
        str: Requested feed in TSV format.

    Raises:
        ValueError: If scope is ebayfeed.SCOPE_NEWLY_LISTED and date is None.
    """
    if scope == SCOPE_NEWLY_LISTED and date is None:
        raise ValueError(
            "date must be specified when scope is {}".format(SCOPE_NEWLY_LISTED)
        )
    feed_tsv = _download_tsv(
        credentials.api, credentials, category, scope, marketplace, date, brange
    )
    return feed_tsv


def _download_tsv(api, credentials, category, scope, marketplace, date, brange):
    # download and gunzip TSV feed for the given category, scope and marketplace using the provided credentials.
    headers, params = _build_req_params(credentials, category, scope, marketplace, date)
    feed_gz = _download_chunks(api, headers, params, int(brange))
    return gunzip(feed_gz)


def _build_req_params(credentials, category, scope, marketplace, date):
    # headers and params for /getItemFeed call
    headers = {
        "X-EBAY-C-MARKETPLACE-ID": marketplace,
        "Authorization": "Bearer {}".format(credentials.access_token),
    }
    params = {"feed_scope": scope, "category_id": category}
    if date:
        _date_is_correct(date)
        params["date"] = date
    return headers, params


def _date_is_correct(date):
    # check date satisfies yyyyMMdd format, else raise valueError
    datetime.strptime(date, "%Y%m%d")
    return True


def _download_chunks(api, headers, params, brange):
    # download feed chunks and cat them together
    feed_gz = b""
    bstart = 0
    while True:
        headers["Range"] = "bytes={}-{}".format(bstart, bstart + brange)
        bstart += brange + 1
        rsp = api.get(_ROUTE, headers, params)
        feed_gz = b"".join([feed_gz, rsp.content])
        feed_length = _get_feed_length(rsp.headers["Content-Range"])
        if bstart >= feed_length or rsp.status_code != 206:
            break
    return feed_gz


def _get_feed_length(content_range):
    # extract feed length (in byte) from response header Content-Range
    return int(content_range.split("/")[-1])
