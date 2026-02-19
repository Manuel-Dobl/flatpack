import unittest

from getcontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_valid_h1_header(self):
        md = "# My Title\n\nSome body text."
        self.assertEqual(extract_title(md), "My Title")

    def test_no_h1_header_raises(self):
        md = "## Subtitle\n\nNo h1 here."
        with self.assertRaises(Exception) as cm:
            extract_title(md)
        self.assertEqual(str(cm.exception), "No Heading Detected")

    def test_h1_not_on_first_line(self):
        md = "Intro line\n\n# Actual Title\nMore text"
        self.assertEqual(extract_title(md), "Actual Title")
