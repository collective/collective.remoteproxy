# -*- coding: utf-8 -*-
from .interfaces import IProxyType
# from bs4 import UnicodeDammit
# from lxml.html.clean import clean_html
from plone.memoize import ram
from plone.memoize.volatile import DontCache
from time import time

import lxml
import plone.api.portal
import re
import requests


def _results_cachekey(
    method,
    remote_url,
    content_selector=None,
    append_script=False,
    append_style=False,
    append_link=False,
    cache_time=3600
):
    cache_time = int(cache_time)
    if not cache_time:
        # Don't cache on cache_time = 0 or any other falsy value
        raise DontCache
    timeout = time() // int(cache_time)
    cachekey = (
        remote_url,
        content_selector,
        append_script,
        append_style,
        append_link,
        timeout
    )
    return cachekey


@ram.cache(_results_cachekey)
def get_content(
    remote_url,
    content_selector=None,
    append_script=False,
    append_link=False,
    append_style=False,
    cache_time=3600
):
    """Get remote html content.
    """

    res = requests.get(remote_url)

    content_type = res.headers['Content-Type']
    if 'text/html' not in content_type:
        # CASE NON-HTML CONTENT (IMAGES/JAVASCRIPT/CSS/WHATEVER)
        return (res.content, content_type)

    # CASE HTML

    # Cleanup...?
    # response = UnicodeDammit(res.text).unicode_markup
    # text = clean_html(res.text)

    # Replace all relative URLs to absolute ones.
    tree = lxml.html.fromstring(res.text)
    tree.make_links_absolute(remote_url)

    c_tree = tree.cssselect(content_selector) if content_selector else [tree]

    append = []
    if append_script:
        append += tree.cssselect('html head script')
    if append_style:
        append += tree.cssselect('html head style')
    if append_link:
        append += tree.cssselect('html head link')

    for el in append:
        # Append to last selected element
        c_tree[-1].append(el)

    # serialize all selected elements in order from the content tree
    ret = u'\n'.join([
        lxml.html.tostring(el, encoding='unicode')
        for el in c_tree
    ])

    # Create a list of remote_url, absolute_url tuples for replacement from
    # all proxytype contents. This enables automatically linking to other
    # proxied contents.
    cat = plone.api.portal.get_tool('portal_catalog')
    proxied_contents = cat.searchResults(
        object_provides=IProxyType.__identifier__
    )
    repl_map = [
        (
            it.getObject().remote_url,
            u'{0}/@@proxyview/'.format(it.getObject().absolute_url()),
            it.getObject().exclude_urls
        )
        for it in proxied_contents
    ]

    # Reverse sort the replacement values to support proxyviews in proxyviews
    repl_map.sort(
        key=lambda el: el[1],
        reverse=True
    )

    # Now, for all IProxyType, replace their remote_url with their absolute_url
    for remote_url_, absolute_url_, exclude_urls_ in repl_map:
        if exclude_urls_:
            rec = re.compile('(?!({0})){1}'.format(
                '|'.join(exclude_urls_),
                remote_url_
            ))
        else:
            rec = re.compile(remote_url_)
        ret = rec.sub(absolute_url_, ret)

        # Replace double-googles within the @@proxyview path.
        # Traversing to those doesn't work.
        rec = re.compile('(?!(\/@@proxyview))\/@@')
        ret = rec.sub('', ret)

    return (ret, content_type)
