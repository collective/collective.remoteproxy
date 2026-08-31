from ..remoteproxy import _cookie_name_matches
from ..remoteproxy import _filter_cookies

import unittest


class CookieFilterTest(unittest.TestCase):

    def test_exact_name(self):
        self.assertTrue(_cookie_name_matches("session", "session"))
        self.assertFalse(_cookie_name_matches("session_id", "session"))

    def test_prefix_wildcard(self):
        self.assertTrue(_cookie_name_matches("_ga_ABC123", "_ga_*"))
        self.assertFalse(_cookie_name_matches("ga_ABC123", "_ga_*"))

    def test_postfix_wildcard(self):
        self.assertTrue(_cookie_name_matches("auth_backup", "*_backup"))
        self.assertFalse(_cookie_name_matches("auth_backup_2", "*_backup"))

    def test_middle_wildcard(self):
        self.assertTrue(_cookie_name_matches("tenant_user_token", "tenant_*_token"))
        self.assertFalse(_cookie_name_matches("tenant_user_id", "tenant_*_token"))

    def test_other_characters_are_literal(self):
        self.assertTrue(_cookie_name_matches("cookie[1]", "cookie[1]"))
        self.assertFalse(_cookie_name_matches("cookie1", "cookie[1]"))

    def test_empty_allow_list_sends_no_cookies(self):
        self.assertEqual(_filter_cookies({"session": "secret"}, ()), {})

    def test_filtering_matches_names_and_preserves_values(self):
        cookies = {"_ga_ABC123": "value", "session": "secret"}
        self.assertEqual(
            _filter_cookies(cookies, ("_ga_*",)),
            {"_ga_ABC123": "value"},
        )
