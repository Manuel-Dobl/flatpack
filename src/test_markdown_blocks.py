import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


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

    # --- Headings ---
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Tiny"), BlockType.HEADING)

    def test_heading_not_heading_when_no_space(self):
        # "#Title" doesn't match "# " prefix
        self.assertEqual(block_to_block_type("#Title"), BlockType.PARAGRAPH)

    # --- Code blocks ---
    def test_code_block(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_missing_closing_fence_is_paragraph(self):
        block = "```\nprint('hi')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_missing_opening_fence_is_paragraph(self):
        block = "print('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Quotes ---
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> hello"), BlockType.QUOTE)

    def test_quote_multi_line_all_prefixed(self):
        block = "> a\n> b\n> c"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multi_line_one_line_not_prefixed_becomes_paragraph(self):
        block = "> a\nb\n> c"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Unordered lists ---
    def test_unordered_list_single_line(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multi_line_all_prefixed(self):
        block = "- a\n- b\n- c"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multi_line_one_line_not_prefixed_becomes_paragraph(self):
        block = "- a\nb\n- c"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Ordered lists ---
    def test_ordered_list_valid_sequence(self):
        block = "1. a\n2. b\n3. c"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_number_becomes_paragraph(self):
        block = "1. a\n3. b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_prefix_becomes_paragraph(self):
        block = "1) a\n2) b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Default ---
    def test_default_paragraph(self):
        self.assertEqual(block_to_block_type("just some text"), BlockType.PARAGRAPH)
