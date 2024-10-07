import unittest
from helper import *

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )
class TestTextToTextNodes(unittest.TestCase):
    
    def test_plain_text(self):
        text = "This is a plain text."
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is a plain text.")
        self.assertEqual(nodes[0].text_type, text_type_text)

    def test_text_with_bold(self):
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, text_type_text)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, text_type_bold)
        self.assertEqual(nodes[2].text, " text.")
        self.assertEqual(nodes[2].text_type, text_type_text)

    def test_text_with_italics(self):
        text = "This is *italic* text."
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, text_type_text)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, text_type_italic)
        self.assertEqual(nodes[2].text, " text.")
        self.assertEqual(nodes[2].text_type, text_type_text)

    def test_text_with_code(self):
        text = "This is `code` text."
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, text_type_text)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, text_type_code)
        self.assertEqual(nodes[2].text, " text.")
        self.assertEqual(nodes[2].text_type, text_type_text)

    def test_text_with_link(self):
        text = "This is a [link](http://example.com)."
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[0].text_type, text_type_text)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, text_type_link)
        self.assertEqual(nodes[1].url, "http://example.com")
        self.assertEqual(nodes[2].text, ".")
        self.assertEqual(nodes[2].text_type, text_type_text)

    def test_text_with_image(self):
        text = "Here is an image ![alt](image_url)."
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Here is an image ")
        self.assertEqual(nodes[0].text_type, text_type_text)
        self.assertEqual(nodes[1].text, "alt")
        self.assertEqual(nodes[1].text_type, text_type_image)
        self.assertEqual(nodes[1].url, "image_url")
        self.assertEqual(nodes[2].text, ".")
        self.assertEqual(nodes[2].text_type, text_type_text)

    def test_text_with_combined_formatting(self):
        text = "Here is a **bold** word, *italic* word, and `code` snippet with a [link](http://example.com) and an image ![alt](image_url)."
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 11)
        self.assertEqual(nodes[0].text, "Here is a ")
        self.assertEqual(nodes[0].text_type, text_type_text)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, text_type_bold)
        self.assertEqual(nodes[2].text, " word, ")
        self.assertEqual(nodes[2].text_type, text_type_text)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, text_type_italic)
        self.assertEqual(nodes[4].text, " word, and ")
        self.assertEqual(nodes[4].text_type, text_type_text)
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, text_type_code)
        self.assertEqual(nodes[6].text, " snippet with a ")
        self.assertEqual(nodes[6].text_type, text_type_text)
        self.assertEqual(nodes[7].text, "link")
        self.assertEqual(nodes[7].text_type, text_type_link)
        self.assertEqual(nodes[7].url, "http://example.com")
        self.assertEqual(nodes[8].text, " and an image ")
        self.assertEqual(nodes[8].text_type, text_type_text)
        self.assertEqual(nodes[9].text, "alt")
        self.assertEqual(nodes[9].text_type, text_type_image)
        self.assertEqual(nodes[9].url, "image_url")
        self.assertEqual(nodes[10].text, ".")
        self.assertEqual(nodes[10].text_type, text_type_text)



class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_block(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_block(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )




if __name__ == "__main__":
    unittest.main()