import unittest
from markdown_blocks import markdown_to_blocks

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_only_whitespace(self):
            md = "   \n\n  \n\n\t\n"
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, [])

    def test_markdown_to_blocks_strips_and_ignores_empty_blocks(self):
        md = """

            First block with extra whitespace



            Second block


        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with extra whitespace",
                "Second block",
            ],
        )
