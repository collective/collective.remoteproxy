# -*- coding: utf-8 -*-
from .behaviors import IRemoteProxyBehavior
from plone.dexterity.browser.traversal import DexterityPublishTraverse
from zope.component import adapter
from zope.location.interfaces import LocationError
from zope.publisher.interfaces.browser import IBrowserRequest

try:
    from repoze.zope2.publishtraverse import DefaultPublishTraverse
except ImportError:
    from ZPublisher.BaseRequest import DefaultPublishTraverse


@adapter(IRemoteProxyBehavior, IBrowserRequest)
class RemoteProxyTraverser(DefaultPublishTraverse):
    """Remote proxy traverser.
    """

    def publishTraverse(self, request, name):
        import pdb
        pdb.set_trace()
        try:
            # Default Traverser
            return DexterityPublishTraverse(
                self.context, request).publishTraverse(request, name)
        except (LocationError, KeyError):
            subpath = self.request.get('collective.remoteproxy__subpath', [])
            subpath.append(name)
            self.request['collective.remoteproxy__subpath'] = subpath
            return self.context
