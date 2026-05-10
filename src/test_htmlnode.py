import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_single(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_props_none(self):
        node = HTMLNode("p", "Hello", None, None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr(self):
        node = HTMLNode("p", "Hello", None, None)
        self.assertEqual(repr(node), "TextNode(p, Hello, None, None)")

    def test_to_html_raises(self):
        node = HTMLNode("p", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
if __name__ == "__main__":
    unittest.main()
