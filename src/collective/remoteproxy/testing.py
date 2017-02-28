# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.remoteproxy


class BrowserLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.remoteproxy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.remoteproxy:default')


COLLECTIVE_REMOTEPROXY_FIXTURE = BrowserLayer()


COLLECTIVE_REMOTEPROXY = IntegrationTesting(
    bases=(COLLECTIVE_REMOTEPROXY,),
    name='BrowserLayer:IntegrationTesting'
)


COLLECTIVE_REMOTEPROXY = FunctionalTesting(
    bases=(COLLECTIVE_REMOTEPROXY,),
    name='BrowserLayer:FunctionalTesting'
)


COLLECTIVE_REMOTEPROXY = FunctionalTesting(
    bases=(
        COLLECTIVE_REMOTEPROXY,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='BrowserLayer:AcceptanceTesting'
)
