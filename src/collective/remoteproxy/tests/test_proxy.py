# -*- coding: utf-8 -*-
from collective.remoteproxy.behaviors import IRemoteProxyBehavior
from collective.remoteproxy.interfaces import IRemoteProxySchema
from collective.remoteproxy.testing import COLLECTIVE_PROXY_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest2 as unittest


class RemoteProxyIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PROXY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='RemoteProxy')
        schema = fti.lookupSchema()
        import pdb
        pdb.set_trace()
        self.assertEqual(IRemoteProxySchema, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='RemoteProxy')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='RemoteProxy')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IRemoteProxyBehavior.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('RemoteProxy', 'RemoteProxy')
        self.assertTrue(
            IRemoteProxyBehavior.providedBy(self.portal['RemoteProxy'])
        )
