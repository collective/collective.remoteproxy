"""Module where all interfaces, events and exceptions live."""

from collective.remoteproxy import _
from zope import schema
from zope.interface import Interface


class IRemoteProxySchema(Interface):
    """Schema interface for the remote proxy behavior and portlet."""

    remote_url = schema.TextLine(
        title=_("label_remote_url", default="Remote URL"),
        description=_(
            "help_remote_url",
            default="URL of the remote content which should be displayed here.",
        ),
        required=True,
    )

    content_selector = schema.TextLine(
        title=_("label_content_selector", default="Content selector"),
        description=_(
            "help_remote_url",
            default="CSS Selector of the content."
            " If given, only the matching content will be used. "
            " If not given, the content response will be used as a whole."
            " Only relevant for text/html content.",
        ),
        required=False,
        missing_value=None,
        default="html body > *",
    )

    keep_scripts = schema.Bool(
        title=_(
            "label_keep_scripts",
            default="Keep scripts",
        ),
        description=_(
            "help_keep_scripts",
            default="Keep or drop script tags."
            " Tags in the body are kept as they are,"
            " those from the header are appended to the content.",
        ),
        required=False,
        default=False,
    )

    keep_styles = schema.Bool(
        title=_(
            "label_styles",
            default="Keep styles",
        ),
        description=_(
            "help_keep_styles",
            default="Keep or drop CSS link and style tags."
            " Tags in the body are kept as they are,"
            " those from the header are appended to the content.",
        ),
        required=False,
        default=False,
    )

    extra_replacements = schema.Tuple(
        title=_("label_extra_replacements", default="Extra Replacement Map"),
        description=_(
            "help_extra_replacements",
            default='List of search and replacement strings, separated by a "|" sign.'
            ' For search or replacement characters containing a "|", escape them like so: "\\|".'
            " One search|replacement definition per line."
            " The replacement happens for each text based mime type, "
            "including application/javascript and appplication/json.",
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
        default=(),
    )

    auth_user = schema.TextLine(
        title=_("label_auth_user", default="Username"),
        description=_(
            "help_auth_user",
            default="Optional username for basic HTTP authentication.",
        ),
        required=False,
        default="",
    )

    auth_pass = schema.TextLine(
        title=_("label_auth_pass", default="Password"),
        description=_(
            "help_auth_pass",
            default="Optional password for basic HTTP authentication.",
        ),
        required=False,
        default="",
    )

    send_cookies = schema.Bool(
        title=_(
            "label_send_cookies",
            default="Send cookies",
        ),
        description=_(
            "help_send_cookies",
            default="Send cookies of your own domain to the server.",
        ),
        required=False,
        default=False,
    )

    standalone = schema.Bool(
        title=_(
            "label_standalone",
            default="Standalone proxy",
        ),
        description=_(
            "help_standalone",
            default="Let this proxy be a standalone proxy which ignores "
            "other proxies and is ignored by other proxies. "
            "This way it will not rewrite to other remote URLs "
            "configured by other proxies.",
        ),
        required=False,
        default=False,
    )

    cache_time = schema.TextLine(
        title=_("label_cache_time", default="Cache time"),
        description=_(
            "help_cache_time",
            default="Time to cache the remote content in seconds. "
            "Empty or 0 for no caching.",
        ),
        required=False,
        default="3600",
    )
