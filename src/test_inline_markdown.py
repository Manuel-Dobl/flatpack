import unittest

from inline_markdown import extract_markdown_images, extract_markdown_links, text_to_textnodes
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_both(self):
        matches = extract_markdown_links(
            "Check out ![logo](https://example.com/logo.png) and visit [my site](https://example.com)"
        )
        self.assertListEqual([("my site", "https://example.com")], matches)

class TestTexttoTextNodes(unittest.TestCase):
    def test_text_to_textnodes_plain_text(self):
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

if __name__ == "__main__":
    unittest.main()
