from test_markdown_to_html import markdown_to_html_node


def run_case(name, md):
    print("\n" + "=" * 20)
    print(name)
    print("=" * 20)
    node = markdown_to_html_node(md)
    # If you have a to_html() method, use it:
    # print(node.to_html())
    print(node)  # fallback: prints object repr


if __name__ == "__main__":
    run_case("Paragraph", "Hello\nworld")
    run_case("Heading", "## Title")
    run_case("Unordered list", "- a\n- b\n- c")
    run_case("Ordered list", "1. a\n2. b\n3. c")
    run_case("Quote", "> one\n> two")
    run_case("Code", "```\nprint('hi')\n```")
