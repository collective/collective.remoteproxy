# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.remoteproxy -t test_remoteproxy.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.remoteproxy.testing.COLLECTIVE_REMOTEPROXY_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_remoteproxy.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Remote Proxy
  Given a logged-in site administrator
    and an add remote proxy form
   When I type 'My Remote Proxy' into the title field
    and I submit the form
   Then a remote proxy with the title 'My Remote Proxy' has been created

Scenario: As a site administrator I can view a Remote Proxy
  Given a logged-in site administrator
    and a remote proxy 'My Remote Proxy'
   When I go to the remote proxy view
   Then I can see the remote proxy title 'My Remote Proxy'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add remote proxy form
  Go To  ${PLONE_URL}/++add++RemoteProxy

a remote proxy 'My Remote Proxy'
  Create content  type=RemoteProxy  id=my-remoteproxy  title=My Remote Proxy


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the remote proxy view
  Go To  ${PLONE_URL}/my-remoteproxy
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a remote proxy with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the remote proxy title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
