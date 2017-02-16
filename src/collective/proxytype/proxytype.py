# -*- coding: utf-8 -*-
from .interfaces import IProxyType
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IProxyType)
class ProxyType(Container):
    """Proxy type
    """
