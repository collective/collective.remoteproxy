# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.remoteproxy.testing import COLLECTIVE_REMOTEPROXY_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.remoteproxy is properly installed."""

    layer = COLLECTIVE_REMOTEPROXY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.remoteproxy is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.remoteproxy'))

    def test_browserlayer(self):
        """Test that IBrowserLayer is registered."""
        from collective.remoteproxy.interfaces import IBrowserLayer
        from plone.browserlayer import utils
        self.assertIn(IBrowserLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_REMOTEPROXY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.remoteproxy'])

    def test_product_uninstalled(self):
        """Test if collective.remoteproxy is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.remoteproxy'))
