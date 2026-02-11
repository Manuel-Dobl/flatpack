from textnode import TextNode, TextType



def main():
    test = TextNode("this some text", TextType.LINK, "https://www.boot.dev")

    print(test)

main()
