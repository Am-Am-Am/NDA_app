import unittest
import re

from nda_email.forms import EMAIL_PATTERN, PHONE_PATTERN


class TestEmailRegex(unittest.TestCase):
    def setUp(self):
        self.regex = re.compile(EMAIL_PATTERN)

    def test_valid_emails(self):
        valid_emails = [
            "a@b.com",
            "a.b@c.d.ru",
            "adsfsdfsf.bgfdgdfg12@cdgfdfgd25.ddfgdgf25.ru ",
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertIsNotNone(self.regex.match(email))

    def test_invalid_emails(self):
        invalid_emails = [
            "a@b",
            "a@b.c",
            "abc",
            "a@b@c",
            ""
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertIsNone(self.regex.match(email))


class TestPhoneRegex(unittest.TestCase):
    def setUp(self):
        self.regex = re.compile(PHONE_PATTERN)

    def test_valid_phones(self):
        valid_phones = [
            "+79130073119",
            "79130073119",
            "7-913-0073119",
            "7:913:007:31:19",
            "7.913.007.31.19",
            "083 120 56 20",
            "8(846)2569888",
            "8(3432)5698888"
        ]
        for phone in valid_phones:
            with self.subTest(phone=phone):
                self.assertIsNotNone(self.regex.match(phone))

    def test_invalid_phones(self):
        invalid_phones = [
            "+7913007311g",
            "7913@0073119",
            "5573212",
            "332 12 07",
            "01234567890123456789",
            "+7  91 3   007 31  1   9",
            "84456464641g"
            "898553@10868"
            ""
        ]
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                self.assertIsNone(self.regex.match(phone))


if __name__ == '__main__':
    unittest.main()
