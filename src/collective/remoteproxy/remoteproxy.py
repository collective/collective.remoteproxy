# -*- coding: utf-8 -*-
from collective.remoteproxy.behaviors import IRemoteProxyBehavior
# from bs4 import UnicodeDammit
# from lxml.html.clean import clean_html
from plone.memoize import ram
from plone.memoize.volatile import DontCache
from requests.auth import HTTPBasicAuth
from time import time

import lxml
import plone.api
import re
import requests

TEXT_TYPES = (
    'application/javascript',
    'application/json',
    'application/xml',
    'text/css',
    'text/html',
    'text/plain'
)


def _results_cachekey(
    method,
    remote_url,
    content_selector=None,
    keep_scripts=False,
    keep_styles=False,
    extra_replacements=None,
    auth_user='',
    auth_pass='',
    cookies=None,
    cache_time=3600,
    standalone=None
):
    cache_time = int(cache_time)
    if not cache_time:
        # Don't cache on cache_time = 0 or any other falsy value
        raise DontCache
    timeout = time() // int(cache_time)
    cachekey = (
        remote_url,
        content_selector,
        keep_scripts,
        keep_styles,
        extra_replacements,
        auth_user,
        auth_pass,
        cookies,
        timeout,
        standalone
    )
    return cachekey


@ram.cache(_results_cachekey)
def get_content(
    remote_url,
    content_selector=None,
    keep_scripts=False,
    keep_styles=False,
    extra_replacements=None,
    auth_user='',
    auth_pass='',
    cookies=None,
    cache_time=3600,
    standalone=None
):
    """Get remote html content.
    """

    auth = None
    if auth_user and auth_pass:
        auth = HTTPBasicAuth(auth_user, auth_pass)

    text_repl_map = []
    if extra_replacements:
        for repl in extra_replacements:
            # split on "|" with negative lookbehind regex, excluding
            # "\"-escaped "|"
            text_repl = re.split(r'(?<!\\)\|', repl)
            assert(len(text_repl) == 2)
            # Replace escaped split characters
            text_repl = (
                text_repl[0].replace(u'\|', '|'),
                text_repl[1].replace(u'\|', u'|')
            )
            text_repl_map.append(text_repl)

    for repl in text_repl_map:
        # Replace text in URLs.
        remote_url = remote_url.replace(repl[0], repl[1])

    res = requests.get(remote_url, auth=auth, cookies=cookies)
    content_type = res.headers['Content-Type']

    content = None
    if content_type.split(';')[0] in TEXT_TYPES:
        # content type is typically 'text/html; charset=UTF-8'
        content = res.text
        for repl in text_repl_map:
            # Text types can be replaced.
            content = content.replace(repl[0], repl[1])
    else:
        content = res.content

    if 'text/html' not in content_type:
        # CASE NON-HTML CONTENT (IMAGES/JAVASCRIPT/CSS/WHATEVER)
        return (content, content_type)

    # CASE HTML

    # Cleanup...?
    # response = UnicodeDammit(content).unicode_markup
    # text = clean_html(content)

    tree = lxml.html.fromstring(content)

    if not keep_scripts:
        for bad in tree.xpath('/html/body//script'):
            bad.getparent().remove(bad)

    if not keep_styles:
        for bad in tree.xpath('/html/body//style'):
            bad.getparent().remove(bad)
        for bad in tree.xpath('/html/body//link'):
            bad.getparent().remove(bad)

    # Replace all relative URLs to absolute ones.
    tree.make_links_absolute(remote_url)

    c_tree = tree.cssselect(content_selector) if content_selector else [tree]

    append = []
    if keep_scripts:
        append += tree.cssselect('html head script')
    if keep_styles:
        append += tree.cssselect('html head style')
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
    # all remote proxy contents. This enables automatically linking to other
    # proxied contents.
    cat = plone.api.portal.get_tool('portal_catalog')
    proxied_contents = []
    if standalone:
        proxied_contents = cat.searchResults(
            UID=standalone
        )
    else:
        proxied_contents = cat.searchResults(
            object_provides=IRemoteProxyBehavior.__identifier__
        )
    repl_map = []
    for it in proxied_contents:
        ob = it.getObject()

        if not standalone and getattr(ob, 'standalone', False):
            # Do not include standalone proxies when not in standalone mode.
            continue

        # if the default view is not ``remoteproxyview``, we have to append
        # ``@@remoteproxyview`` to the replaced URLs.
        add_viewname = '/@@remoteproxyview'\
            if 'remoteproxyview' not in ob.getLayout()\
            else ''

        # do not include the query string or content target when replacing
        # keep them intact.
        remote_url = ob.remote_url.split('?')[0].split('#')[0].rstrip('/')
        repl_map.append(
            (
                remote_url,
                ob.absolute_url() + add_viewname
            )
        )

    # Reverse sort the replacement map, so that longest remote urls come first.
    # That way, url replacement on nexted proxies doesn't get messed up.
    repl_map.sort(
        key=lambda el: el[1],
        reverse=True
    )

    # Now, for all remote proxies, replace their remote_url with their
    # absolute_url
    for remote_url_, absolute_url_ in repl_map:
        rec = re.compile(remote_url_)
        ret = rec.sub(absolute_url_, ret)

        # Replace double-googles within the @@remoteproxyview path.
        # Traversing to those doesn't work.
        rec = re.compile('(?!(\/@@remoteproxyview))\/@@')
        ret = rec.sub('/', ret)

    return (ret, content_type)
