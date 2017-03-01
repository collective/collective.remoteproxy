# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.remoteproxy import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBrowserLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRemoteProxySchema(Interface):
    """Schema interface for the remote proxy behavior and portlet.
    """

    remote_url = schema.TextLine(
        title=_(
            'label_remote_url',
            default=u'Remote URL'
        ),
        description=_(
            'help_remote_url',
            default='URL of the remote content which should be displayed here.'
        ),
        required=True,
    )

    exclude_urls = schema.Tuple(
        title=_(
            u'label_exclude_urls',
            default=u'Exclude URLs'
        ),
        description=_(
            u'help_exclude_urls',
            default=u'List of URLs to exclude from replacement - e.g. static '
                    u'resources, which should be loaded directly. '
                    u'One URL per line.'
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
        default=()
    )

    content_selector = schema.TextLine(
        title=_(
            'label_content_selector',
            default=u'Content selector'
        ),
        description=_(
            'help_remote_url',
            default=u'CSS Selector of the content. If given, only the '
                    u'matching content will be used. If not given, the '
                    u'content response will be used as a whole.'
        ),
        required=True,
        default=u'html body > *'
    )

    append_script = schema.Bool(
        title=_(
            'label_copy_script',
            default=u'Append script tags'
        ),
        description=_(
            'help_copy_script',
            default=u'Copy JavaScript resources from the content header '
                    u'into the body, so that they will be included in the '
                    u'output.'
        ),
        required=False,
        default=False,
    )

    append_link = schema.Bool(
        title=_(
            'label_copy_link',
            default=u'Append link tags',
        ),
        description=_(
            'help_copy_header_link',
            default=u'Copy CSS link resources from the content header into '
                    u'the body, so that they will be included in the output.'
        ),
        required=False,
        default=False,
    )

    append_style = schema.Bool(
        title=_(
            'label_copy_style',
            default=u'Append style tags',
        ),
        description=_(
            'help_copy_style',
            default=u'Copy CSS style resources from the content header into '
                    u'the body, so that they will be included in the output.'
        ),
        required=False,
        default=False,
    )

    keep_body_script = schema.Bool(
        title=_(
            'label_keep_body_script',
            default=u'Keep body script tags',
        ),
        description=_(
            'help_keep_body_script',
            default=u'Keep or drop script tags from the body.'
        ),
        required=False,
        default=False,
    )

    keep_body_link = schema.Bool(
        title=_(
            'label_keep_body_link',
            default=u'Keep body link tags',
        ),
        description=_(
            'help_keep_body_link',
            default=u'Keep or drop CSS link tags from the body.'
        ),
        required=False,
        default=False,
    )

    keep_body_style = schema.Bool(
        title=_(
            'label_keep_body_style',
            default=u'Keep body style tags',
        ),
        description=_(
            'help_keep_body_style',
            default=u'Keep or drop style tags from the body.'
        ),
        required=False,
        default=False,
    )

    auth_user = schema.TextLine(
        title=_(
            'label_auth_user',
            default=u'Username'
        ),
        description=_(
            'help_auth_user',
            default=u'Optional username for basic HTTP authentication.'
        ),
        required=False,
        default=u'',
    )

    auth_pass = schema.TextLine(
        title=_(
            'label_auth_pass',
            default=u'Password'
        ),
        description=_(
            'help_auth_pass',
            default=u'Optional password for basic HTTP authentication.'
        ),
        required=False,
        default=u'',
    )

    send_cookies = schema.Bool(
        title=_(
            'label_send_cookies',
            default=u'Send cookies',
        ),
        description=_(
            'help_send_cookies',
            default=u'Send cookies of your own domain to the server.'
        ),
        required=False,
        default=False,
    )

    cache_time = schema.TextLine(
        title=_(
            'label_cache_time',
            default=u'Cache time'
        ),
        description=_(
            'help_cache_time',
            default=u'Time to cache the remote content in seconds. '
                    u'Empty or 0 for no caching.'  # noqa
        ),
        required=False,
        default=u'3600',
    )
