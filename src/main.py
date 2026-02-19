from textnode import TextNode, TextType
import os
import shutil
import sys
from getcontent import generate_page, generate_pages_recursive

basepath = "/"
dir_path_public = "./docs"


def main():

    print(f"Assembly Complete. Using: {basepath}")


def copy_static(src, dst):
    os.makedirs(dst, exist_ok=True)

    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)

        if os.path.isfile(src_path):
            print(f"copy file: {src_path} -> {dst_path}")
            shutil.copy2(src_path, dst_path)
        else:
            print(f"copy dir:  {src_path} -> {dst_path}")
            copy_static(src_path, dst_path)


def copy_static_to_public():
    dst = "docs"
    print(f"clean: {dst}")
    shutil.rmtree(dst, ignore_errors=True)
    print(f"mkdir: {dst}")
    os.makedirs(dst, exist_ok=True)
    copy_static("static", dst)


if __name__ == "__main__":
    # Update basepath if a command-line argument is provided
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(f"Assembly Complete. Using: {basepath}")

    copy_static_to_public()

    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
