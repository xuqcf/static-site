import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_with_tag(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Click me!</a>')
    
    def test_leaf_no_tag(self):
        node = LeafNode(None, "just raw text")
        self.assertEqual(node.to_html(), "just raw text")
    
    def test_no_value_raises(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
