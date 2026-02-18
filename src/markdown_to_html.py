from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes


def text_to_children(text):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]


def markdown_to_html_node(markdown):

    # takes markdown text and cleans it up and makes a list of clean blocks
    blocks = markdown_to_blocks(markdown)
    # loop over each block
    block_list = []
    for block in blocks:
        # determine type of block
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            paragraph_text = " ".join(block.splitlines())
            newnode = ParentNode("p", text_to_children(paragraph_text))
            block_list.append(newnode)

        elif block_type == BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            tag = f"h{level}"
            heading_text = block[level:].lstrip()
            newnode = ParentNode(tag, text_to_children(heading_text))
            block_list.append(newnode)

        elif block_type == BlockType.CODE:
            raw = block[4:-4]
            code_leaf = LeafNode("code", raw)
            newnode = ParentNode("pre", [code_leaf])
            block_list.append(newnode)

        elif block_type == BlockType.QUOTE:
            lines = block.splitlines()
            clean_lines = [line.lstrip("> ").lstrip(">") for line in lines]
            quote_text = "\n".join(clean_lines)
            newnode = ParentNode("blockquote", text_to_children(quote_text))
            block_list.append(newnode)

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.splitlines()
            clean_items = [item[2:] for item in items]  # removes "- " or "* "
            li_nodes = [
                ParentNode("li", text_to_children(text)) for text in clean_items
            ]
            newnode = ParentNode("ul", li_nodes)
            block_list.append(newnode)

        elif block_type == BlockType.ORDERED_LIST:
            items = block.splitlines()
            clean_items = [item.split(" ", 1)[1] for item in items]
            li_nodes = [
                ParentNode("li", text_to_children(text)) for text in clean_items
            ]
            newnode = ParentNode("ol", li_nodes)
            block_list.append(newnode)

    return ParentNode("div", block_list)
