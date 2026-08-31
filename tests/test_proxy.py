from collective.remoteproxy.behaviors import IRemoteProxyBehavior
from collective.remoteproxy.interfaces import IRemoteProxySchema
from collective.remoteproxy.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class RemoteProxyIntegrationTest(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior(self):
        fti = queryUtility(IDexterityFTI, name="RemoteProxy")
        self.assertIn("collective.remoteproxy", fti.behaviors)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="RemoteProxy")
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="RemoteProxy")
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IRemoteProxyBehavior.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory("RemoteProxy", "RemoteProxy")
        self.assertTrue(IRemoteProxyBehavior.providedBy(self.portal["RemoteProxy"]))
