import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode("p", "this is a paragraph", children=None, props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props(self):
        node = HTMLNode("a", "Boot.dev", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_multiple_attributes(self):
        node = HTMLNode(
            "a",
            "Boot.dev",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "one")
        child2 = LeafNode("span", "two")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(), "<div><span>one</span><span>two</span></div>"
        )

    def test_to_html_raises_when_children_missing(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()


if __name__ == "__main__":
    unittest.main()
