# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.remoteproxy import _
from zope import schema
from zope.interface import Interface


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

    content_selector = schema.TextLine(
        title=_(
            'label_content_selector',
            default=u'Content selector'
        ),
        description=_(
            'help_remote_url',
            default=u'CSS Selector of the content.'
                    u' If given, only the matching content will be used. '
                    u' If not given, the content response will be used as a whole.'  # noqa
                    u' Only relevant for text/html content.'
        ),
        required=False,
        missing_value=None,
        default=u'html body > *'
    )

    keep_scripts = schema.Bool(
        title=_(
            'label_keep_scripts',
            default=u'Keep scripts',
        ),
        description=_(
            'help_keep_scripts',
            default=u'Keep or drop script tags.'
                    u' Tags in the body are kept as they are,'
                    u' those from the header are appended to the content.'
        ),
        required=False,
        default=False,
    )

    keep_styles = schema.Bool(
        title=_(
            'label_styles',
            default=u'Keep styles',
        ),
        description=_(
            'help_keep_styles',
            default=u'Keep or drop CSS link and style tags.'
                    u' Tags in the body are kept as they are,'
                    u' those from the header are appended to the content.'
        ),
        required=False,
        default=False,
    )

    extra_replacements = schema.Tuple(
        title=_(
            u'label_extra_replacements',
            default=u'Extra Replacement Map'
        ),
        description=_(
            u'help_extra_replacements',
            default=u'List of search and replacement strings, separated by a "|" sign.'  # noqa
                    u' For search or replacement characters containing a "|", escape them like so: "\|".'  # noqa
                    u' One search|replacement definition per line.'
                    u' The replacement happens for each text based mime type, including application/javascript and appplication/json.'  # noqa
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
        default=()
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
