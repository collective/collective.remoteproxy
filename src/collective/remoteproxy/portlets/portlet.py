from collective.remoteproxy import _
from collective.remoteproxy.interfaces import IRemoteProxySchema
from collective.remoteproxy.remoteproxy import get_content
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFPlone.utils import getFSVersionTuple
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


PLONE5 = getFSVersionTuple()[0] >= 5

if PLONE5:
    base_AddForm = base.AddForm
    base_EditForm = base.EditForm
else:
    from plone.app.portlets.browser.z3cformhelper import AddForm as base_AddForm  # noqa
    from plone.app.portlets.browser.z3cformhelper import (
        EditForm as base_EditForm,
    )  # noqa
    from z3c.form import field


class IRemoteProxyBasePortlet(IPortletDataProvider):
    """Portlet base schema interface."""

    header = schema.TextLine(
        title=_("label_header", default="Portlet header"),
        description=_("help_header", "Title of the rendered portlet."),
        required=False,
        default="",
    )


class IRemoteProxyPortlet(IRemoteProxyBasePortlet, IRemoteProxySchema):
    """Full proxy portlet schema interface.
    IRemoteProxyBasePortlet as first item to get it's fields first.
    """


@implementer(IRemoteProxyPortlet)
class Assignment(base.Assignment):
    def __init__(
        self,
        header,
        remote_url,
        content_selector,
        keep_scripts,
        keep_styles,
        extra_replacements,
        auth_user,
        auth_pass,
        send_cookies,
        cache_time,
    ):
        self.header = header
        self.remote_url = remote_url
        self.content_selector = content_selector
        self.keep_scripts = keep_scripts
        self.keep_styles = keep_styles
        self.extra_replacements = extra_replacements
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.send_cookies = send_cookies
        self.cache_time = cache_time

    @property
    def title(self):
        if self.header:
            return self.header
        else:
            return _("Remote Proxy Portlet")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile("portlet.pt")

    @property
    def available(self):
        return True

    def get_content(self):
        cookies = self.request.cookies if self.data.send_cookies else None
        content, content_type = get_content(
            remote_url=self.data.remote_url,
            content_selector=self.data.content_selector,
            keep_scripts=self.data.keep_scripts,
            keep_styles=self.data.keep_styles,
            extra_replacements=self.extra_replacements,
            auth_user=self.data.auth_user,
            auth_pass=self.data.auth_pass,
            cookies=cookies,
            cache_time=self.data.cache_time,
        )
        return content

    def update(self):
        pass


class AddForm(base_AddForm):
    if PLONE5:
        schema = IRemoteProxyPortlet
    else:
        fields = field.Fields(IRemoteProxyPortlet)

    label = _("Add Remote Proxy Portlet")
    description = _("This portlet allows to display remote content.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base_EditForm):
    if PLONE5:
        schema = IRemoteProxyPortlet
    else:
        fields = field.Fields(IRemoteProxyPortlet)

    label = _("Edit Remote Proxy Portlet")
    description = _("This portlet allows to display remote content.")
