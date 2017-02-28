# -*- coding: utf-8 -*-
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
    from plone.app.portlets.browser.z3cformhelper import EditForm as base_EditForm  # noqa
    from z3c.form import field


class IRemoteProxyBasePortlet(IPortletDataProvider):
    """Portlet base schema interface.
    """

    header = schema.TextLine(
        title=_('label_header', default=u'Portlet header'),
        description=_(
            'help_header',
            u'Title of the rendered portlet.'
        ),
        required=False,
        default=u""
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
        exclude_urls,
        content_selector,
        append_script,
        append_link,
        append_style,
        cache_time
    ):
        self.header = header
        self.remote_url = remote_url
        self.exclude_urls = exclude_urls
        self.content_selector = content_selector
        self.append_script = append_script
        self.append_link = append_link
        self.append_style = append_style
        self.cache_time = cache_time

    @property
    def title(self):
        if self.header:
            return self.header
        else:
            return _(u'Remote Proxy Portlet')


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('portlet.pt')

    @property
    def available(self):
        return True

    def get_content(self):
        content, content_type = get_content(
            remote_url=self.data.remote_url,
            content_selector=self.data.content_selector,
            append_script=self.data.append_script,
            append_link=self.data.append_link,
            append_style=self.data.append_style,
            cache_time=self.data.cache_time
        )
        return content

    def update(self):
        pass


class AddForm(base_AddForm):
    if PLONE5:
        schema = IRemoteProxyPortlet
    else:
        fields = field.Fields(IRemoteProxyPortlet)

    label = _(u'Add Remote Proxy Portlet')
    description = _(
        u'This portlet allows to display remote content.'
    )

    def create(self, data):
        return Assignment(**data)


class EditForm(base_EditForm):
    if PLONE5:
        schema = IRemoteProxyPortlet
    else:
        fields = field.Fields(IRemoteProxyPortlet)

    label = _(u'Edit Remote Proxy Portlet')
    description = _(
        u'This portlet allows to display remote content.'
    )
