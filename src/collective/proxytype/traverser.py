# -*- coding: utf-8 -*-
from .interfaces import IProxyType
from plone.dexterity.browser.traversal import DexterityPublishTraverse
from zope.component import adapter
from zope.location.interfaces import LocationError
from zope.publisher.interfaces.browser import IBrowserRequest

try:
    from repoze.zope2.publishtraverse import DefaultPublishTraverse
except ImportError:
    from ZPublisher.BaseRequest import DefaultPublishTraverse


@adapter(IProxyType, IBrowserRequest)
class ProxyTraverser(DefaultPublishTraverse):
    """ProxyType traverser.
    """

    def publishTraverse(self, request, name):
        try:
            # Default Traverser
            return DexterityPublishTraverse(
                self.context, request).publishTraverse(request, name)
        except (LocationError, KeyError):
            subpath = self.request.get('collective.proxytype__subpath', [])
            subpath.append(name)
            self.request['collective.proxytype__subpath'] = subpath
            return self.context
