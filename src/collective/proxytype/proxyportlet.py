# -*- coding: utf-8 -*-
from . import _
from .proxy import get_content
from Products.CMFPlone.utils import getFSVersionTuple
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.interface import implements
from collective.proxytype.interfaces import IProxySchema


PLONE5 = getFSVersionTuple()[0] >= 5

if PLONE5:
    base_AddForm = base.AddForm
    base_EditForm = base.EditForm
else:
    from plone.app.portlets.browser.z3cformhelper import AddForm as base_AddForm  # noqa
    from plone.app.portlets.browser.z3cformhelper import EditForm as base_EditForm  # noqa
    from z3c.form import field


class IProxyBasePortlet(IPortletDataProvider):
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


class IProxyPortlet(IProxyBasePortlet, IProxySchema):
    """Full proxy portlet schema interface.
    IProxyBasePortlet as first item to get it's fields first.
    """


class Assignment(base.Assignment):
    implements(IProxyPortlet)

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
            return _(u'Proxy Portlet')


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('proxyportlet.pt')

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
        schema = IProxyPortlet
    else:
        fields = field.Fields(IProxyPortlet)

    label = _(u"Add Proxy Portlet")
    description = _(
        u"This portlet allows to display remote content."
    )

    def create(self, data):
        return Assignment(**data)


class EditForm(base_EditForm):
    if PLONE5:
        schema = IProxyPortlet
    else:
        fields = field.Fields(IProxyPortlet)

    label = _(u"Edit Proxy Portlet")
    description = _(
        u"This portlet allows to display remote content."
    )
