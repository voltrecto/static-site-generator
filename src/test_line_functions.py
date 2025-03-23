import unittest
from line_functions import *
from textnode import TextNode, TextType

class TestLineFunctions(unittest.TestCase):
    def test_simple(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is text with a ", TextType.TEXT), 
                    TextNode("code block", TextType.CODE), 
                    TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_no_delim(self):
        node = TextNode("Plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_mixed(self):
        node = TextNode("Text with `code` and more text", TextType.TEXT)
        node2 = TextNode("I'm bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and more text", TextType.TEXT),
            TextNode("I'm bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)     

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)   

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)   

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_only_text(self):
        node = TextNode("This is just text.", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is just text.", TextType.TEXT)],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [Google link](https://www.google.com) and nothing else.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("Google link", TextType.LINK, "https://www.google.com"),
                TextNode(" and nothing else.", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()