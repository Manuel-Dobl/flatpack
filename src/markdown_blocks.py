from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    # takes markdown text and cleans it up and makes it blocks first
    stripped_string = markdown.strip()
    split_string = stripped_string.split("\n\n")

    cleaned_blocks = []
    for s in split_string:
        stripped_split = s.strip()
        if stripped_split != "":
            cleaned_blocks.append(stripped_split)
    return cleaned_blocks


def block_to_block_type(block):
    split_block = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    elif block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE

    elif block.startswith(">"):
        split_block = block.split("\n")
        for split in split_block:
            if split[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    elif block.startswith("- "):
        split_block = block.split("\n")
        for split in split_block:
            if split[0:2] != "- ":
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    elif block.startswith("1. "):
        lines = block.split("\n")

        expected_num = 1

        for line in lines:
            prefix = f"{expected_num}. "
            if not line.startswith(prefix):
                return BlockType.PARAGRAPH
            expected_num += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
