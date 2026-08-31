Changelog
=========


3.1 (unreleased)
----------------

- Nothing changed yet.


3.0 (2026-09-01)
----------------

Breaking change:

- Introduce a `allowed_cookies` whitelist and set this as new default.
  To send cookies you need to enable the `send_cookies` switch and define all
  the cookies you want to send in `allowed_cookies`. An empty `allowed_cookies`
  setting will not send any cookies, even if `send_cookies` is active. You can
  use the `*` wildcard to match zero or more characters.
  [thet]

Bugfixes:

- Don't break, if plone.tiles is not installed.
  [thet]

- Fix a problem with cookie encoding.
  Fixes: #2
  [thet]


2.0 (2021-02-05)
----------------

- fix tests [jensens]

- Code tyle black, isort [jensens]

- modernize packaging and add GH Actions CI [jensens]

- py 3 support, drop py 2 support [jensens]


1.0 (2019-01-17)
----------------

- Initial release.
  [thet]

